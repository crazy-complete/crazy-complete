'''This module contains helper functions for Fish.'''

from . import helpers

_QUERY = helpers.FishFunction('query', r'''
# ===========================================================================
#
# This function implements the parsing of options and positionals in the Fish shell.
#
# Usage: query <OPTIONS> <COMMAND> [ARGS...]
#
# The first argument is a comma-separated list of options that the parser should know about.
# Short options (-o), long options (--option), and old-style options (-option) are supported.
#
# If an option takes an argument, it is suffixed by '='.
# If an option takes an optional argument, it is suffixed by '=?'.
#
# For example:
#   query '-f,--flag,-old-style,--with-arg=,--with-optional=?' [...]
#
#   Here, -f, --flag and -old-style don't take options, --with-arg requires an
#   argument and --with-optional takes an optional argument.
#
# COMMANDS
#   positional_contains <NUM> <WORDS...>
#     Checks if the positional argument number NUM is one of WORDS.
#     NUM counts from one.
#
#   has_option [WITH_INCOMPLETE] <OPTIONS...>
#     Checks if an option given in OPTIONS is passed on commandline.
#     If an option requires an argument, this command returns true only if the
#     option includes an argument. If 'WITH_INCOMPLETE' is specified, it also
#     returns true for options missing their arguments.
#
#   option_is <OPTIONS...> -- <VALUES...>
#     Checks if any option in OPTIONS has a value of VALUES.
#
#   num_of_positionals [<OPERATOR> <NUMBER>]
#     Checks the number of positional arguments.
#     If no arguments are provided, print the total count of positional arguments.
#     If two arguments are provided, the first argument should be one of
#     the comparison operators: '-lt', '-le', '-eq', '-ne', '-gt', '-ge'.
#     Returns 0 if the count of positional arguments matches the
#     specified NUMBER according to the comparison operator, otherwise returns 1.
#
# ===========================================================================

set -l positionals
#ifdef positionals_positions
set -l positionals_positions
#endif
set -l having_options
set -l option_values

#ifdef DEBUG
switch (count $argv)
  case 0
    echo '%FUNCNAME%: missing OPTIONS argument' >&2
    return 1
  case 1
    echo '%FUNCNAME%: missing COMMAND' >&2
    return 1
end
#endif

set -l options $argv[1]
set -e argv[1]

set -l cmd $argv[1]
set -e argv[1]

set -l my_cache_key "$(commandline -b) $options"

if test "$__QUERY_CACHE_KEY" = "$my_cache_key"
  set positionals    $__QUERY_CACHE_POSITIONALS
#ifdef positionals_positions
  set positionals_positions $__QUERY_CACHE_POSITIONALS_POSITIONS
#endif
  set having_options $__QUERY_CACHE_HAVING_OPTIONS
  set option_values  $__QUERY_CACHE_OPTION_VALUES
else
  # =========================================================================
  # Parsing of OPTIONS argument
  # =========================================================================

#ifdef short_options
  set -l short_opts_with_arg
  set -l short_opts_without_arg
  set -l short_opts_with_optional_arg
#endif
#ifdef long_options
  set -l long_opts_with_arg
  set -l long_opts_without_arg
  set -l long_opts_with_optional_arg
#endif
#ifdef old_options
  set -l old_opts_with_arg
  set -l old_opts_without_arg
  set -l old_opts_with_optional_arg
#endif

  set -l option

  if test -n "$options"
    for option in (string split -- ',' $options)
      if false
        true
#ifdef long_options
      else if string match -qr -- '^--.+=$' $option
        set -a long_opts_with_arg (string replace -- '=' '' $option)
      else if string match -qr -- '^--.+=\?$' $option
        set -a long_opts_with_optional_arg (string replace -- '=?' '' $option)
      else if string match -qr -- '^--.+$' $option
        set -a long_opts_without_arg $option
#endif
#ifdef short_options
      else if string match -qr -- '^-.=$' $option
        set -a short_opts_with_arg (string replace -- '=' '' $option)
      else if string match -qr -- '^-.=\?$' $option
        set -a short_opts_with_optional_arg (string replace -- '=?' '' $option)
      else if string match -qr -- '^-.$' $option
        set -a short_opts_without_arg $option
#endif
#ifdef old_options
      else if string match -qr -- '^-..+=$' $option
        set -a old_opts_with_arg (string replace -- '=' '' $option)
      else if string match -qr -- '^-..+=\?$' $option
        set -a old_opts_with_optional_arg (string replace -- '=?' '' $option)
      else if string match -qr -- '^-..+$' $option
        set -a old_opts_without_arg $option
#endif
      end
    end
  end

  # =========================================================================
  # Parsing of options and positionals
  # =========================================================================

  set -l cmdline (commandline -poc)
  set -l cmdline_count (count $cmdline)

  set -l argi 2 # cmdline[1] is command name
  while test $argi -le $cmdline_count
    set -l arg "$cmdline[$argi]"
    set -l have_trailing_arg (test $argi -lt $cmdline_count && echo true || echo false)

    switch $arg
      case '-'
        set -a positionals -
#ifdef positionals_positions
        set -s positionals_positions $argi
#endif
      case '--'
        set -a positionals $cmdline[$(math $argi + 1)..]
#ifdef positionals_positions
        set -a positionals_positions (command seq (math $argi + 1) $cmdline_count)
#endif
        break
      case '--*=*'
        set -l split (string split -m 1 -- '=' $arg)
        set -a having_options $split[1]
        set -a option_values "$split[2]"
      case '--*'
#ifdef long_options
        if contains -- $arg $long_opts_with_arg
          if $have_trailing_arg
            set -a having_options $arg
            set -a option_values $cmdline[(math $argi + 1)]
            set argi (math $argi + 1)
          end
        else
          set -a having_options $arg
          set -a option_values ''
        end
#endif
      case '-*'
        set -l end_of_parsing false
#ifdef old_options

        if string match -q -- '*=*' $arg
          set -l split (string split -m 1 -- '=' $arg)
          if contains -- $split[1] $old_opts_with_arg $old_opts_with_optional_arg
            set -a having_options $split[1]
            set -a option_values "$split[2]"
            set end_of_parsing true
          end
        else if contains -- $arg $old_opts_with_arg
          set end_of_parsing true
          if $have_trailing_arg
            set -a having_options $arg
            set -a option_values $cmdline[(math $argi + 1)]
            set argi (math $argi + 1)
          end
        else if contains -- $arg $old_opts_without_arg $old_opts_with_optional_arg
          set -a having_options $arg
          set -a option_values ''
          set end_of_parsing true
        end
#endif
#ifdef short_options

        set -l arg_length (string length -- $arg)
        set -l i 2
        while not $end_of_parsing; and test $i -le $arg_length
          set -l option "-$(string sub -s $i -l 1 -- $arg)"
          set -l trailing_chars "$(string sub -s (math $i + 1) -- $arg)"

          if contains -- $option $short_opts_without_arg
            set -a having_options $option
            set -a option_values ''
          else if contains -- $option $short_opts_with_arg
            set end_of_parsing true

            if test -n "$trailing_chars"
              set -a having_options $option
              set -a option_values $trailing_chars
            else if $have_trailing_arg
              set -a having_options $option
              set -a option_values $cmdline[(math $argi + 1)]
              set argi (math $argi + 1)
            end
          else if contains -- $option $short_opts_with_optional_arg
            set end_of_parsing true
            set -a having_options $option
            set -a option_values "$trailing_chars" # may be empty
          end

          set i (math $i + 1)
        end
#endif
      case '*'
        set -a positionals $arg
#ifdef positionals_positions
        set -a positionals_positions $argi
#endif
    end

    set argi (math $argi + 1)
  end

  set -g __QUERY_CACHE_POSITIONALS    $positionals
#ifdef positionals_positions
  set -g __QUERY_CACHE_POSITIONALS_POSITIONS $positionals_positions
#endif
  set -g __QUERY_CACHE_HAVING_OPTIONS $having_options
  set -g __QUERY_CACHE_OPTION_VALUES  $option_values
  set -g __QUERY_CACHE_KEY            $my_cache_key
end

# ===========================================================================
# Commands
# ===========================================================================

switch $cmd
#ifdef positional_contains
  case 'positional_contains'
    if test (count $argv) -eq 0
      echo '%FUNCNAME%: positional_contains: argv[3]: missing number' >&2
      return 1
    end

    set -l positional_num $argv[1]
    set -e argv[1]
    contains -- $positionals[$positional_num] $argv && return 0 || return 1
#endif
#ifdef has_option
  case 'has_option'
#ifdef with_incomplete
    set -l with_incomplete false

    if test $argv[1] = 'WITH_INCOMPLETE'
      set with_incomplete true
      set -e argv[1]
    end

#endif
    for option in $having_options
      contains -- $option $argv && return 0
    end

#ifdef with_incomplete
    if $with_incomplete
      set -l tokens (commandline -po)
      set -e tokens[1]
      for option in $argv
        if test 2 -eq (string length -- $option)
          set option (string sub -l 1 -s 2 -- $option)
          string match -q -r -- "^-[A-z0-9]*$option\$"   $tokens[-2] && return 0
          string match -q -r -- "^-[A-z0-9]*$option.*\$" $tokens[-1] && return 0
        else
          string match -q -r -- "^$option\$"       $tokens[-2] && return 0
          string match -q -r -- "^$option(=.*)?\$" $tokens[-1] && return 0
          contains -- $tokens[-1] $argv && return 0
        end
      end
    end

#endif
    return 1
#endif
#ifdef num_of_positionals
  case 'num_of_positionals'
    switch (count $argv)
      case 0
        count $positionals
      case 1
        echo '%FUNCNAME%: num_of_positionals: $argv[1]: missing operand' >&2
        return 1
      case 2
        if contains -- $argv[1] -lt -le -eq -ne -gt -ge;
          test (count $positionals) $argv[1] $argv[2] && return 0 || return 1
        else
          echo '%FUNCNAME%: num_of_positionals: $argv[1]: unknown operator' >&2
          return 1
        end
      case '*'
        echo '%FUNCNAME%: num_of_positionals: too many arguments' >&2
        return 1
    end
#endif
#ifdef option_is
  case 'option_is'
    set -l options
    set -l values

    for arg in $argv
      set -e argv[1]

      if string match -q -- -- $arg
        set values $argv
        break
      else
        set -a options $arg
      end
    end

    if test (count $values) -eq 0
      echo '%FUNCNAME%: missing values' >&2
      return 1
    end

    set -l i (count $having_options)
    while test $i -ge 1
      if contains -- $having_options[$i] $options
        if contains -- $option_values[$i] $values
          return 0
        end
      end

      set i (math $i - 1)
    end

    return 1
#endif
#ifdef positionals_positions
  case 'positional_pos'
    echo $positionals_positions[$argv[1]]
#endif
#ifdef DEBUG
  case '*'
    echo '%FUNCNAME%: argv[2]: invalid command' >&2
    return 1
#endif
end
''')

