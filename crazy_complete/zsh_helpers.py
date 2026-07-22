# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2025-2026 Benjamin Abendroth <braph93@gmx.de>

'''This module contains helper functions for Zsh.'''

from .helpers import GeneralHelpers, ShellFunction


_QUERY = ShellFunction('query', r'''
# ===========================================================================
#
# This function is for querying the command line.
#
# COMMANDS
#   init <OPTIONS> <ARGS...>
#     This is the first call you have to make, otherwise the other commands
#     won't (successfully) work.
#
#     It parses <ARGS> according to <OPTIONS> and stores results in the
#     variables POSITIONALS, HAVING_OPTIONS and OPTION_VALUES.
#
#     The first argument is a comma-separated list of options that the parser
#     should know about. Short options (-o), long options (--option), and
#     old-style options (-option) are supported.
#
#     If an option takes an argument, it is suffixed by '='.
#     If an option takes an optional argument, it is suffixed by '=?'.
#
#   get_positional <NUM>
#     Prints out the positional argument number NUM (starting from 1)
#
#   has_option [WITH_INCOMPLETE] <OPTIONS...>
#     Checks if an option given in OPTIONS is passed on commandline.
#     If an option requires an argument, this command returns true only if the
#     option includes an argument. If 'WITH_INCOMPLETE' is specified, it also
#     returns true for options missing their arguments.
#
#   option_is [-a] [-i] -- <OPTIONS...> -- <VALUES...>
#     Checks if one option in OPTIONS has a value of VALUES.
#
# EXAMPLE
#   local POSITIONALS HAVING_OPTIONS OPTION_VALUES
#   query init '-f,-a=,-optional=?' program_name -f -optional -a foo bar
#   query has_option -f
#   query option_is -- -a -- foo
#
#   Here, -f is a flag, -a takes an argument, and -optional takes an optional
#   argument.
#
#   Both queries return true.
#
# ===========================================================================

local cmd="$1"; shift

case "$cmd" in
#ifdef get_positional
  get_positional)
#ifdef DEBUG
    if (( $# != 1 )); then
      echo "%FUNCNAME%: get_positional: takes exactly one argument" >&2
      return 1
    fi

    if test "$1" -eq 0; then
      echo "%FUNCNAME%: get_positional: positionals start at 1, not 0!" >&2
      return 1
    fi

#endif
    printf "%s" "${POSITIONALS[$1]}"
    return 0;;
#endif
#ifdef get_option
  get_option)
    local i=0

#ifdef DEBUG
    if (( $# == 0 )); then
      echo "%FUNCNAME%: get_option: arguments required" >&2
      return 1
    fi

#endif
    for (( i=0; i <= ${#HAVING_OPTIONS[@]}; ++i )); do
      local option="${HAVING_OPTIONS[$i]}"
      if array_contains "$option" "$@"; then
        printf "%s\n" "${OPTION_VALUES[$i]}"
      fi
    done

    return 0;;
#endif
#ifdef has_option
  has_option)
#ifdef with_incomplete
    local option='' with_incomplete=0
    [[ "$1" == 'WITH_INCOMPLETE' ]] && { with_incomplete=1; shift; }
#else
    local option=''
#endif

#ifdef DEBUG
    if (( $# == 0 )); then
      echo "%FUNCNAME%: has_option: arguments required" >&2
      return 1
    fi

#endif
    for option in "${HAVING_OPTIONS[@]}"; do
      array_contains "$option" "$@" && return 0
    done

#ifdef with_incomplete
    (( with_incomplete )) && \
      array_contains "$INCOMPLETE_OPTION" "$@" && return 0

#endif
    return 1;;
#endif
#ifdef option_is
  option_is)
    local i=0 dash_dash_pos=0 cmd_option_is_options=() cmd_option_is_values=()
    local nocase=0 any=0

    while (( $# )); do
#ifdef any
      [[ "$1" == "-a" ]] && { any=1; shift; continue; }
#endif
#ifdef nocase
      [[ "$1" == "-i" ]] && { nocase=1; shift; continue; }
#endif
      [[ "$1" == "--" ]] && { shift; break; }
    done

    dash_dash_pos=${@[(i)--]}
    cmd_option_is_options=("${@:1:$((dash_dash_pos - 1))}")
    cmd_option_is_values=("${@:$((dash_dash_pos + 1))}")
#ifdef nocase
    (( nocase )) && cmd_option_is_values=("${(L)cmd_option_is_values[@]}")
#endif

#ifdef DEBUG
    if (( ${#cmd_option_is_options[@]} == 0 )); then
      echo "%FUNCNAME%: option_is: missing options" >&2
      return 1
    fi

    if (( ${#cmd_option_is_values[@]} == 0 )); then
      echo "%FUNCNAME%: option_is: missing values" >&2
      return 1
    fi

#endif
    for (( i=${#HAVING_OPTIONS[@]}; i > 0; --i )); do
      if array_contains "${HAVING_OPTIONS[$i]}" "${cmd_option_is_options[@]}"; then
        local value="${OPTION_VALUES[$i]}"
#ifdef nocase
        (( nocase )) && value="${(L)value}"
#endif
        array_contains "$value" "${cmd_option_is_values[@]}" && return 0
#ifdef any
        (( any )) || return 1
#else
        return 1
#endif
      fi
    done

    return 1;;
#endif
  init)
    local -a options=(${=1})
    shift;;
  *)
    echo "%FUNCNAME%: argv[1]: invalid command" >&2
    return 1;;
esac

# continuing init...

# ===========================================================================
# Parsing of available options
# ===========================================================================

#ifdef old_options
local   old_opts_with_arg=()   old_opts_with_optional_arg=()   old_opts_without_arg=()
#endif
#ifdef long_options
local  long_opts_with_arg=()  long_opts_with_optional_arg=()  long_opts_without_arg=()
#endif
#ifdef short_options
local short_opts_with_arg=() short_opts_with_optional_arg=() short_opts_without_arg=()
#endif

local option=''
for option in "${options[@]}"; do
  case "$option" in
#ifdef long_options
    --?*=)    long_opts_with_arg+=("${option%=}");;
    --?*=\?)  long_opts_with_optional_arg+=("${option%=?}");;
    --?*)     long_opts_without_arg+=("$option");;
#endif
#ifdef short_options
    -?=)      short_opts_with_arg+=("${option%=}");;
    -?=\?)    short_opts_with_optional_arg+=("${option%=?}");;
    -?)       short_opts_without_arg+=("$option");;
#endif
#ifdef old_options
    -??*=)    old_opts_with_arg+=("${option%=}");;
    -??*=\?)  old_opts_with_optional_arg+=("${option%=?}");;
    -??*)     old_opts_without_arg+=("$option");;
#endif
#ifdef DEBUG
    *) echo "%FUNCNAME%: $option: not a valid short, long or oldstyle option" >&2; return 1;;
#endif
  esac
done

# ===========================================================================
# Parsing of command line options
# ===========================================================================

POSITIONALS=()
HAVING_OPTIONS=()
OPTION_VALUES=()
INCOMPLETE_OPTION=''

local args=("${(Q)@}")
local argi=2 # argi[1] is program name
for ((; argi <= ${#args[@]}; ++argi)); do
  local arg="${args[$argi]}"
  local have_trailing_arg=$(test $argi -lt $# && echo true || echo false)

  case "$arg" in
    --)
      POSITIONALS+=("${@:$((argi + 1))}")
      break;;
    --*=*)
      HAVING_OPTIONS+=("${arg%%=*}")
      OPTION_VALUES+=("${arg#*=}");;
    --*)
#ifdef long_options
      if array_contains "$arg" "${long_opts_with_arg[@]}"; then
        if $have_trailing_arg; then
          HAVING_OPTIONS+=("$arg")
          OPTION_VALUES+=("${args[$((++argi))]}")
#ifdef with_incomplete
        else
          INCOMPLETE_OPTION="$arg"
#endif
        fi
      else
        HAVING_OPTIONS+=("$arg")
        OPTION_VALUES+=("")
      fi
#endif
      ;;
    -?*) # ignore '-'
#ifdef old_options
      if [[ "$arg" == *=* ]]; then
        local option="${arg%%=*}" value="${arg#*=}"
        if array_contains "$option" "${old_opts_with_arg[@]}" "${old_opts_with_optional_arg[@]}"; then
          HAVING_OPTIONS+=("$option")
          OPTION_VALUES+=("$value")
          continue
        fi
      elif array_contains "$arg" "${old_opts_with_arg[@]}"; then
        if $have_trailing_arg; then
          HAVING_OPTIONS+=("$arg")
          OPTION_VALUES+=("${args[$((++argi))]}")
#ifdef with_incomplete
        else
          INCOMPLETE_OPTION="$arg"
#endif
        fi
        continue
      elif array_contains "$arg" "${old_opts_without_arg[@]}" "${old_opts_with_optional_arg[@]}"; then
        HAVING_OPTIONS+=("$arg")
        OPTION_VALUES+=("")
        continue
      fi
#endif

#ifdef short_options
      local i=1 arg_length=${#arg}
      for ((; i < arg_length; ++i)); do
        local option="-${arg:$i:1}"
        local trailing_chars="${arg:$((i+1))}"

        if array_contains "$option" "${short_opts_without_arg[@]}"; then
          HAVING_OPTIONS+=("$option")
          OPTION_VALUES+=("")
        elif array_contains "$option" "${short_opts_with_arg[@]}"; then
          if [[ -n "$trailing_chars" ]]; then
            HAVING_OPTIONS+=("$option")
            OPTION_VALUES+=("$trailing_chars")
          elif $have_trailing_arg; then
            HAVING_OPTIONS+=("$option")
            OPTION_VALUES+=("${args[$((++argi))]}")
#ifdef with_incomplete
          else
            INCOMPLETE_OPTION="$option"
#endif
          fi

          continue 2
        elif array_contains "$option" "${short_opts_with_optional_arg[@]}"; then
          HAVING_OPTIONS+=("$option")
          OPTION_VALUES+=("$trailing_chars") # may be empty
          continue 2
        fi
      done
#endif
      ;;
    *)
      POSITIONALS+=("$arg");;
  esac
done
''', ['array_contains'])

