'''Code for parsing a command line in Bash, version 2'''

from collections import namedtuple

from . import utils
from .str_utils import indent
from .bash_utils import make_option_variable_name
from .bash_parser_subcommand_code import make_subcommand_call_code, get_subcommand_path

_PARSER_CODE = '''\
POSITIONALS=()
END_OF_OPTIONS=0
POSITIONAL_NUM=0

local cmd="root" argi arg i char trailing_chars
local ARG_NONE=0 ARG_REQUIRED=1 ARG_OPTIONAL=2 VAR MODE

%FIND_OPTION_CODE%

__append_to_array() {
  local -n arr=$1
  arr+=("$2")
}

for ((argi=1; argi < ${#words[@]} - 1; ++argi)); do
  arg="${words[argi]}"

  case "$arg" in
    --)
      END_OF_OPTIONS=1
      for ((++argi; argi < ${#words[@]}; ++argi)); do
        POSITIONALS[POSITIONAL_NUM++]="${words[argi]}"
      done
      break;;
    -)
      POSITIONALS[POSITIONAL_NUM++]="-";;
    --*=*)
      if __find_option "$cmd" "${arg%%=*}"
      then __append_to_array "$VAR" "${arg#*=}"
      fi;;
    --*)
      if __find_option "$cmd" "$arg"; then
        if (( MODE == ARG_REQUIRED ))
        then __append_to_array "$VAR" "${words[++argi]}"
        else __append_to_array "$VAR" "_OPT_ISSET_"
        fi
      fi;;
    -*)
      if [[ "$arg" == -*=* ]]; then
        if __find_option "$cmd" "${arg%%=*}"; then
          __append_to_array "$VAR" "${arg#*=}"
          continue
        fi
      fi

      if __find_option "$cmd" "$arg"; then
        if (( MODE == ARG_REQUIRED ));
        then __append_to_array "$VAR" "${words[++argi]}"
        else __append_to_array "$VAR" "_OPT_ISSET_"
        fi

        continue
      fi

      for ((i=1; i < ${#arg}; ++i)); do
        char="${arg:$i:1}"
        trailing_chars="${arg:$((i + 1))}"

        if __find_option "$cmd" "-$char"; then
          if (( MODE == ARG_REQUIRED )); then
            if [[ -n "$trailing_chars" ]]
            then __append_to_array "$VAR" "$trailing_chars"
            else __append_to_array "$VAR" "${words[++argi]}"
            fi
            break;
          elif (( MODE == ARG_OPTIONAL )); then
            if [[ -n "$trailing_chars" ]]
            then __append_to_array "$VAR" "$trailing_chars"
            else __append_to_array "$VAR" _OPT_ISSET_
            fi
            break;
          else
            __append_to_array "$VAR" "_OPT_ISSET_"
          fi
        fi
      done;;
    *)
      POSITIONALS[POSITIONAL_NUM++]="$arg"
%SUBCOMMAND_SWITCH_CODE%
      ;;
  esac
done

for ((; argi < ${#words[@]}; ++argi)); do
  arg="${words[$argi]}"

  case "$arg" in
    -) POSITIONALS[POSITIONAL_NUM++]="-";;
    -*);;
    *) POSITIONALS[POSITIONAL_NUM++]="$arg";;
  esac
done'''

_OPT_ISSET = '_OPT_ISSET_'

def _make_find_option_code(commandline):
    c = '__find_option() {\n'

    for commandline in reversed(commandline.get_all_commandlines()):
        option_cases = generate_option_cases(commandline)
        command = get_subcommand_path(commandline)
        if commandline.inherit_options:
            command += '*'

        c += f'  case "$1" in "{command}")\n'
        c +=  '    case "$2" in\n'

        for case in option_cases:
            c += '      %s) VAR=%s; MODE=%s; return;;\n' % (
                '|'.join(case.option_strings),
                case.variable,
                case.mode)

        c += '    esac\n'
        c += '  esac\n'

    c += '  return 1\n'
    c += '}'

    return c

def generate(commandline):
    find_option_code     = _make_find_option_code(commandline)
    subcommand_call_code = make_subcommand_call_code(commandline)

    s = _PARSER_CODE

    if subcommand_call_code:
        s = s.replace('%SUBCOMMAND_SWITCH_CODE%', indent(subcommand_call_code, 6))
    else:
        s = s.replace('%SUBCOMMAND_SWITCH_CODE%\n', '')

    if find_option_code:
        s = s.replace('%FIND_OPTION_CODE%', find_option_code)
    else:
        s = s.replace('%FIND_OPTION_CODE%\n', '')

    return s

def generate_option_cases(commandline):
    OptionCase = namedtuple('OptionCase', ['option_strings', 'variable', 'mode'])
    options = commandline.get_options()
    abbreviations = utils.get_option_abbreviator(commandline)
    option_cases = []

    for option in options:
        long_options  = abbreviations.get_many_abbreviations(option.get_long_option_strings())
        long_options += abbreviations.get_many_abbreviations(option.get_old_option_strings())
        short_options = option.get_short_option_strings()

        value_variable = make_option_variable_name(option, prefix='OPT_')

        if option.complete and option.optional_arg is True:
            mode = '$ARG_OPTIONAL'
        elif option.complete:
            mode = '$ARG_REQUIRED'
        else:
            mode = '$ARG_NONE'

        option_cases.append(OptionCase(short_options + long_options, value_variable, mode))

    return option_cases
