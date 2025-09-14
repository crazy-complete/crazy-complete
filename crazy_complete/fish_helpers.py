'''This module contains helper functions for Fish.'''

from . import helpers

_FISH_QUERY = helpers.FishFunction('fish_query', r'''
# ===========================================================================
#
# This function implements the parsing of options and positionals in the Fish shell.
#
# Usage: __fish_query <OPTIONS> <COMMAND> [ARGS...]
#
# The first argument is a comma-separated list of options that the parser should know about.
# Short options (-o), long options (--option), and old-style options (-option) are supported.
#
# If an option takes an argument, it is suffixed by '='.
# If an option takes an optional argument, it is suffixed by '=?'.
#
# For example:
#   __fish_query '-f,--flag,-old-style,--with-arg=,--with-optional=?' [...]
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
        set -a long_opts_with_arg (string replace -- '='  '' $option)
      else if string match -qr -- '^--.+=\?$' $option
        set -a long_opts_with_optional_arg (string replace -- '=?' '' $option)
      else if string match -qr -- '^--.+$' $option
        set -a long_opts_without_arg $option
#endif
#ifdef short_options
      else if string match -qr -- '^-.=$' $option
        set -a short_opts_with_arg (string replace -- '='  '' $option)
      else if string match -qr -- '^-.=\?$' $option
        set -a short_opts_with_optional_arg (string replace -- '=?' '' $option)
      else if string match -qr -- '^-.$' $option
        set -a short_opts_without_arg $option
#endif
#ifdef old_options
      else if string match -qr -- '^-..+=$' $option
        set -a old_opts_with_arg (string replace -- '='  '' $option)
      else if string match -qr -- '^-..+=\?$' $option
        set -a old_opts_with_optional_arg  (string replace -- '=?' '' $option)
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
      case '--'
        for argi in (seq (math $argi + 1) $cmdline_count)
          set -a positionals $cmdline[$argi]
        end
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
    end

    set argi (math $argi + 1)
  end

  set -g __QUERY_CACHE_POSITIONALS    $positionals
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
#
# This function is made out of /usr/share/fish/functions/__fish_complete_directories.fish

argparse --max-args 0 'd/description=' 'c/comp=' 'D/directories' 'C/cd=' -- $argv || return 1

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
  pushd $_flag_cd || return 1
end

set -l files (complete -C"'' $comp")

if set -q _flag_cd[1]
  popd
end

if set -q files[1]
  if set -q _flag_directories[1]
    set files (printf '%s\n' $files | string match -r '.*/$')
  end

  printf '%s\n' $files\t"$desc"
end
''')

class FishHelpers(helpers.GeneralHelpers):
    '''Class holding helper functions for Fish.'''

    def __init__(self, function_prefix):
        super().__init__(function_prefix)
        self.add_function(_FISH_QUERY)
        self.add_function(_FISH_COMPLETE_FILEDIR)
