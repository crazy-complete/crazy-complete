#!/usr/bin/python3

from . import helpers

_ZSH_HELPER_FUNC = helpers.ShellFunction('zsh_helper', r'''
# ===========================================================================
#
# This function is for querying the command line.
#
# COMMANDS
#   setup <OPTIONS> <ARGS...>
#     This is the first call you have to make, otherwise the other commands
#     won't (successfully) work.
#
#     It parses <ARGS> accordings to <OPTIONS> and stores results in the
#     variables POSITIONALS, HAVING_OPTIONS and OPTION_VALUES.
#
#     The first argument is a comma-seperated list of options that the parser
#     should know about. Short options (-o), long options (--option), and
#     old-style options (-option) are supported.
#
#     If an option takes an argument, it is suffixed by '='.
#     If an option takes an optional argument, it is suffixed by '=?'.
#
#   get_positional <NUM>
#     Prints out the positional argument number NUM (starting from 1)
#
#   has_option <OPTIONS...>
#     Checks if a option given in OPTIONS is passed on commandline.
#
#   option_is <OPTIONS...> -- <VALUES...>
#     Checks if one option in OPTIONS has a value of VALUES.
#
# EXAMPLE
#   local POSITIONALS HAVING_OPTIONS OPTION_VALUES
#   zsh_helper setup '-f,-a=,-optional=?' program_name -f -optional -a foo bar
#   zsh_helper has_option -f
#   zsh_helper option_is -a -- foo
#
#   Here, -f is a flag, -a takes an argument, and -optional takes an optional
#   argument.
#
#   Both queries return true.
#
# ===========================================================================

local FUNC="zsh_helper"
local CONTAINS="${FUNC}_contains"

$CONTAINS() {
  local ARG KEY="$1"; shift
  for ARG; do [[ "$KEY" == "$ARG" ]] && return 0; done
  return 1
}

if [[ $# == 0 ]]; then
  echo "$FUNC: missing command" >&2
  return 1;
fi

local CMD=$1
shift

case "$CMD" in
  get_positional)
    if test $# -ne 1; then
      echo "$FUNC: get_positional: takes exactly one argument" >&2
      return 1;
    fi

    if test "$1" -eq 0; then
      echo "$FUNC: get_positional: positionals start at 1, not 0!" >&2
      return 1
    fi

    printf "%s" "${POSITIONALS[$1]}"
    return 0
    ;;
  has_option)
    if test $# -eq 0; then
      echo "$FUNC: has_option: arguments required" >&2
      return 1;
    fi

    local OPTION=''
    for OPTION in "${HAVING_OPTIONS[@]}"; do
      $CONTAINS "$OPTION" "$@" && return 0
    done

    return 1
    ;;
  option_is)
    local -a CMD_OPTION_IS_OPTIONS CMD_OPTION_IS_VALUES
    local END_OF_OPTIONS_NUM=0

    while test $# -ge 1; do
      if [[ "$1" == "--" ]]; then
        (( ++END_OF_OPTIONS_NUM ))
      elif test $END_OF_OPTIONS_NUM -eq 0; then
        CMD_OPTION_IS_OPTIONS+=("$1")
      elif test $END_OF_OPTIONS_NUM -eq 1; then
        CMD_OPTION_IS_VALUES+=("$1")
      fi

      shift
    done

    if test ${#CMD_OPTION_IS_OPTIONS[@]} -eq 0; then
      echo "$FUNC: option_is: missing options" >&2
      return 1
    fi

    if test ${#CMD_OPTION_IS_VALUES[@]} -eq 0; then
      echo "$FUNC: option_is: missing values" >&2
      return 1
    fi

    local I=${#HAVING_OPTIONS[@]}
    while test $I -ge 1; do
      local OPTION="${HAVING_OPTIONS[$I]}"
      if $CONTAINS "$OPTION" "${CMD_OPTION_IS_OPTIONS[@]}"; then
        local VALUE="${OPTION_VALUES[$I]}"
        $CONTAINS "$VALUE" "${CMD_OPTION_IS_VALUES[@]}" && return 0
      fi

      (( --I ))
    done

    return 1
    ;;
  setup)
    local IFS=','
    local -a OPTIONS=(${=1})
    unset IFS
    shift
    ;;
  *)
    echo "$FUNC: argv[1]: invalid command" >&2
    return 1
    ;;
esac

# continuing setup....

# ===========================================================================
# Parsing of available options
# ===========================================================================

local -a   OLD_OPTS_WITH_ARG   OLD_OPTS_WITH_OPTIONAL_ARG   OLD_OPTS_WITHOUT_ARG
local -a  LONG_OPTS_WITH_ARG  LONG_OPTS_WITH_OPTIONAL_ARG  LONG_OPTS_WITHOUT_ARG
local -a SHORT_OPTS_WITH_ARG SHORT_OPTS_WITH_OPTIONAL_ARG SHORT_OPTS_WITHOUT_ARG

local OPTION
for OPTION in "${OPTIONS[@]}"; do
  case "$OPTION" in
    --?*=)    LONG_OPTS_WITH_ARG+=("${OPTION%=}");;
    --?*=\?)  LONG_OPTS_WITH_OPTIONAL_ARG+=("${OPTION%=?}");;
    --?*)     LONG_OPTS_WITHOUT_ARG+=("$OPTION");;

    -?=)      SHORT_OPTS_WITH_ARG+=("${OPTION%=}");;
    -?=\?)    SHORT_OPTS_WITH_OPTIONAL_ARG+=("${OPTION%=?}");;
    -?)       SHORT_OPTS_WITHOUT_ARG+=("$OPTION");;

    -??*=)    OLD_OPTS_WITH_ARG+=("${OPTION%=}");;
    -??*=\?)  OLD_OPTS_WITH_OPTIONAL_ARG+=("${OPTION%=?}");;
    -??*)     OLD_OPTS_WITHOUT_ARG+=("$OPTION");;

    *) echo "$FUNC: $OPTION: not a valid short, long or oldstyle option" >&2; return 1;;
  esac
done

# ===========================================================================
# Parsing of command line options
# ===========================================================================

POSITIONALS=()
HAVING_OPTIONS=()
OPTION_VALUES=()

local ARGI=2 # ARGI[1] is program name
while [[ $ARGI -le $# ]]; do
  local ARG="${@[$ARGI]}"
  local HAVE_TRAILING_ARG=$(test $ARGI -lt $# && echo true || echo false)

  case "$ARG" in
    (-)
      POSITIONALS+=(-);;
    (--)
      for ARGI in $(seq $((ARGI + 1)) $#); do
        POSITIONALS+=("${@[$ARGI]}")
      done
      break;;
    (--*)
      for OPTION in $LONG_OPTS_WITH_ARG $LONG_OPTS_WITHOUT_ARG $LONG_OPTS_WITH_OPTIONAL_ARG; do
        if [[ "$ARG" == "$OPTION="* ]]; then
          HAVING_OPTIONS+=("$OPTION")
          OPTION_VALUES+=("${ARG#$OPTION=}")
          break
        elif [[ "$ARG" == "$OPTION" ]]; then
          if $CONTAINS "$OPTION" "${LONG_OPTS_WITH_ARG[@]}"; then
            if $HAVE_TRAILING_ARG; then
              HAVING_OPTIONS+=("$OPTION")
              OPTION_VALUES+=("${@[$((ARGI + 1))]}")
              (( ARGI++ ))
            fi
          else
            HAVING_OPTIONS+=("$OPTION")
            OPTION_VALUES+=("")
          fi
          break
        fi
      done;;
    (-*)
      local HAVE_MATCH=false

      for OPTION in $OLD_OPTS_WITH_ARG $OLD_OPTS_WITHOUT_ARG $OLD_OPTS_WITH_OPTIONAL_ARG; do
        if [[ "$ARG" == "$OPTION="* ]]; then
          HAVING_OPTIONS+=("$OPTION")
          OPTION_VALUES+=("${ARG#$OPTION=}")
          HAVE_MATCH=true
          break
        elif [[ "$ARG" == "$OPTION" ]]; then
          if $CONTAINS "$OPTION" "${OLD_OPTS_WITH_ARG[@]}"; then
            if $HAVE_TRAILING_ARG; then
              HAVING_OPTIONS+=("$OPTION")
              OPTION_VALUES+=("${@[$((ARGI + 1))]}")
              (( ARGI++ ))
            fi
          else
            HAVING_OPTIONS+=("$OPTION")
            OPTION_VALUES+=("")
          fi

          HAVE_MATCH=true
          break
        fi
      done

      if ! $HAVE_MATCH; then
        local ARG_LENGTH=${#ARG}
        local I=1
        local IS_END=false
        while ! $IS_END && test $I -lt $ARG_LENGTH; do
          local ARG_CHAR="${ARG:$I:1}"
          local HAVE_TRAILING_CHARS=$(test $((I+1)) -lt $ARG_LENGTH && echo true || echo false)

          for OPTION in $SHORT_OPTS_WITH_ARG $SHORT_OPTS_WITHOUT_ARG $SHORT_OPTS_WITH_OPTIONAL_ARG; do
            local OPTION_CHAR="${OPTION:1:1}"

            if test "$ARG_CHAR" = "$OPTION_CHAR"; then
              if $CONTAINS "$OPTION" "${SHORT_OPTS_WITH_ARG[@]}"; then
                if $HAVE_TRAILING_CHARS; then
                  HAVING_OPTIONS+=("$OPTION")
                  OPTION_VALUES+=("${ARG:$((I+1))}")
                  IS_END=true
                elif $HAVE_TRAILING_ARG; then
                  HAVING_OPTIONS+=("$OPTION")
                  OPTION_VALUES+=("${@[$((ARGI + 1))]}")
                  (( ARGI++ ))
                  IS_END=true
                fi
              elif $CONTAINS "$OPTION" "${SHORT_OPTS_WITH_OPTIONAL_ARG[@]}"; then
                HAVING_OPTIONS+=("$OPTION")

                if $HAVE_TRAILING_CHARS; then
                  IS_END=true
                  OPTION_VALUES+=("${ARG:$((I+1))}")
                else
                  OPTION_VALUES+=("")
                fi
              else
                HAVING_OPTIONS+=("$OPTION")
                OPTION_VALUES+=("")
              fi

              break
            fi
          done

          (( I++ ))
        done
      fi;;
    (*)
      POSITIONALS+=("$ARG");;
  esac

  (( ARGI++ ))
done
''')

_EXEC = helpers.ShellFunction('exec', r'''
local -a DESCRIBE=()
local LINE=''

while IFS='' read -r LINE; do
  LINE="${LINE/:/\\:/}"
  LINE="${LINE/$'\t'/:}"
  DESCRIBE+=("$LINE")
done < <(eval "$1")

_describe '' DESCRIBE
''')

class ZSH_Helpers(helpers.GeneralHelpers):
    def __init__(self, function_prefix):
        super().__init__(function_prefix)
        self.add_function(_ZSH_HELPER_FUNC)
        self.add_function(_EXEC)
