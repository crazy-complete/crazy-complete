#!/usr/bin/zsh

zsh_query() {
  # ===========================================================================
  #
  # This function is for querying the command line.
  #
  # COMMANDS
  #   setup <OPTIONS> <ARGS...>
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
  #   zsh_query setup '-f,-a=,-optional=?' program_name -f -optional -a foo bar
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
    setup)
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

  # continuing setup....

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
}

_exec() {
  local -a describe=()
  local item='' desc=''

  while IFS=$'\t' read -r item desc; do
    item="${item/:/\\:/}"
    describe+=("$item:$desc")
  done < <(eval "$1")

  _describe '' describe
}

_has_hidden_option() {
  local option=''

  for option; do
    case "$option" in
      -?) option="${option:1:1}"
          [[ "${words[-1]}" != --* ]] && [[ "${words[-1]}" == -*$option* ]] && return 0
          [[ "${words[-2]}" != --* ]] && [[ "${words[-2]}" == -*$option  ]] && return 0;;
       *)
          [[ "${words[-1]}" == $option* ]] && return 0
          [[ "${words[-2]}" == $option  ]] && return 0;;
      esac
  done

  return 1
}

# =============================================================================
# TEST CODE
# =============================================================================

if [[ $# == 1 ]] && [[ "$1" == "-q" ]]; then
  echo() {}
fi

test_case() {
  local TEST_NUMBER="$1"; shift
  local EXPECTED="$1"; shift
  local -a TEST_ARGS=() SETUP_ARGS=()

  while test $# -ge 1; do
    if [[ "$1" == ":SETUP:" ]]; then
      shift
      SETUP_ARGS=("$@")
      break
    else
      TEST_ARGS+=("$1")
      shift
    fi
  done

  zsh_query setup "${SETUP_ARGS[@]}"

  local RESULT
  RESULT="$(zsh_query "${TEST_ARGS[@]}")"
  local RESULT_EXIT=$?
  echo -n "Testing $TEST_NUMBER ... "

  if [[ "$EXPECTED" == "-true" ]]; then;
    if test $RESULT_EXIT -ne 0; then
      echo "expected TRUE, got $RESULT_EXIT"
      exit 1
    fi
  elif [[ "$EXPECTED" == "-false" ]]; then;
    if test $RESULT_EXIT -eq 0; then
      echo "expected FALSE, got $RESULT_EXIT"
      exit 1
    fi
  elif [[ "$EXPECTED" != "$RESULT" ]]; then
    echo "expected '$EXPECTED', got '$RESULT'"
    exit 1
  fi

  echo "OK"
}

opts='-f,--flag,-flag,-a=,--arg=,-arg=,-o=?,--optional=?,-optional=?'
test_case 01 'foo'  get_positional 1 :SETUP: "$opts" prog foo
test_case 02 'foo'  get_positional 1 :SETUP: "$opts" prog foo
test_case 03 'foo'  get_positional 1 :SETUP: "$opts" prog -f foo
test_case 04 'foo'  get_positional 1 :SETUP: "$opts" prog -flag foo
test_case 05 'foo'  get_positional 1 :SETUP: "$opts" prog --flag foo
test_case 06 'foo'  get_positional 1 :SETUP: "$opts" prog -a arg foo
test_case 07 'foo'  get_positional 1 :SETUP: "$opts" prog -arg arg foo
test_case 08 'foo'  get_positional 1 :SETUP: "$opts" prog --arg arg foo
test_case 09 'foo'  get_positional 1 :SETUP: "$opts" prog -aarg foo
test_case 10 'foo'  get_positional 1 :SETUP: "$opts" prog -arg=arg foo
test_case 11 'foo'  get_positional 1 :SETUP: "$opts" prog --arg=arg foo
test_case 12 'foo'  get_positional 1 :SETUP: "$opts" prog -o foo
test_case 13 'foo'  get_positional 1 :SETUP: "$opts" prog -optional foo
test_case 14 'foo'  get_positional 1 :SETUP: "$opts" prog --optional foo
test_case 15 'foo'  get_positional 1 :SETUP: "$opts" prog -oarg foo
test_case 16 'foo'  get_positional 1 :SETUP: "$opts" prog -optional=arg foo
test_case 17 'foo'  get_positional 1 :SETUP: "$opts" prog --optional=arg foo
test_case 18 'foo'  get_positional 1 :SETUP: "$opts" prog -foarg foo
test_case 19 'foo'  get_positional 1 :SETUP: "$opts" prog -faarg foo
test_case 20 'foo'  get_positional 1 :SETUP: "$opts" prog -fa arg foo
test_case 21 'foo'  get_positional 1 :SETUP: "$opts" prog -- foo
test_case 22 '-'    get_positional 1 :SETUP: "$opts" prog -
test_case 23 '-f'   get_positional 1 :SETUP: "$opts" prog -- -f
test_case 24 -true  has_option -f --flag -flag :SETUP: "$opts" prog -f
test_case 25 -true  has_option -f --flag -flag :SETUP: "$opts" prog --flag
test_case 26 -true  has_option -f --flag -flag :SETUP: "$opts" prog -flag
test_case 27 -false has_option -f --flag -flag :SETUP: "$opts" prog -- -f
test_case 28 -false has_option -f --flag -flag :SETUP: "$opts" prog -- --flag
test_case 29 -false has_option -f --flag -flag :SETUP: "$opts" prog -- -flag
test_case 30 -false has_option -f --flag -flag :SETUP: "$opts" prog --arg --flag
test_case 31 -false has_option -f --flag -flag :SETUP: "$opts" prog -a --flag
test_case 32 -true  has_option -a --arg -arg :SETUP: "$opts" prog -afoo
test_case 33 -true  has_option -a --arg -arg :SETUP: "$opts" prog -a foo
test_case 34 -true  has_option -a --arg -arg :SETUP: "$opts" prog -arg foo
test_case 35 -true  has_option -a --arg -arg :SETUP: "$opts" prog -arg=foo
test_case 36 -true  has_option -a --arg -arg :SETUP: "$opts" prog --arg foo
test_case 37 -true  has_option -a --arg -arg :SETUP: "$opts" prog --arg=foo
test_case 38 -false has_option -a --arg -arg :SETUP: "$opts" prog -a
test_case 39 -false has_option -a --arg -arg :SETUP: "$opts" prog -arg
test_case 40 -false has_option -a --arg -arg :SETUP: "$opts" prog --arg
test_case 41 -true  has_option WITH_INCOMPLETE -a --arg -arg :SETUP: "$opts" prog -a
test_case 42 -true  has_option WITH_INCOMPLETE -a --arg -arg :SETUP: "$opts" prog -arg
test_case 43 -true  has_option WITH_INCOMPLETE -a --arg -arg :SETUP: "$opts" prog --arg
test_case 44 -true  option_is -a --arg -arg -- foo bar :SETUP: "$opts" prog -a foo
test_case 45 -true  option_is -a --arg -arg -- foo bar :SETUP: "$opts" prog --arg foo
test_case 46 -true  option_is -a --arg -arg -- foo bar :SETUP: "$opts" prog -arg foo
test_case 47 -false option_is -a --arg -arg -- foo     :SETUP: "$opts" prog -flag
test_case 48 -true  option_is -o --optional -optional -- foo bar :SETUP: "$opts" prog -ofoo
test_case 49 -true  option_is -o --optional -optional -- foo bar :SETUP: "$opts" prog --optional=foo
test_case 50 -true  option_is -o --optional -optional -- foo bar :SETUP: "$opts" prog -optional=foo
test_case 51 -true  option_is -o --optional -optional -- foo bar :SETUP: "$opts" prog -obar
test_case 52 -true  option_is -o --optional -optional -- foo bar :SETUP: "$opts" prog --optional=bar
test_case 53 -true  option_is -o --optional -optional -- foo bar :SETUP: "$opts" prog -optional=bar

words=(-o)           _has_hidden_option -o --option -option || echo "01: failed"
words=(-o arg)       _has_hidden_option -o --option -option || echo "02: failed"
words=(-oarg)        _has_hidden_option -o --option -option || echo "03: failed"
words=(-fo arg)      _has_hidden_option -o --option -option || echo "04: failed"
words=(-foarg)       _has_hidden_option -o --option -option || echo "05: failed"
words=(--option)     _has_hidden_option -o --option -option || echo "06: failed"
words=(--option arg) _has_hidden_option -o --option -option || echo "07: failed"
words=(--option=arg) _has_hidden_option -o --option -option || echo "08: failed"
words=(-option)      _has_hidden_option -o --option -option || echo "09: failed"
words=(-option arg)  _has_hidden_option -o --option -option || echo "10: failed"
words=(-option=arg)  _has_hidden_option -o --option -option || echo "11: failed"
words=(-o 1 2)       _has_hidden_option -o --option -option && echo "12: failed"
