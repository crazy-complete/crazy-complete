'''This module contains helper functions for Zsh.'''

from . import helpers


_ZSH_QUERY_FUNC = helpers.ShellFunction('zsh_query', r'''
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
#   option_is <OPTIONS...> -- <VALUES...>
#     Checks if one option in OPTIONS has a value of VALUES.
#
# EXAMPLE
#   local POSITIONALS HAVING_OPTIONS OPTION_VALUES
#   zsh_query init '-f,-a=,-optional=?' program_name -f -optional -a foo bar
#   zsh_query has_option -f
#   zsh_query option_is -a -- foo
#
#   Here, -f is a flag, -a takes an argument, and -optional takes an optional
#   argument.
#
#   Both queries return true.
#
# ===========================================================================

__zsh_query_contains() {
  local arg='' key="$1"; shift
  for arg; do [[ "$key" == "$arg" ]] && return 0; done
  return 1
}

local cmd="$1"; shift

case "$cmd" in
#ifdef get_positional
  get_positional)
    if (( $# != 1 )); then
      echo "%FUNCNAME%: get_positional: takes exactly one argument" >&2
      return 1
    fi

    if test "$1" -eq 0; then
      echo "%FUNCNAME%: get_positional: positionals start at 1, not 0!" >&2
      return 1
    fi

    printf "%s" "${POSITIONALS[$1]}"
    return 0;;
#endif
#ifdef get_option
  get_option)
    local i=0

    if (( $# == 0 )); then
      echo "%FUNCNAME%: get_option: arguments required" >&2
      return 1
    fi

    for (( i=0; i <= ${#HAVING_OPTIONS[@]}; ++i )); do
      local option="${HAVING_OPTIONS[$i]}"
      if __zsh_query_contains "$option" "$@"; then
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

#endif
    if (( $# == 0 )); then
      echo "%FUNCNAME%: has_option: arguments required" >&2
      return 1
    fi

    for option in "${HAVING_OPTIONS[@]}"; do
      __zsh_query_contains "$option" "$@" && return 0
    done

#ifdef with_incomplete
    (( with_incomplete )) && \
      __zsh_query_contains "$INCOMPLETE_OPTION" "$@" && return 0

#endif
    return 1;;
#endif
#ifdef option_is
  option_is)
    local i=0 dash_dash_pos=0 cmd_option_is_options=() cmd_option_is_values=()

    dash_dash_pos=${@[(i)--]}
    cmd_option_is_options=("${@:1:$((dash_dash_pos - 1))}")
    cmd_option_is_values=("${@:$((dash_dash_pos + 1))}")

    if (( ${#cmd_option_is_options[@]} == 0 )); then
      echo "%FUNCNAME%: option_is: missing options" >&2
      return 1
    fi

    if (( ${#cmd_option_is_values[@]} == 0 )); then
      echo "%FUNCNAME%: option_is: missing values" >&2
      return 1
    fi

    for (( i=${#HAVING_OPTIONS[@]}; i > 0; --i )); do
      local option="${HAVING_OPTIONS[$i]}"
      if __zsh_query_contains "$option" "${cmd_option_is_options[@]}"; then
        local value="${OPTION_VALUES[$i]}"
        __zsh_query_contains "$value" "${cmd_option_is_values[@]}" && return 0
      fi
    done

    return 1;;
#endif
  init)
    local IFS=','
    local -a options=(${=1})
    unset IFS
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
    *) echo "%FUNCNAME%: $option: not a valid short, long or oldstyle option" >&2; return 1;;
  esac
done

# ===========================================================================
# Parsing of command line options
# ===========================================================================

POSITIONALS=()
HAVING_OPTIONS=()
OPTION_VALUES=()
INCOMPLETE_OPTION=''

local argi=2 # argi[1] is program name
for ((; argi <= $#; ++argi)); do
  local arg="${@[$argi]}"
  local have_trailing_arg=$(test $argi -lt $# && echo true || echo false)

  case "$arg" in
    -)
      POSITIONALS+=(-);;
    --)
      for argi in $(command seq $((argi + 1)) $#); do
        POSITIONALS+=("${@[$argi]}")
      done
      break;;
    --*=*)
      HAVING_OPTIONS+=("${arg%%=*}")
      OPTION_VALUES+=("${arg#*=}");;
    --*)
#ifdef long_options
      if __zsh_query_contains "$arg" "${long_opts_with_arg[@]}"; then
        if $have_trailing_arg; then
          HAVING_OPTIONS+=("$arg")
          OPTION_VALUES+=("${@[$((++argi))]}")
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
    -*)
      local end_of_parsing=0

#ifdef old_options
      if [[ "$arg" == *=* ]]; then
        local option="${arg%%=*}" value="${arg#*=}"
        if __zsh_query_contains "$option" "${old_opts_with_arg[@]}" "${old_opts_with_optional_arg[@]}"; then
          HAVING_OPTIONS+=("$option")
          OPTION_VALUES+=("$value")
          end_of_parsing=1
        fi
      elif __zsh_query_contains "$arg" "${old_opts_with_arg[@]}"; then
        end_of_parsing=1
        if $have_trailing_arg; then
          HAVING_OPTIONS+=("$arg")
          OPTION_VALUES+=("${@[$((++argi))]}")
#ifdef with_incomplete
        else
          INCOMPLETE_OPTION="$arg"
#endif
        fi
      elif __zsh_query_contains "$arg" "${old_opts_without_arg[@]}" "${old_opts_with_optional_arg[@]}"; then
        HAVING_OPTIONS+=("$arg")
        OPTION_VALUES+=("")
        end_of_parsing=1
      fi
#endif

#ifdef short_options
      local i=1 arg_length=${#arg}
      for ((; ! end_of_parsing && i < arg_length; ++i)); do
        local option="-${arg:$i:1}"
        local trailing_chars="${arg:$((i+1))}"

        if __zsh_query_contains "$option" "${short_opts_without_arg[@]}"; then
          HAVING_OPTIONS+=("$option")
          OPTION_VALUES+=("")
        elif __zsh_query_contains "$option" "${short_opts_with_arg[@]}"; then
          end_of_parsing=1

          if [[ -n "$trailing_chars" ]]; then
            HAVING_OPTIONS+=("$option")
            OPTION_VALUES+=("$trailing_chars")
          elif $have_trailing_arg; then
            HAVING_OPTIONS+=("$option")
            OPTION_VALUES+=("${@[$((++argi))]}")
#ifdef with_incomplete
          else
            INCOMPLETE_OPTION="$option"
#endif
          fi
        elif __zsh_query_contains "$option" "${short_opts_with_optional_arg[@]}"; then
          end_of_parsing=1
          HAVING_OPTIONS+=("$option")
          OPTION_VALUES+=("$trailing_chars") # may be empty
        fi
      done
#endif
      ;;
    *)
      POSITIONALS+=("$arg");;
  esac
done
''')

