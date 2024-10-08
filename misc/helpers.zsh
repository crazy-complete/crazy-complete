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
  #   has_option <OPTIONS...>
  #     Checks if an option given in OPTIONS is passed on commandline.
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
  
  local FUNC="zsh_query"
  
  __zsh_query_contains() {
    local arg='' key="$1"; shift
    for arg; do [[ "$key" == "$arg" ]] && return 0; done
    return 1
  }
  
  if [[ $# == 0 ]]; then
    echo "$FUNC: missing command" >&2
    return 1;
  fi
  
  local cmd="$1"
  shift
  
  case "$cmd" in
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
  
      local option=''
      for option in "${HAVING_OPTIONS[@]}"; do
        __zsh_query_contains "$option" "$@" && return 0
      done
  
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
        echo "$FUNC: option_is: missing options" >&2
        return 1
      fi
  
      if test ${#cmd_option_is_values[@]} -eq 0; then
        echo "$FUNC: option_is: missing values" >&2
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
      echo "$FUNC: argv[1]: invalid command" >&2
      return 1
      ;;
  esac
  
  # continuing setup....
  
  # ===========================================================================
  # Parsing of available options
  # ===========================================================================
  
  local -a   old_opts_with_arg=()   old_opts_with_optional_arg=()   old_opts_without_arg=()
  local -a  long_opts_with_arg=()  long_opts_with_optional_arg=()  long_opts_without_arg=()
  local -a short_opts_with_arg=() short_opts_with_optional_arg=() short_opts_without_arg=()
  
  local option=''
  for option in "${options[@]}"; do
    case "$option" in
      --?*=)    long_opts_with_arg+=("${option%=}");;
      --?*=\?)  long_opts_with_optional_arg+=("${option%=?}");;
      --?*)     long_opts_without_arg+=("$option");;
  
      -?=)      short_opts_with_arg+=("${option%=}");;
      -?=\?)    short_opts_with_optional_arg+=("${option%=?}");;
      -?)       short_opts_without_arg+=("$option");;
  
      -??*=)    old_opts_with_arg+=("${option%=}");;
      -??*=\?)  old_opts_with_optional_arg+=("${option%=?}");;
      -??*)     old_opts_without_arg+=("$option");;
  
      *) echo "$FUNC: $option: not a valid short, long or oldstyle option" >&2; return 1;;
    esac
  done
  
  # ===========================================================================
  # Parsing of command line options
  # ===========================================================================
  
  POSITIONALS=()
  HAVING_OPTIONS=()
  OPTION_VALUES=()
  
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
        if __zsh_query_contains "$arg" "${long_opts_with_arg[@]}"; then
          if $have_trailing_arg; then
            HAVING_OPTIONS+=("$arg")
            OPTION_VALUES+=("${@[$((argi + 1))]}")
            (( argi++ ))
          fi
        else
          HAVING_OPTIONS+=("$arg")
          OPTION_VALUES+=("")
        fi;;
      -*)
        local end_of_parsing=false

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
          fi
        elif __zsh_query_contains "$arg" "${old_opts_without_arg[@]}" "${old_opts_with_optional_arg[@]}"; then
          HAVING_OPTIONS+=("$arg")
          OPTION_VALUES+=("")
          end_of_parsing=true
        fi
  
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
            else if $have_trailing_arg
              HAVING_OPTIONS+=("$option")
              OPTION_VALUES+=("${@[$((argi + 1))]}")
              (( argi++ ))
            fi
          elif __zsh_query_contains "$option" "${short_opts_with_optional_arg[@]}"; then
            end_of_parsing=true
            HAVING_OPTIONS+=("$option")
            OPTION_VALUES+=("$trailing_chars") # may be empty
          fi

          (( i++ ))
        done;;
      *)
        POSITIONALS+=("$arg");;
    esac
  
    (( argi++ ))
  done
}

_exec() {
  local -a describe=()
  local line=''

  while IFS='' read -r line; do
    line="${line/:/\\:/}"
    line="${line/$'\t'/:}"
    describe+=("$line")
  done < <(eval "$1")

  _describe '' describe
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
test_case 32 -true  option_is -a --arg -arg -- foo bar :SETUP: "$opts" prog -a foo
test_case 33 -true  option_is -a --arg -arg -- foo bar :SETUP: "$opts" prog --arg foo
test_case 34 -true  option_is -a --arg -arg -- foo bar :SETUP: "$opts" prog -arg foo
test_case 41 -false option_is -a --arg -arg -- foo     :SETUP: "$opts" prog -flag
test_case 35 -true  option_is -o --optional -optional -- foo bar :SETUP: "$opts" prog -ofoo
test_case 36 -true  option_is -o --optional -optional -- foo bar :SETUP: "$opts" prog --optional=foo
test_case 37 -true  option_is -o --optional -optional -- foo bar :SETUP: "$opts" prog -optional=foo
test_case 38 -true  option_is -o --optional -optional -- foo bar :SETUP: "$opts" prog -obar
test_case 39 -true  option_is -o --optional -optional -- foo bar :SETUP: "$opts" prog --optional=bar
test_case 40 -true  option_is -o --optional -optional -- foo bar :SETUP: "$opts" prog -optional=bar