_FISH_COMPLETE_FILEDIR = helpers.FishFunction('fish_complete_filedir', r'''
# Function for completing files or directories
#
# Options:
#   -d|--description=DESC   The description for completed entries
#   -c|--comp=STR           Complete STR instead of current command line argument
#   -D|--directories        Only complete directories
#   -C|--cd=DIR             List contents in DIR
#ifdef regex
#   -r|--regex=PATTERN      Only list files matching pattern
#endif
#
# This function is made out of /usr/share/fish/functions/__fish_complete_directories.fish

#ifdef regex
argparse --max-args 0 'd/description=' 'c/comp=' 'D/directories' 'C/cd=' 'r/regex=' -- $argv || return 1
#else
argparse --max-args 0 'd/description=' 'c/comp=' 'D/directories' 'C/cd=' -- $argv || return 1
#endif

set -l comp
set -l desc

if set -q _flag_description[1]
  set desc $_flag_description
else if set -g _flag_directories
  set desc 'Directory'
end

if set -q _flag_comp[1]
  set comp $_flag_comp
else
  set comp (commandline -ct | string replace -r -- '^-[^=]*=' '')
end

if set -q _flag_cd[1]
  pushd $_flag_cd 2>/dev/null || return 1
end

set -l files (complete -C"'' $comp")

if set -q _flag_cd[1]
  popd
end

if set -q files[1]
  if set -q _flag_directories[1]
    set files (printf '%s\n' $files | string match -r '.*/$')
  end
#ifdef regex

  if set -q _flag_regex[1]
    set files (printf '%s\n' $files | string match -rg "(.*/\$)|($_flag_regex[1])\$")
  end
#endif

  printf '%s\n' $files\t"$desc"
end
''')

