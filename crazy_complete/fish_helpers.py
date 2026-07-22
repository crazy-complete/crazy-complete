# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2025-2026 Benjamin Abendroth <braph93@gmx.de>

'''This module contains helper functions for Fish.'''

from .helpers import GeneralHelpers, FishFunction

_QUERY_INIT = FishFunction('query_init', r'''
# ===========================================================================
#
# This function implements the parsing of options and positionals in the
# Fish shell.
#
# Usage: query_init COMMANDLINE_DEFINITION...
#
# COMMANDLINE DEFINITION
#   A command line definition has the format:
#      POSITIONAL_PATTERN=>OPTIONS
#
#   Definitions must be ordered from the least specific to the most specific
#   (global options first, then subcommand options).
#
# POSITIONAL PATTERN
#   The text before the '=>' is the positional pattern. An empty pattern
#   matches the top-level command. Subcommands inside the positional-pattern
#   are separated by '>'.
#
# OPTIONS
#   The text after the '=>' are the options for the command. Options
#   are separated by space.
#
# OPTION
#   Short options (-o), long options (--option), and old-style options (-option)
#   are supported.
#
#   If an option takes an argument, it is suffixed by '='.
#   If an option takes an optional argument, it is suffixed by '=?'.
#
# EXAMPLE
#   set -l opts \
#      '=>-f --flag -old-flag --with-arg= --with-optional=?' \
#      '(subcommand|subcmd)=>--choices=' \
#      '(subcommand|subcmd)>(subsub)=>--sub-sub-flag'
#
#   query_init $opts
#
#   Here, -f, --flag and -old-flag don't take options, --with-arg requires an
#   argument and --with-optional takes an optional argument.
#
#   If the first positional matches "subcommand" or "subcmd", --choices is
#   available as an option.
#
#   If, additionally, the seconds positional matches "subsub", --sub-sub-flag
#   is available as an option.
#
# ===========================================================================
#
set -l definitions $argv
set -l positionals
#ifdef positional_position
set -l positionals_positions
#endif
set -l having_options
set -l option_values
set -l last_arg_is_option_argument false

#ifdef subcommands
function %PREFIX%_match_positionals -S
  set -l patterns (string split -- '>' "$argv[1]")
  set -l i (count $patterns)

  while test $i -ge 1
    string match -q -r -- "^$patterns[$i]\$" "$positionals[$i]" || return 1
    set i (math $i - 1)
  end
end
#endif

function %PREFIX%_get_option -S
  set -l option $argv[1]
  set -l i (count $definitions)

  while test $i -ge 1
    set -l split (string split -m 1 -- '=>' $definitions[$i])
#ifdef subcommands
    if %PREFIX%_match_positionals "$split[1]"
#else
    if true
#endif
      set -l opt
      for opt in (string split -- ' ' $split[2])
        test "$opt" = "$option"   && begin echo '0'; return; end
        test "$opt" = "$option="  && begin echo '1'; return; end
        test "$opt" = "$option=?" && begin echo '?'; return; end
      end
    end

    set i (math $i - 1)
  end
end

set -l cmdline (commandline -poc)
set -l cmdline_count (count $cmdline)

set -l argi 2 # cmdline[1] is command name
while test $argi -le $cmdline_count
  set -l arg "$cmdline[$argi]"
  set -l have_trailing_arg (test $argi -lt $cmdline_count && echo true || echo false)

  switch $arg
    case '-'
      set -a positionals -
#ifdef positional_position
      set -a positionals_positions $argi
#endif
    case '--'
      set -a positionals $cmdline[$(math $argi + 1)..]
#ifdef positional_position
      set -a positionals_positions (seq (math $argi + 1) $cmdline_count)
#endif
      break
    case '--*=*'
      set -l split (string split -m 1 -- '=' $arg)
      set -a having_options $split[1]
      set -a option_values "$split[2]"
    case '--*'
#ifdef long_options
      set -l option_type (%PREFIX%_get_option $arg)
      if test "$option_type" = '1'
        if $have_trailing_arg
          set -a having_options $arg
          set -a option_values $cmdline[(math $argi + 1)]
          set argi (math $argi + 1)
        else
          set last_arg_is_option_argument true
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
        set -l option_type (%PREFIX%_get_option $split[1])
        if contains -- "$option_type" '1' '?'
          set -a having_options $split[1]
          set -a option_values "$split[2]"
          set end_of_parsing true
        end
      else
        set -l option_type (%PREFIX%_get_option $arg)
        if test "$option_type" = '1'
          set end_of_parsing true
          if $have_trailing_arg
            set -a having_options $arg
            set -a option_values $cmdline[(math $argi + 1)]
            set argi (math $argi + 1)
          else
            set last_arg_is_option_argument true
          end
        else if contains -- "$option_type" '0' '?'
          set -a having_options $arg
          set -a option_values ''
          set end_of_parsing true
        end
      end
#endif
#ifdef short_options

      set -l arg_length (string length -- $arg)
      set -l i 2
      while not $end_of_parsing; and test $i -le $arg_length
        set -l option "-$(string sub -s $i -l 1 -- $arg)"
        set -l trailing_chars "$(string sub -s (math $i + 1) -- $arg)"
        set -l option_type (%PREFIX%_get_option $option)

        if test "$option_type" = '0'
          set -a having_options $option
          set -a option_values ''
        else if test "$option_type" = '1'
          set end_of_parsing true

          if test -n "$trailing_chars"
            set -a having_options $option
            set -a option_values $trailing_chars
          else if $have_trailing_arg
            set -a having_options $option
            set -a option_values $cmdline[(math $argi + 1)]
            set argi (math $argi + 1)
          else
            set last_arg_is_option_argument true
          end
        else if test "$option_type" = '?'
          set end_of_parsing true
          set -a having_options $option
          set -a option_values "$trailing_chars" # may be empty
        end

        set i (math $i + 1)
      end
#endif
    case '*'
      set -a positionals $arg
#ifdef positional_position
      set -a positionals_positions $argi
#endif
  end

  set argi (math $argi + 1)
end

set -g __QUERY_CACHE_POSITIONALS    $positionals
#ifdef positional_position
set -g __QUERY_CACHE_POSITIONALS_POSITIONS $positionals_positions
#endif
set -g __QUERY_CACHE_HAVING_OPTIONS $having_options
set -g __QUERY_CACHE_OPTION_VALUES  $option_values

set -l cmdline_last_arg (commandline -ct | string unescape)
set -g __QUERY_CACHE_CURRENT_ARG $cmdline_last_arg

$last_arg_is_option_argument && return

set -l split (string split -m1 -- '=' $cmdline_last_arg)
# `string split` returns 0 if it did split the string
if test $status -eq 0 && contains -- (%PREFIX%_get_option $split[1]) '1' '?'
  set -g __QUERY_CACHE_CURRENT_ARG $split[2]
  return
end
#ifdef short_options

set -l arg_length (string length -- $cmdline_last_arg)
set -l i 2
while test $i -le $arg_length
  set -l option "-$(string sub -s $i -l 1 -- $cmdline_last_arg)"
  if contains -- (%PREFIX%_get_option $option) '1' '?'
    set -g __QUERY_CACHE_CURRENT_ARG (string sub -s (math $i + 1) -- $cmdline_last_arg)
    return
  end

  set i (math $i + 1)
end
#endif
''')

