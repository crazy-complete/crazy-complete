#!/bin/bash

unset CDPATH
set -u +o histexpand

foo() {
  local -a POSITIONALS
  local POSITIONAL_INDEX=0
  local argi c
  local HAVE_ARG=0 HAVE_A=0 HAVE_B=0

  for ((argi=1; argi <= $#; ++argi)); do
    local arg="${!argi}"

    case "$arg" in
      --arg|--arg=*)
        HAVE_ARG=1
        [[ "$arg" == *"="* ]] || (( ++argi ))
        ;;
      --)
        (( ++argi ))
        break
        ;;
      --*)
        ;;
      -)
        POSITIONALS[$((POSITIONAL_INDEX++))]="$arg"
        ;;
      -*)
        for ((c=1; c < ${#arg}; ++c)); do
          local char="${arg:$c:1}"
          case "$char" in
            a)
              HAVE_A=1
              (( $c + 1 < ${#arg} )) || (( ++argi ))
              break;
              ;;
            b)
              HAVE_B=1
          esac
        done
        ;;
      *)
        POSITIONALS[$((POSITIONAL_INDEX++))]="$arg"
        ;;
    esac
  done

  for ((; argi <= $#; ++argi)); do
    POSITIONALS[$((POSITIONAL_INDEX++))]="${!argi}"
  done

  echo "HAVE_B=$HAVE_B"
  echo "HAVE_A=$HAVE_A"
  echo "HAVE_ARG=$HAVE_ARG"
  echo "POSITIONALS=${POSITIONALS[@]}"
}

foo --arg=foo -ba bar foo -- bar baz

exec_() {
  local item desc

  while IFS=$'\t' read -r item desc; do
    if [[ "$item" == "$cur"* ]]; then
      COMPREPLY+=("$(printf '%q' "$item")")
    fi
  done < <(eval "$1")
}

bash_helper() {
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

  local FUNC="bash_helper"
  local CONTAINS="__contains"

  __contains() {
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
      local -a CMD_OPTION_IS_OPTIONS=() CMD_OPTION_IS_VALUES=()
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

      local I=$(( ${#HAVING_OPTIONS[@]} - 1))
      while test $I -ge 0; do
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
      local -a OPTIONS=(${1})
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
    local ARG="${!ARGI}"
    local HAVE_TRAILING_ARG=$(test $ARGI -lt $# && echo true || echo false)

    case "$ARG" in
      -)
        POSITIONALS+=(-);;
      --)
        for ARGI in $(seq $((ARGI + 1)) $#); do
          POSITIONALS+=("${@[$ARGI]}")
        done
        break;;
      --*)
        for OPTION in "${LONG_OPTS_WITH_ARG[@]}" "${LONG_OPTS_WITHOUT_ARG[@]}" "${LONG_OPTS_WITH_OPTIONAL_ARG[@]}"; do
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
      -*)
        local HAVE_MATCH=false

        for OPTION in "${OLD_OPTS_WITH_ARG[@]}" "${OLD_OPTS_WITHOUT_ARG[@]}" "${OLD_OPTS_WITH_OPTIONAL_ARG[@]}"; do
          if [[ "$ARG" == "$OPTION="* ]]; then
            HAVING_OPTIONS+=("$OPTION")
            OPTION_VALUES+=("${ARG#$OPTION=}")
            HAVE_MATCH=true
            break
          elif [[ "$ARG" == "$OPTION" ]]; then
            if $CONTAINS "$OPTION" "${OLD_OPTS_WITH_ARG[@]}"; then
              if $HAVE_TRAILING_ARG; then
                HAVING_OPTIONS+=("$OPTION")
                OPTION_VALUES+=("${@:$((ARGI + 1)):1}")
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

            for OPTION in "${SHORT_OPTS_WITH_ARG[@]}" "${SHORT_OPTS_WITHOUT_ARG[@]}" "${SHORT_OPTS_WITH_OPTIONAL_ARG[@]}"; do
              local OPTION_CHAR="${OPTION:1:1}"

              if test "$ARG_CHAR" = "$OPTION_CHAR"; then
                if $CONTAINS "$OPTION" "${SHORT_OPTS_WITH_ARG[@]}"; then
                  if $HAVE_TRAILING_CHARS; then
                    HAVING_OPTIONS+=("$OPTION")
                    OPTION_VALUES+=("${ARG:$((I+1))}")
                    IS_END=true
                  elif $HAVE_TRAILING_ARG; then
                    HAVING_OPTIONS+=("$OPTION")
                    OPTION_VALUES+=("${@:$((ARGI + 1)):1}")
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
      *)
        POSITIONALS+=("$ARG");;
    esac

    (( ARGI++ ))
  done
}

value_list() {
  local separator="$1"; shift
  local -a values=("$@")
  local -a having_values

  if [[ -z "$cur" ]]; then
    COMPREPLY=("${values[@]}")
    return
  fi

  IFS="$separator" read -r -a having_values <<< "$cur"

  local -a remaining_values=()
  local value having_value found_value

  for value in "${values[@]}"; do
    found_value=false

    for having_value in "${having_values[@]}"; do
      if [[ "$value" == "$having_value" ]]; then
        found_value=true
        break
      fi
    done

    if ! $found_value; then
      remaining_values+=("$value")
    fi
  done

  COMPREPLY=()

  if [[ "${cur: -1}" == "$separator" ]]; then
    for value in "${remaining_values[@]}"; do
      COMPREPLY+=("$cur$value")
    done
  elif (( ${#having_values[@]} )); then
    local cur_last_value=${having_values[-1]}

    for value in "${remaining_values[@]}"; do
      if [[ "$value" == "$cur_last_value"* ]]; then
        COMPREPLY+=("${cur%"$cur_last_value"}$value")
      fi
    done
  fi
}

exported_variables() {
  COMPREPLY=()

  local var
  for var in $(declare -p -x | sed 's/=.*//; s/.* //'); do
    [[ "$var" == "$cur"* ]] && COMPREPLY+=("$var")
  done
}

# TODO: test
#bash_helper setup -o= progname -o bar
#bash_helper has_option -o && echo true
#bash_helper option_is -o -- bar && echo true