_LIST_FILES = helpers.FishFunction('list_files', r'''
#ifdef regex
argparse --max-args 0 'D/directories' 'C/cd=' 'r/regex=' -- $argv || return 1
#else
argparse --max-args 0 'D/directories' 'C/cd=' -- $argv || return 1
#endif

set -l files

if set -q _flag_cd[1]
  pushd $_flag_cd 2>/dev/null || return 1
end

if set -q _flag_directories[1]
  set files */
else
  set files *
end

if set -q _flag_cd[1]
  popd
end

if set -q files[1]
#ifdef regex
  if set -q _flag_regex[1]
    set files (printf '%s\n' $files | string match -rg "(.*/\$)|($_flag_regex[1])\$")
  end

#endif
  printf '%s\n' $files
end
''')

_COMPLETE_LIST_UNIQ = helpers.FishFunction('complete_list_uniq', r'''
for comp in (__fish_complete_list $argv)
  set -l vals (string split -- $argv[1] (string split -m 1 -- \t $comp)[1])
  set -l last $vals[-1]
  set -e vals[-1]
  not contains $last $vals && printf "%s\n" $comp
end
''')

_HISTORY = helpers.FishFunction('history', r'''
builtin history | command grep -E -o -- $argv[1]
''')

_MIME_FILE = helpers.FishFunction('mime_file', r'''
set -l i_opt

set -l comp (commandline -ct | string replace -r -- '^-[^=]*=' '')

if command file -i /dev/null &>/dev/null
  set i_opt '-i'
else if command file -I /dev/null &>/dev/null
  set i_opt '-I'
else
  complete -C"'' $comp"
  return
end

set -l line
command file -L $i_opt -- "$comp"* 2>/dev/null | while read line
  set -l split (string split -m 1 -r ':' "$line")

  if string match -q -- '*inode/directory*' $split[2]
    printf '%s/\n' "$split[1]"
  else if begin; echo "$split[2]" | command grep -q -E -- $argv[1]; end
    printf '%s\n' "$split[1]"
  end
end
''')