_POSITIONAL_CONTAINS = FishFunction('positional_contains', r'''
# positional_contains [-i] <NUM> <WORDS>
#
# Checks if the positional argument number NUM is one of WORDS.
# NUM counts from one.
#
#ifdef nocase
set -l nocase false
if test "$argv[1]" = -i; set nocase true; set -e argv[1]; end

#endif
#ifdef DEBUG
if test (count $argv) -eq 0
  echo '%FUNCNAME%: missing number' >&2
  return 1
end

#endif
set -l positional_num $argv[1]
set -e argv[1]
#ifdef nocase
if $nocase
  contains -- (string lower -- $__QUERY_CACHE_POSITIONALS[$positional_num] $argv)
else
  contains -- $__QUERY_CACHE_POSITIONALS[$positional_num] $argv
end
#else
contains -- $__QUERY_CACHE_POSITIONALS[$positional_num] $argv
#endif
''', ['query_init'])

_HAS_OPTION = FishFunction('has_option', r'''
# has_option [WITH_INCOMPLETE] <OPTIONS>
#
# Checks if an option given in OPTIONS is passed on commandline.
# If an option requires an argument, this command returns true only if the
# option includes an argument. If 'WITH_INCOMPLETE' is specified, it also
# returns true for options missing their arguments.
#
set -l option
#ifdef with_incomplete
set -l with_incomplete false

if test $argv[1] = 'WITH_INCOMPLETE'
  set with_incomplete true
  set -e argv[1]
end

#endif
for option in $__QUERY_CACHE_HAVING_OPTIONS
  contains -- $option $argv && return 0
end

#ifdef with_incomplete
if $with_incomplete
  set -l tokens (commandline -po)
  set -e tokens[1]
  for option in $argv
    if test 2 -eq (string length -- $option)
      set option (string sub -l 1 -s 2 -- $option)
      string match -rq -- "^-[A-z0-9]*$option\$"   $tokens[-2] && return 0
      string match -rq -- "^-[A-z0-9]*$option.*\$" $tokens[-1] && return 0
    else
      string match -q -r -- "^$option\$"       $tokens[-2] && return 0
      string match -q -r -- "^$option(=.*)?\$" $tokens[-1] && return 0
      contains -- $tokens[-1] $argv && return 0
    end
  end
end

#endif
return 1
''', ['query_init'])