_ARRAY_CONTAINS = ShellFunction('array_contains', r'''
local arg='' key="$1"; shift
for arg; do [[ "$key" == "$arg" ]] && return 0; done
return 1
''')

_OPTION_MATCH = ShellFunction('option_match', r'''
local i=0 dash_dash_pos=0 options=() regex='' nocase=0 any=0

while (( $# )); do
#ifdef any
  [[ "$1" == '-a' ]] && { any=1; shift; continue; }
#endif
#ifdef nocase
  [[ "$1" == '-i' ]] && { nocase=1; shift; continue; }
#endif
  [[ "$1" == '--' ]] && { shift; break; }
done

dash_dash_pos=${@[(i)--]}
options=("${@:1:$((dash_dash_pos - 1))}")
regex="${@:$((dash_dash_pos + 1)):1}"

#ifdef DEBUG
if (( ${#options[@]} == 0 )); then
  echo "%FUNCNAME%: missing options" >&2
  return 1
fi

if (( ${#regex} == 0 )); then
  echo "%FUNCNAME%: missing regex" >&2
  return 1
fi

#endif
for (( i=${#HAVING_OPTIONS[@]}; i > 0; --i )); do
  if array_contains "${HAVING_OPTIONS[$i]}" "${options[@]}"; then
#ifdef nocase
    if (( nocase ));
    then [[ "${(L)OPTION_VALUES[$i]}" =~ "${(L)regex}" ]] && return 0
    else [[ "${OPTION_VALUES[$i]}" =~ "${regex}" ]] && return 0
    fi
#else
    [[ "${OPTION_VALUES[$i]}" =~ "${regex}" ]] && return 0
#endif
#ifdef any
    (( any )) || return 1
#else
    return 1
#endif
  fi
done

return 1
''', ['array_contains'])