_SUBSTRACT_PREFIX_SUFFIX = helpers.FishFunction('subtract_prefix_suffix', r'''
set -l s1 $argv[1]
set -l s2 $argv[2]

set -l len1 (string length -- $s1)
set -l len2 (string length -- $s2)

set -l maxk $len1
if test $len2 -lt $maxk
  set maxk $len2
end

set -l k $maxk
while test $k -gt 0
  set -l start (math $len1 - $k + 1)
  set -l suf (string sub -s $start -l $k -- $s1)
  set -l pre (string sub -s 1 -l $k -- $s2)

  if test "$suf" = "$pre"
    if test $len1 -eq $k
      echo ''
    else
      string sub -l (math $len1 - $k) -- $s1
    end
    return
  end

  set k (math $k - 1)
end

echo $s1
''')

_COMMANDLINE_STRING = helpers.FishFunction('commandline_string', r'''
set -l line
set -l comp (commandline -ct | string replace -r -- '^-[^=]*=' '')
set comp (string unescape -- "$comp")

complete -C "$comp" | while read line
  set -l split (string split -m 1 -- \t $line)
  set -l comp2 (subtract_prefix_suffix "$comp" "$split[1]")
  printf '%s\t%s\n' "$comp2$split[1]" "$split[2]"
end''', ['subtract_prefix_suffix'])