_OPTION_IS = FishFunction('option_is', r'''
# option_is [-a] [-i] -- <OPTIONS...> -- <VALUES...>
#
# Checks if any option in OPTIONS has a value of VALUES.
#
#ifdef any
set -l any false
#endif
#ifdef nocase
set -l nocase false
#endif

while set -q argv[1]
#ifdef any
  if test "$argv[1]" = -a; set any true; set -e argv[1]; continue; end
#endif
#ifdef nocase
  if test "$argv[1]" = -i; set nocase true; set -e argv[1]; continue; end
#endif
  if test "$argv[1]" = --; set -e argv[1]; break; end
end

set -l eof_string (contains -i -- -- $argv || math (count $argv) + 1)
set -l options $argv[1..$(math $eof_string - 1)]
set -l values $argv[$(math $eof_string + 1)..]
#ifdef nocase
set -l option_values $__QUERY_CACHE_OPTION_VALUES
$nocase && set values (string lower -- $values)
$nocase && set option_values (string lower -- $option_values)
#endif

#ifdef DEBUG
if test (count $options) -eq 0
  echo '%FUNCNAME%: missing options' >&2
  return 1
end

if test (count $values) -eq 0
  echo '%FUNCNAME%: missing values' >&2
  return 1
end

#endif
set -l i (count $__QUERY_CACHE_HAVING_OPTIONS)
while test $i -ge 1
  if contains -- $__QUERY_CACHE_HAVING_OPTIONS[$i] $options
#ifdef nocase
    contains -- $option_values[$i] $values && return 0
#else
    contains -- $__QUERY_CACHE_OPTION_VALUES[$i] $values && return 0
#endif
#ifdef any
    $any || return 1
#else
    return 1
#endif
  end

  set i (math $i - 1)
end

return 1
''', ['query_init'])

_OPTION_MATCH = FishFunction('option_match', r'''
# option_match [-a] [-i] -- <OPTIONS...> -- <REGEX>
#
# Checks if any option in OPTIONS has a value that matches REGEX.
#
#ifdef any
set -l any false
#endif
#ifdef nocase
set -l nocase ''
#endif

while set -q argv[1]
#ifdef any
  if test "$argv[1]" = -a; set any true; set -e argv[1]; continue; end
#endif
#ifdef nocase
  if test "$argv[1]" = -i; set nocase i; set -e argv[1]; continue; end
#endif
  if test "$argv[1]" = --; set -e argv[1]; break; end
end

set -l eof_string (contains -i -- -- $argv || math (count $argv) + 1)
set -l options $argv[1..$(math $eof_string - 1)]
set -l regex $argv[(math $eof_string + 1)]

#ifdef DEBUG
if test (count $options) -eq 0
  echo '%FUNCNAME%: missing options' >&2
  return 1
end

if test (count $regex) -eq 0
  echo '%FUNCNAME%: missing regex' >&2
  return 1
end

#endif
set -l i (count $__QUERY_CACHE_HAVING_OPTIONS)
while test $i -ge 1
  if contains -- $__QUERY_CACHE_HAVING_OPTIONS[$i] $options
#ifdef nocase
    string match -rq$nocase -- $regex $__QUERY_CACHE_OPTION_VALUES[$i] && return 0
#else
    string match -rq -- $regex $__QUERY_CACHE_OPTION_VALUES[$i] && return 0
#endif
#ifdef any
    $any || return 1
#else
    return 1
#endif
  end

  set i (math $i - 1)
end

return 1
''', ['query_init'])