_PREFIX = ShellFunction('prefix', r'''
if [[ "$PREFIX" == "$1"* ]]; then
  PREFIX="${PREFIX#"$1"}"
  IPREFIX="$IPREFIX$1"
  $2
else
  compadd -S '' -- "$1"
fi
''')

_EXEC = ShellFunction('exec', r'''
local item='' desc='' describe=()

while IFS=$'\t' read -r item desc; do
  item="${item//\\/\\\\}"
  item="${item//:/\\:}"
  desc="${desc//\\/\\\\}"
  [[ -n "$desc" ]] && describe+=("$item:$desc") || describe+=("$item")
done < <(eval "$1")

_describe '' describe
''')

_KEY_VALUE_PAIR_EXEC = ShellFunction('key_value_pair_exec', r'''
local sep="$1"
local func="$2"
local key='' desc=''
local -a args=()

while IFS=$'\t' read -r key desc; do
  desc="${desc//\\/\\\\}"
  desc="${desc//:/\\:}"
  desc="${desc//\[/\\[}"
  desc="${desc//\]/\\]}"

  if [[ "${key[-1]}" == '=' ]]; then
    key="${key:0:-1}"
    args+=("${key}[$desc]:::{exec '$func $key'}")
  else
    args+=("${key}[$desc]")
  fi
done < <(eval "$func")

_values -S "$sep" '' "${args[@]}"
''', ['exec'])