_EXEC = helpers.ShellFunction('exec', r'''
local item='' desc='' describe=()

while IFS=$'\t' read -r item desc; do
  item="${item//:/\\:}"
  [[ -n "$desc" ]] && describe+=("$item:$desc") || describe+=("$item")
done < <(eval "$1")

_describe '' describe
''')

_HISTORY = helpers.ShellFunction('history', r'''
[[ -f "$HISTFILE" ]] || return

local match=''

command grep -E -o -- "$1" "$HISTFILE" | while read -r match; do
  compadd -- "$match"
done
''')

_MIME_FILE = helpers.ShellFunction('mime_file', r'''
local line='' file='' mime='' i_opt='' cur=''

cur="${words[$CURRENT]}"
[[ "$cur" == --*= ]] && cur="${cur#--*=}"

if command file -i /dev/null &>/dev/null; then
  i_opt="-i"
elif command file -I /dev/null &>/dev/null; then
  i_opt="-I"
else
  compadd -- "$cur"*
  return
fi

command file -L $i_opt -- "$cur"* 2>/dev/null | while read -r line; do
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

# =============================================================================
# Bonus
# =============================================================================

_ALSA_COMPLETE_CARDS = helpers.ShellFunction('alsa_complete_cards', r'''
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

_describe 'ALSA card' cards''')

_ALSA_COMPLETE_DEVICES = helpers.ShellFunction('alsa_complete_devices', r'''
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

_describe 'ALSA device' devices''')


class ZshHelpers(helpers.GeneralHelpers):
    '''Class holding helper functions for Zsh.'''

    def __init__(self, function_prefix):
        super().__init__(function_prefix, helpers.ShellFunction)
        self.add_function(_ZSH_QUERY_FUNC)
        self.add_function(_EXEC)
        self.add_function(_HISTORY)
        self.add_function(_MIME_FILE)
        self.add_function(_ALSA_COMPLETE_CARDS)
        self.add_function(_ALSA_COMPLETE_DEVICES)