_DATE_FORMAT = helpers.FishFunction('date_format', r'''
set -l comp (commandline -ct | string replace -r -- '^-[^=]*=' '')

if test "$(string sub -s -1 -l 1 -- $comp)" = '%'
  printf '%s%s\t%s\n' \
    "$comp" 'a' 'abbreviated day name' \
    "$comp" 'A' 'full day name' \
    "$comp" 'b' 'abbreviated month name' \
    "$comp" 'h' 'abbreviated month name' \
    "$comp" 'B' 'full month name' \
    "$comp" 'c' 'preferred locale date and time' \
    "$comp" 'C' '2-digit century' \
    "$comp" 'd' 'day of month (01-31)' \
    "$comp" 'D' 'American format month/day/year (%m/%d/%y)' \
    "$comp" 'e' 'day of month ( 1-31)' \
    "$comp" 'F' 'ISO 8601 year-month-date (%Y-%m-%d)' \
    "$comp" 'G' '4-digit ISO 8601 week-based year' \
    "$comp" 'g' '2-digit ISO 8601 week-based year' \
    "$comp" 'H' 'hour (00-23)' \
    "$comp" 'I' 'hour (01-12)' \
    "$comp" 'j' 'day of year (001-366)' \
    "$comp" 'k' 'hour ( 0-23)' \
    "$comp" 'l' 'hour ( 1-12)' \
    "$comp" 'm' 'month (01-12)' \
    "$comp" 'M' 'minute (00-59)' \
    "$comp" 'n' 'newline' \
    "$comp" 'p' 'locale dependent AM/PM' \
    "$comp" 'r' 'locale dependent a.m. or p.m. time (%I:%M:%S %p)' \
    "$comp" 'R' '24-hour notation time (%H:%M)' \
    "$comp" 's' 'seconds since the epoch' \
    "$comp" 'S' 'seconds (00-60)' \
    "$comp" 't' 'tab' \
    "$comp" 'T' '24-hour notation with seconds (%H:%M:%S)' \
    "$comp" 'u' 'day of week (1-7, 1=Monday)' \
    "$comp" 'U' 'week number of current year, Sunday based (00-53)' \
    "$comp" 'V' 'ISO 8601 week number of current year, week 1 has 4 days in current year (01-53)' \
    "$comp" 'w' 'day of week (0-6, 0=Sunday)' \
    "$comp" 'W' 'week number of current year, Monday based (00-53)' \
    "$comp" 'x' 'locale dependent date representation without time' \
    "$comp" 'X' 'locale dependent time representation without date' \
    "$comp" 'y' '2-digit year (00-99)' \
    "$comp" 'Y' 'full year' \
    "$comp" 'z' 'UTC offset' \
    "$comp" 'Z' 'timezone name' \
    "$comp" '%' 'literal %'
end
''')

# =============================================================================
# Bonus
# =============================================================================

_NET_INTERFACES_LIST = helpers.FishFunction('net_interfaces_list', r'''
if test -d /sys/class/net
  command ls /sys/class/net
else if command ifconfig -l &>/dev/null
  command ifconfig -l # BSD / macOS
else
  command ifconfig 2>/dev/null | command awk '/^[a-z0-9]/ {print $1}' | command sed 's/://'
end''')

_TIMEZONE_LIST = helpers.FishFunction('timezone_list', r'''
if ! command timedatectl list-timezones 2>/dev/null
  command find /usr/share/zoneinfo -type f |\
  command sed 's|/usr/share/zoneinfo/||g'  |\
  command grep -E -v '^(posix|right)'
end''')

_ALSA_LIST_CARDS = helpers.FishFunction('alsa_list_cards', r'''
set -l card

for card in (command aplay -l | string match -r '^card [0-9]+: [^,]+')
  set card (string replace 'card ' '' $card)
  set -l split (string split ': ' $card)

  if set -q split[2]
    printf "%s\t%s\n" $split[1] $split[2]
  end
end''')

_ALSA_LIST_DEVICES = helpers.FishFunction('alsa_list_devices', r'''
set -l card

for card in (command aplay -l | string match -r '^card [0-9]+: [^,]+')
  set card (string replace 'card ' '' $card)
  set -l split (string split ': ' $card)

  if set -q split[2]
    printf "hw:%s\t%s\n" $split[1] $split[2]
  end
end''')


class FishHelpers(helpers.GeneralHelpers):
    '''Class holding helper functions for Fish.'''

    def __init__(self, function_prefix):
        super().__init__(function_prefix, helpers.FishFunction)
        self.add_function(_QUERY)
        self.add_function(_FISH_COMPLETE_FILEDIR)
        self.add_function(_LIST_FILES)
        self.add_function(_COMPLETE_LIST_UNIQ)
        self.add_function(_HISTORY)
        self.add_function(_DATE_FORMAT)
        self.add_function(_MIME_FILE)
        self.add_function(_SUBSTRACT_PREFIX_SUFFIX)
        self.add_function(_COMMANDLINE_STRING)
        self.add_function(_NET_INTERFACES_LIST)
        self.add_function(_TIMEZONE_LIST)
        self.add_function(_ALSA_LIST_CARDS)
        self.add_function(_ALSA_LIST_DEVICES)