_NUM_OF_POSITIONALS = FishFunction('num_of_positionals', r'''
# num_of_positionals [<OPERATOR> <NUMBER>]
#
# If no arguments are provided, print the count of positional arguments.
#
# If two arguments are provided, the first argument should be one of
# the comparison operators: '-lt', '-le', '-eq', '-ne', '-gt', '-ge'.
# Returns 0 if the count of positional arguments matches the
# specified NUMBER according to the comparison operator, otherwise
# returns 1.
#
switch (count $argv)
  case 0
    count $__QUERY_CACHE_POSITIONALS
#ifdef DEBUG
  case 1
    echo '%FUNCNAME%: $argv[1]: missing operand' >&2
    return 1
#endif
  case 2
#ifdef DEBUG
    if not contains -- $argv[1] -lt -le -eq -ne -gt -ge;
      echo '%FUNCNAME%: $argv[1]: unknown operator' >&2
      return 1
    end
#endif
    test (count $__QUERY_CACHE_POSITIONALS) $argv[1] $argv[2] && return 0 || return 1
#ifdef DEBUG
  case '*'
    echo '%FUNCNAME%: too many arguments' >&2
    return 1
#endif
end
''', ['query_init'])

_POSITIONAL_POSITION = FishFunction('positional_position', r'''
# positional_position <POSITIONAL_NUMBER>
#
# Prints the command-line index of the specified positional argument.
#
echo $__QUERY_CACHE_POSITIONALS_POSITIONS[$argv[1]]
''', ['query_init'])

_CAPTURE_OPTION = FishFunction('capture_option', r'''
# capture_option <VARIABLE> <OPTIONS>
#
# Stores all values supplied to OPTIONS in VARIABLE.
# VARIABLE is global.
#
set -l variable $argv[1]
set -l options $argv[2..]
set -l values
set -l i 1

while test $i -le (count $__QUERY_CACHE_HAVING_OPTIONS)
  if contains -- $__QUERY_CACHE_HAVING_OPTIONS[$i] $options
    set -a values $__QUERY_CACHE_OPTION_VALUES[$i]
  end

  set i (math $i + 1)
end

set -g $variable $values
''', ['query_init'])

_GET_COMPLETING_ARG = FishFunction('get_completing_arg', r'''
if test -n "$__fish_stripprefix"
  string replace -r -- $__fish_stripprefix '' "$__QUERY_CACHE_CURRENT_ARG"
else
  printf '%s\n' "$__QUERY_CACHE_CURRENT_ARG"
end
''')

_FILEDIR = FishFunction('filedir', r'''
# Function for completing files or directories
#
# Options:
#   -d|--description=DESC   The description for completed entries
#   -D|--directories        Only complete directories
#   -C|--cd=DIR             List contents in DIR
#ifdef regex
#   -r|--regex=PATTERN      Only list files matching pattern
#endif
#ifdef regex_ignore
#   -i|--ignore=PATTERN     Ignore files matching pattern
#endif

argparse --max-args 0 'd/description=' 'D/directories' 'C/cd=' \
#ifdef regex
    'r/regex=' \
#endif
#ifdef regex_ignore
    'i/ignore=' \
#endif
    -- $argv || return 1

set -l comp (get_completing_arg)
set -l desc
set -l files

if set -q _flag_cd[1]
  pushd $_flag_cd 2>/dev/null || return 1
  set files (complete -C"'' $comp")
  popd
else
  set files (complete -C"'' $comp")
end

if set -q _flag_description[1]
  set desc $_flag_description
else if set -g _flag_directories
  set desc 'Directory'
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
#ifdef regex_ignore

  if set -q _flag_ignore[1]
    set files (printf '%s\n' $files | string match -rv "(^|.*/)($_flag_ignore[1])\$")
  end
#endif

  printf '%s\n' $files\t"$desc"
end
''', ['get_completing_arg'])

