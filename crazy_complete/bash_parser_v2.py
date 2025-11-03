'''Code for parsing a command line in Bash, version 2'''

from collections import namedtuple

from . import utils
from . import shell
from . import bash_patterns
from .str_utils import indent
from .bash_parser_subcommand_code import (
    make_subcommand_switch_code, get_subcommand_path
)
from .preprocessor import preprocess

_PARSER_CODE = '''\
#ifdef positionals
POSITIONALS=()
#endif
END_OF_OPTIONS=0

local cmd="root" argi arg i char trailing_chars VAR ARGS

%FIND_OPTION_CODE%

__append_to_array() {
  local -n arr=$1
  arr+=("$2")
}

for ((argi=1; argi < cword; ++argi)); do
  arg="${words_dequoted[argi]}"

  case "$arg" in
    --)
      END_OF_OPTIONS=1
#ifdef positionals
      POSITIONALS+=("${words_dequoted[@]:$((++argi))}")
#endif
      return;;
#ifdef long_options
    --*=*)
      if __find_option "$cmd" "${arg%%=*}"
      then __append_to_array "$VAR" "${arg#*=}"
      fi;;
    --*)
      if __find_option "$cmd" "$arg"; then
        if [[ "$ARGS" == 1 ]]
        then __append_to_array "$VAR" "${words_dequoted[++argi]}"
        else __append_to_array "$VAR" "_OPT_ISSET_"
        fi
      fi;;
#else
    --*);;
#endif
    -?*) # ignore '-'
#ifdef old_options
      if [[ "$arg" == -*=* ]]; then
        if __find_option "$cmd" "${arg%%=*}"; then
          __append_to_array "$VAR" "${arg#*=}"
          continue
        fi
      fi

      if __find_option "$cmd" "$arg"; then
        if [[ "$ARGS" == 1 ]]
        then __append_to_array "$VAR" "${words_dequoted[++argi]}"
        else __append_to_array "$VAR" "_OPT_ISSET_"
        fi

        continue
      fi
#endif

#ifdef short_options
      for ((i=1; i < ${#arg}; ++i)); do
        char="${arg:$i:1}"
        trailing_chars="${arg:$((i + 1))}"

        if __find_option "$cmd" "-$char"; then
          if [[ "$ARGS" == 1 ]]; then
            if [[ -n "$trailing_chars" ]]
            then __append_to_array "$VAR" "$trailing_chars"
            else __append_to_array "$VAR" "${words_dequoted[++argi]}"
            fi
            break;
#ifdef short_optionals
          elif [[ "$ARGS" == '?' ]]; then
            if [[ -n "$trailing_chars" ]]
            then __append_to_array "$VAR" "$trailing_chars"
            else __append_to_array "$VAR" _OPT_ISSET_
            fi
            break;
#endif
          else
            __append_to_array "$VAR" "_OPT_ISSET_"
          fi
        fi
      done
#endif
      ;;
#ifdef positionals
    *)
      POSITIONALS+=("$arg")
%SUBCOMMAND_SWITCH_CODE%
      ;;
#endif
  esac
done
#ifdef positionals

for ((; argi <= cword; ++argi)); do
  case "${words_dequoted[argi]}" in
    -?*);;
    *) POSITIONALS+=("${words_dequoted[argi]}");;
  esac
done
#endif'''

_OPT_ISSET = '_OPT_ISSET_'


def _make_find_option_code(commandline, variable_manager):
    cmdlines = list(reversed(commandline.get_all_commandlines()))
    code = []

    if len(cmdlines) == 1:
        code += [_make_cmd_plus_option_switch_code(cmdlines[0], variable_manager, True)]
    else:
        for cmdline in cmdlines:
            code += [_make_cmd_plus_option_switch_code(cmdline, variable_manager)]

    c =  '__find_option() {\n'
    c += '%s\n' % indent('\n'.join(filter(None, code)), 2)
    c += '  return 1\n'
    c += '}'

    return c


def _make_cmd_plus_option_switch_code(commandline, variable_manager, omit_cmd_check=False):
    option_cases = _generate_option_cases(commandline, variable_manager)
    if not option_cases:
        return None

    if omit_cmd_check:
        return _make_option_switch_code(option_cases)

    command = get_subcommand_path(commandline)
    command = shell.quote(command)
    if commandline.inherit_options:
        command += '*'

    c  = f'case "$1" in {command})\n'
    c += '%s\n' % indent(_make_option_switch_code(option_cases), 2)
    c += 'esac'
    return c


def _make_option_switch_code(option_cases):
    c  = 'case "$2" in\n'

    for case in option_cases:
        c += '  %s)'        % bash_patterns.make_pattern(case.option_strings)
        c += ' VAR=%s;'     % case.variable
        c += ' ARGS=%s;'    % case.args
        c += ' return;;\n'

    c += 'esac'
    return c


def generate(commandline, variable_manager):
    '''Generate code for parsing the command line.'''

    find_option_code = _make_find_option_code(commandline, variable_manager)
    subcommand_switch_code = make_subcommand_switch_code(commandline)

    defines = []
    types = utils.get_defined_option_types(commandline)
    if types.short:
        defines.append('short_options')
    if types.long:
        defines.append('long_options')
    if types.old:
        defines.append('old_options')
    if types.short_optional:
        defines.append('short_optionals')
    if types.positionals:
        defines.append('positionals')

    s = preprocess(_PARSER_CODE, defines)

    if subcommand_switch_code:
        s = s.replace('%SUBCOMMAND_SWITCH_CODE%', indent(subcommand_switch_code, 6))
    else:
        s = s.replace('%SUBCOMMAND_SWITCH_CODE%\n', '')

    if find_option_code:
        s = s.replace('%FIND_OPTION_CODE%', find_option_code)
    else:
        s = s.replace('%FIND_OPTION_CODE%\n', '')

    return s


def _generate_option_cases(commandline, variable_manager):
    OptionCase = namedtuple('OptionCase', ['option_strings', 'variable', 'args'])
    options = commandline.get_options()
    abbreviations = utils.get_option_abbreviator(commandline)
    option_cases = []

    for option in options:
        long_options  = abbreviations.get_many_abbreviations(option.get_long_option_strings())
        long_options += abbreviations.get_many_abbreviations(option.get_old_option_strings())
        short_options = option.get_short_option_strings()

        value_variable = variable_manager.capture_variable(option)

        if option.complete and option.optional_arg is True:
            args = "'?'"
        elif option.complete:
            args = '1'
        else:
            args = '0'

        option_cases.append(OptionCase(short_options + long_options, value_variable, args))

    return option_cases
