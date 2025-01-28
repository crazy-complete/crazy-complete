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

if [[ $# == 0 ]]; then
  echo "%FUNCNAME%: missing command" >&2
  return 1;
fi

local cmd="$1"
shift

case "$cmd" in
  get_positional)
    if test $# -ne 1; then
      echo "%FUNCNAME%: get_positional: takes exactly one argument" >&2
      return 1;
    fi

    if test "$1" -eq 0; then
      echo "%FUNCNAME%: get_positional: positionals start at 1, not 0!" >&2
      return 1
    fi

    printf "%s" "${POSITIONALS[$1]}"
    return 0
    ;;
  has_option)
#ifdef with_incomplete
    local with_incomplete=0
    [[ "$1" == "WITH_INCOMPLETE" ]] && { with_incomplete=1; shift; }

#endif
    if test $# -eq 0; then
      echo "%FUNCNAME%: has_option: arguments required" >&2
      return 1;
    fi

    local option=''
    for option in "${HAVING_OPTIONS[@]}"; do
      __zsh_query_contains "$option" "$@" && return 0
    done

#ifdef with_incomplete
    (( with_incomplete )) && \
      __zsh_query_contains "$INCOMPLETE_OPTION" "$@" && return 0

#endif
    return 1
    ;;
  option_is)
    local -a cmd_option_is_options cmd_option_is_values
    local end_of_options_num=0

    while test $# -ge 1; do
      if [[ "$1" == "--" ]]; then
        (( ++end_of_options_num ))
      elif test $end_of_options_num -eq 0; then
        cmd_option_is_options+=("$1")
      elif test $end_of_options_num -eq 1; then
        cmd_option_is_values+=("$1")
      fi

      shift
    done

    if test ${#cmd_option_is_options[@]} -eq 0; then
      echo "%FUNCNAME%: option_is: missing options" >&2
      return 1
    fi

    if test ${#cmd_option_is_values[@]} -eq 0; then
      echo "%FUNCNAME%: option_is: missing values" >&2
      return 1
    fi

    local I=${#HAVING_OPTIONS[@]}
    while test $I -ge 1; do
      local option="${HAVING_OPTIONS[$I]}"
      if __zsh_query_contains "$option" "${cmd_option_is_options[@]}"; then
        local VALUE="${OPTION_VALUES[$I]}"
        __zsh_query_contains "$VALUE" "${cmd_option_is_values[@]}" && return 0
      fi

      (( --I ))
    done

    return 1
    ;;
  init)
    local IFS=','
    local -a options=(${=1})
    unset IFS
    shift
    ;;
  *)
    echo "%FUNCNAME%: argv[1]: invalid command" >&2
    return 1
    ;;
esac

# continuing init...

# ===========================================================================
# Parsing of available options
# ===========================================================================

#ifdef old_options
local -a   old_opts_with_arg=()   old_opts_with_optional_arg=()   old_opts_without_arg=()
#endif
#ifdef long_options
local -a  long_opts_with_arg=()  long_opts_with_optional_arg=()  long_opts_without_arg=()
#endif
#ifdef short_options
local -a short_opts_with_arg=() short_opts_with_optional_arg=() short_opts_without_arg=()
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
while [[ $argi -le $# ]]; do
  local arg="${@[$argi]}"
  local have_trailing_arg=$(test $argi -lt $# && echo true || echo false)

  case "$arg" in
    -)
      POSITIONALS+=(-);;
    --)
      for argi in $(seq $((argi + 1)) $#); do
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
          OPTION_VALUES+=("${@[$((argi + 1))]}")
          (( argi++ ))
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
      local end_of_parsing=false

#ifdef old_options
      if [[ "$arg" == *=* ]]; then
        local option="${arg%%=*}"
        local value="${arg#*=}"
        if __zsh_query_contains "$option" "${old_opts_with_arg[@]}" "${old_opts_with_optional_arg[@]}"; then
          HAVING_OPTIONS+=("$option")
          OPTION_VALUES+=("$value")
          end_of_parsing=true
        fi
      elif __zsh_query_contains "$arg" "${old_opts_with_arg[@]}"; then
        end_of_parsing=true
        if $have_trailing_arg; then
          HAVING_OPTIONS+=("$arg")
          OPTION_VALUES+=("${@[$((argi + 1))]}")
          (( argi++ ))
#ifdef with_incomplete
        else
          INCOMPLETE_OPTION="$arg"
#endif
        fi
      elif __zsh_query_contains "$arg" "${old_opts_without_arg[@]}" "${old_opts_with_optional_arg[@]}"; then
        HAVING_OPTIONS+=("$arg")
        OPTION_VALUES+=("")
        end_of_parsing=true
      fi
#endif

#ifdef short_options
      local arg_length=${#arg}
      local i=1
      while ! $end_of_parsing && test $i -lt $arg_length; do
        local option="-${arg:$i:1}"
        local trailing_chars="${arg:$((i+1))}"

        if __zsh_query_contains "$option" "${short_opts_without_arg[@]}"; then
          HAVING_OPTIONS+=("$option")
          OPTION_VALUES+=("")
        elif __zsh_query_contains "$option" "${short_opts_with_arg[@]}"; then
          end_of_parsing=true

          if [[ -n "$trailing_chars" ]]; then
            HAVING_OPTIONS+=("$option")
            OPTION_VALUES+=("$trailing_chars")
          elif $have_trailing_arg; then
            HAVING_OPTIONS+=("$option")
            OPTION_VALUES+=("${@[$((argi + 1))]}")
            (( argi++ ))
#ifdef with_incomplete
          else
            INCOMPLETE_OPTION="$option"
#endif
          fi
        elif __zsh_query_contains "$option" "${short_opts_with_optional_arg[@]}"; then
          end_of_parsing=true
          HAVING_OPTIONS+=("$option")
          OPTION_VALUES+=("$trailing_chars") # may be empty
        fi

        (( i++ ))
      done
#endif
      ;;
    *)
      POSITIONALS+=("$arg");;
  esac

  (( argi++ ))
done
''')

_EXEC = helpers.ShellFunction('exec', r'''
local -a describe=()
local item='' desc=''

while IFS=$'\t' read -r item desc; do
  item="${item//:/\\:}"
  describe+=("$item:$desc")
done < <(eval "$1")

_describe '' describe
''')

class ZshHelpers(helpers.GeneralHelpers):
    def __init__(self, function_prefix):
        super().__init__(function_prefix)
        self.add_function(_ZSH_QUERY_FUNC)
        self.add_function(_EXEC)