_LIST = FishFunction('list', r'''
set -l duplicates false

if test $argv[1] = '-d'
  set duplicates true
  set -e argv[1]
end

set -l separator $argv[1]
set -l func $argv[2]
set -l comp (get_completing_arg)

if test -z "$comp"
  eval $func
  return
end

set -l i
set -l value
set -l values
set -l descriptions

set -g __fish_stripprefix "^.*"(string escape --style=regex -- $separator)

for value in (eval $func)
  set -l split (string split -- \t $value)
  set -a values $split[1]
  set -a descriptions "$split[2]"
end

set -e __fish_stripprefix

set -l having_values (string split -- $separator $comp)
set -l remaining_values_idxs

if $duplicates
  set remaining_values_idxs (seq 1 (count $values))
else
  set i 1
  for value in $values
    if not contains -- $value $having_values
      set -a remaining_values_idxs $i
    end

    set i (math $i + 1)
  end
end

switch $comp
  case "*$separator"
    for i in $remaining_values_idxs
      printf '%s%s\t%s\n' $comp $values[$i] "$descriptions[$i]"
    end
  case "*$separator*"
    set comp (string split -r -m 1 -- $separator $comp)[1]

    for i in $remaining_values_idxs
      printf '%s%s%s\t%s\n' "$comp" $separator $values[$i] "$descriptions[$i]"
    end
  case '*'
    for i in $remaining_values_idxs
      printf '%s\t%s\n' $values[$i] "$descriptions[$i]"
    end
end
''', ['get_completing_arg'])

_PREFIX = FishFunction('prefix', r'''
set -l comp (get_completing_arg)
set -l prefix_escaped (string escape --style=regex -- $argv[1])
if string match -qr -- $prefix_escaped $comp
  set -g __fish_stripprefix "^"$prefix_escaped
  printf "%s\n" $argv[1](eval $argv[2])
  set -e __fish_stripprefix
else
  printf "%s\n" $argv[1]
end
''', ['get_completing_arg'])

_KEY_VALUE_LIST = FishFunction('key_value_list', r'''
set -l sep1 $argv[1]
set -l sep2 $argv[2]
set -l value
set -l keys
set -l descriptions
set -l functions
set -l excludes
set -l i

for i in (seq 3 4 (count $argv))
  set -a keys $argv[$i]
  set -a descriptions $argv[(math $i + 1)]
  set -a functions $argv[(math $i + 2)]
  set -a excludes $argv[(math $i + 3)]
end

set -l comp (get_completing_arg)
set -l remaining (seq 1 (count $keys))
set -l pairs (string split -- $sep1 $comp)
set -l pair

for pair in $pairs
  set -l split (string split -m1 -- $sep2 $pair)
  set i (contains -i -- $split[1] $keys)

  if test $status -eq 0
    set -l exclude
    for exclude in (string split -- ' ' $excludes[$i])
      set i (contains -i -- $exclude $keys)
      if test $status -eq 0
        set remaining (string match -v $i -- $remaining)
      end
    end
  end
end

if test -z "$comp" || test (string sub -s -1 -l 1 -- $comp) = $sep1
  for i in $remaining
    if test "$functions[$i]" = false
      printf '%s%s\t%s\n' "$comp" $keys[$i] "$descriptions[$i]"
    else
      printf '%s%s%s\t%s\n' "$comp" $keys[$i] $sep2 "$descriptions[$i]"
    end
  end
  return
end

function %PREFIX%__call_func_for_key -S
  set -l i
  for i in (seq 1 (count $keys))
    if test $keys[$i] = $argv[1]
      set -g __fish_stripprefix "^.*"(string escape --style=regex -- $sep2)
      $functions[$i]
      set -e __fish_stripprefix
      return
    end
  end
end

set -l pair $pairs[-1]
set -l split (string split -m1 -- $sep2 $pair)

switch $pair
  case "*$sep2*"
    set -l value_len (string length -- $split[2])

    if test $value_len -gt 0
      set comp (string sub -e -$value_len -- $comp)
    end

    for value in (%PREFIX%__call_func_for_key $split[1])
      printf '%s%s\n' $comp $value
    end
  case '*'
    set -l key_len (string length -- $split[1])
    set comp (string sub -e -$key_len -- $comp)

    for i in $remaining
      if test "$functions[$i]" = false
        printf '%s%s\t%s\n' "$comp" $keys[$i] "$descriptions[$i]"
      else
        printf '%s%s%s\t%s\n' "$comp" $keys[$i] $sep2 "$descriptions[$i]"
      end
    end
end
''', ['get_completing_arg'])