_KEY_VALUE_LIST_EXEC = ShellFunction('key_value_list_exec', r'''
local sep1="$1"
local sep2="$2"
local func="$3"
local key='' desc='' excludes=''
local -a args=()

while IFS=$'\t' read -r key desc excludes; do
  desc="${desc//\\/\\\\}"
  desc="${desc//:/\\:}"
  desc="${desc//\[/\\[}"
  desc="${desc//\]/\\]}"

  [[ -n "$excludes" ]] && excludes="($excludes)"

  if [[ "${key: -1:1}" == '=' ]]; then
    key="${key:0:-1}"
    args+=("${excludes}${key}[$desc]: :{exec '$func $key'}")
  elif [[ "${key: -2:2}" == '=?' ]]; then
    key="${key:0:-2}"
    args+=("${excludes}${key}[$desc]:: :{exec '$func $key'}")
  else
    args+=("${excludes}${key}[$desc]")
  fi
done < <(eval "$func")

_values -s "$sep1" -S "$sep2" '' "${args[@]}"
''', ['exec'])

_HISTORY = ShellFunction('history', r'''
[[ -f "$HISTFILE" ]] || return

local match=''

command grep -E -o -- "$1" "$HISTFILE" | while read -r match; do
  compadd -- "$match"
done
''')

_MIME_FILE = ShellFunction('mime_file', r'''
local line='' file='' mime='' i_opt=''

if command file -i /dev/null &>/dev/null; then
  i_opt="-i"
elif command file -I /dev/null &>/dev/null; then
  i_opt="-I"
else
  compadd -- "$PREFIX"*
  return
fi

command file -L $i_opt -- "$PREFIX"* 2>/dev/null | while read -r line; do
  mime="${line##*:}"

  if [[ "$mime" == *inode/directory* ]] || command grep -q -E -- "$1" <<< "$mime"; then
    file="${line%:*}"

    if [[ "$file" == *\\* ]]; then
      file="$(command perl -pe 's/\\([0-7]{3})/chr(oct($1))/ge' <<< "$file")"
    fi

    if [[ "$mime" == *inode/directory* ]]; then
      compadd -- "$file/"
    else
      compadd -- "$file"
    fi
  fi
done
''')

_UID_LIST = ShellFunction('uid_list', r'''
local items=($(command getent passwd | command awk -F: '{printf "%s:%s\n", $3, $1}'))
_describe 'users' items
''')

_GID_LIST = ShellFunction('gid_list', r'''
local items=($(command getent group | command awk -F: '{printf "%s:%s\n", $3, $1}'))
_describe 'groups' items
''')

_CHARSET_LIST = ShellFunction('charset_list', r'''
local items=($(command locale -m))
_describe 'charsets' items
''')

_PATH_FILES_RELATIVE = ShellFunction('path_files_relative', r'''
local DIR="$1"; shift
_path_files -W "$PWD/$DIR" "$@"
''')

# =============================================================================
# Bonus
# =============================================================================

_MOUNTPOINT = ShellFunction('mountpoint', r'''
local item=''

command findmnt -lno TARGET | while read -r item; do
  compadd -- "$item"
done
''')

_ALSA_COMPLETE_CARDS = ShellFunction('alsa_complete_cards', r'''
local card='' cards=()
command aplay -l \
  | command grep -Eo '^card [0-9]+: [^,]+' \
  | command uniq \
  | while builtin read card; do
  card="${card#card }"
  local id="${card%%: *}"
  local name="${card#*: }"
  cards+=("$id:$name")
done

_describe 'ALSA card' cards
''')

_ALSA_COMPLETE_DEVICES = ShellFunction('alsa_complete_devices', r'''
local card='' id='' name='' devices=()
command aplay -l \
  | command grep -Eo '^card [0-9]+: [^,]+' \
  | command uniq \
  | while builtin read card; do
  card="${card#card }"
  id="${card%%: *}"
  name="${card#*: }"
  devices+=("hw\\:$id:$name")
done

_describe 'ALSA device' devices
''')


class ZshHelpers(GeneralHelpers):
    '''Class holding helper functions for Zsh.'''

    def __init__(self, config, function_prefix):
        super().__init__(config, function_prefix, ShellFunction)
        self.add_function(_ARRAY_CONTAINS)
        self.add_function(_QUERY)
        self.add_function(_OPTION_MATCH)
        self.add_function(_EXEC)
        self.add_function(_KEY_VALUE_PAIR_EXEC)
        self.add_function(_KEY_VALUE_LIST_EXEC)
        self.add_function(_PREFIX)
        self.add_function(_HISTORY)
        self.add_function(_PATH_FILES_RELATIVE)
        self.add_function(_MIME_FILE)
        self.add_function(_UID_LIST)
        self.add_function(_GID_LIST)
        self.add_function(_CHARSET_LIST)
        self.add_function(_MOUNTPOINT)
        self.add_function(_ALSA_COMPLETE_CARDS)
        self.add_function(_ALSA_COMPLETE_DEVICES)