_KEY_VALUE_PAIR = FishFunction('key_value_pair', r'''
set -l sep $argv[1]
set -l keys
set -l descriptions
set -l functions
set -l i

for i in (seq 2 3 (count $argv))
  set -a keys $argv[$i]
  set -a descriptions $argv[(math $i + 1)]
  set -a functions $argv[(math $i + 2)]
end

function %PREFIX%__call_func_for_key -S
  set -l i
  for i in (seq 1 (count $keys))
    if test $keys[$i] = $argv[1]
      set -g __fish_stripprefix "^.*"(string escape --style=regex -- $sep)
      $functions[$i]
      set -e __fish_stripprefix
      return
    end
  end
end

set -l comp (get_completing_arg)
set -l split (string split -m1 -- $sep $comp)

if test (count $split) -eq 2
  set -l value
  for value in (%PREFIX%__call_func_for_key $split[1])
    printf '%s%s%s\n' $split[1] $sep $value
  end
else
  for i in (seq 1 (count $keys))
    if test "$functions[$i]" = false
      printf '%s\t%s\n' $keys[$i] "$descriptions[$i]"
    else
      printf '%s%s\t%s\n' $keys[$i] $sep "$descriptions[$i]"
    end
  end
end
''', ['get_completing_arg'])

_KEY_VALUE_PAIR_EXEC = FishFunction('key_value_pair_exec', r'''
set -l sep $argv[1]
set -l func $argv[2]
set -l comp (get_completing_arg)
set -l split (string split -m1 -- $sep $comp)

if test (count $split) -eq 2
  set -l value
  set -g __fish_stripprefix "^.*"(string escape --style=regex -- $sep)
  for value in ($func $split[1])
    printf '%s%s%s\n' $split[1] $sep $value
  end
  set -e __fish_stripprefix
else
  $func
end
''', ['get_completing_arg'])

_KEY_VALUE_LIST_EXEC = FishFunction('key_value_list_exec', r'''
set -l sep1 $argv[1]
set -l sep2 $argv[2]
set -l func $argv[3]
set -l comp (get_completing_arg)
set -l pairs (string split -- $sep1 $comp)

set -l keys
set -l descriptions
set -l takes_arg
set -l excludes

set -l line
set -l i

for line in ($func)
  set -l split (string split -- \t $line)
  set -l key $split[1]
  set -l non_repeatable_exclude ''

  if string match -qr -- '=$' $key
    set key (string sub -e -1 -- $key)
    set -a takes_arg true
  else if string match -qr -- '=\?$' $key
    set key (string sub -e -2 -- $key)
    set -a takes_arg false
  else
    set -a takes_arg false
  end

  if string match -q -- '\**' $key
    set key (string sub -s 2 -- $key)
  else
    set non_repeatable_exclude " $key"
  end

  set -a keys $key
  set -a descriptions $split[2]
  set -a excludes "$split[3]$non_repeatable_exclude"
end

set -l remaining (seq 1 (count $keys))

set -l pair
for pair in $pairs
  set -l split (string split -m1 -- $sep2 $pair)
  set i (contains -i -- $split[1] $keys)

  if test $status -eq 0
    set -l exclude
    for exclude in (string split -n -- ' ' $excludes[$i])
      set i (contains -i -- $exclude $keys)
      if test $status -eq 0
        set remaining (string match -v $i -- $remaining)
      end
    end
  end
end

if test -z "$comp" || test (string sub -s -1 -l 1 -- $comp) = $sep1
  for i in $remaining
    if test "$takes_arg[$i]" = false
      printf '%s%s\t%s\n' "$comp" $keys[$i] "$descriptions[$i]"
    else
      printf '%s%s%s\t%s\n' "$comp" $keys[$i] $sep2 "$descriptions[$i]"
    end
  end
  return
end

set -l pair $pairs[-1]
set -l split (string split -m1 -- $sep2 $pair)

switch $pair
  case "*$sep2*"
    set -l value_len (string length -- $split[2])

    if test $value_len -gt 0
      set comp (string sub -e -$value_len -- $comp)
    end

    set -g __fish_stripprefix "^.*"(string escape --style=regex -- $sep)
    for value in ($func $split[1])
      printf '%s%s\n' $comp $value
    end
    set -e __fish_stripprefix
  case '*'
    set -l key_len (string length -- $split[1])
    set comp (string sub -e -$key_len -- $comp)

    for i in $remaining
      if test "$takes_arg[$i]" = false
        printf '%s%s\t%s\n' "$comp" $keys[$i] "$descriptions[$i]"
      else
        printf '%s%s%s\t%s\n' "$comp" $keys[$i] $sep2 "$descriptions[$i]"
      end
    end
end
''', ['get_completing_arg'])

_HISTORY = FishFunction('history', r'''
builtin history | command grep -E -o -- $argv[1]
''')

_MIME_FILE = FishFunction('mime_file', r'''
set -l i_opt

set -l comp (get_completing_arg)

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
''', ['get_completing_arg'])

_SUBSTRACT_PREFIX_SUFFIX = FishFunction('subtract_prefix_suffix', r'''
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

_COMMANDLINE_STRING = FishFunction('commandline_string', r'''
set -l line
set -l comp (get_completing_arg)

complete -C "$comp" | while read line
  set -l split (string split -m 1 -- \t $line)
  set -l comp2 (subtract_prefix_suffix "$comp" "$split[1]")
  printf '%s\t%s\n' "$comp2$split[1]" "$split[2]"
end''', ['subtract_prefix_suffix', 'get_completing_arg'])

_DATE_FORMAT = FishFunction('date_format', r'''
set -l comp (get_completing_arg)

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
''', ['get_completing_arg'])

_NUMBER = FishFunction('number', r'''
set -l comp (get_completing_arg)
set -l number (string match -r -- '^[0-9,.]*' $comp)

if test -z "$number"
  return
end

set -l suffix_and_desc
for suffix_and_desc in $argv
  set suffix_and_desc (string split -m 1 -- ':' $suffix_and_desc)
  printf '%s%s\t%s\n' $number $suffix_and_desc[1] $suffix_and_desc[2]
end
''', ['get_completing_arg'])

# =============================================================================
# Bonus
# =============================================================================

_TIMEZONE_LIST = FishFunction('timezone_list', r'''
if ! command timedatectl list-timezones 2>/dev/null
  command find /usr/share/zoneinfo -type f |\
  command sed 's|/usr/share/zoneinfo/||g'  |\
  command grep -E -v '^(posix|right)'
end
''')

_ALSA_LIST_CARDS = FishFunction('alsa_list_cards', r'''
set -l card

for card in (command aplay -l | string match -r '^card [0-9]+: [^,]+')
  set card (string replace 'card ' '' $card)
  set -l split (string split ': ' $card)

  if set -q split[2]
    printf "%s\t%s\n" $split[1] $split[2]
  end
end
''')

_ALSA_LIST_DEVICES = FishFunction('alsa_list_devices', r'''
set -l card

for card in (command aplay -l | string match -r '^card [0-9]+: [^,]+')
  set card (string replace 'card ' '' $card)
  set -l split (string split ': ' $card)

  if set -q split[2]
    printf "hw:%s\t%s\n" $split[1] $split[2]
  end
end
''')


class FishHelpers(GeneralHelpers):
    '''Class holding helper functions for Fish.'''

    def __init__(self, config, function_prefix):
        super().__init__(config, function_prefix, FishFunction)
        self.add_function(_QUERY_INIT)
        self.add_function(_POSITIONAL_CONTAINS)
        self.add_function(_HAS_OPTION)
        self.add_function(_OPTION_IS)
        self.add_function(_OPTION_MATCH)
        self.add_function(_NUM_OF_POSITIONALS)
        self.add_function(_POSITIONAL_POSITION)
        self.add_function(_CAPTURE_OPTION)

        self.add_function(_GET_COMPLETING_ARG)
        self.add_function(_FILEDIR)
        self.add_function(_LIST)
        self.add_function(_PREFIX)
        self.add_function(_KEY_VALUE_LIST)
        self.add_function(_KEY_VALUE_PAIR)
        self.add_function(_KEY_VALUE_LIST_EXEC)
        self.add_function(_KEY_VALUE_PAIR_EXEC)
        self.add_function(_HISTORY)
        self.add_function(_DATE_FORMAT)
        self.add_function(_NUMBER)
        self.add_function(_MIME_FILE)
        self.add_function(_SUBSTRACT_PREFIX_SUFFIX)
        self.add_function(_COMMANDLINE_STRING)
        self.add_function(_TIMEZONE_LIST)
        self.add_function(_ALSA_LIST_CARDS)
        self.add_function(_ALSA_LIST_DEVICES)
