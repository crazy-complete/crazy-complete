'''Code for parsing a command line in Bash.'''

from collections import namedtuple

from . import utils
from .str_utils import indent
from .bash_utils import CasePatterns
from .bash_parser_subcommand_code import (
    make_subcommand_switch_code, get_subcommand_path
)

_PARSER_CODE = '''\
POSITIONALS=()
END_OF_OPTIONS=0

local cmd="root" argi arg i char trailing_chars

for ((argi=1; argi < cword; ++argi)); do
  arg="${words_dequoted[argi]}"

  case "$arg" in
    --)
      END_OF_OPTIONS=1
      POSITIONALS+=("${words_dequoted[@]:$((++argi))}")
      return;;
    -?*) # ignore '-'
%LONG_OPTION_CASES%
      for ((i=1; i < ${#arg}; ++i)); do
        char="${arg:$i:1}"
        trailing_chars="${arg:$((i + 1))}"
%SHORT_OPTION_CASES%
      done;;
    *)
      POSITIONALS+=("$arg")
%SUBCOMMAND_SWITCH_CODE%
      ;;
  esac
done

for ((; argi <= cword; ++argi)); do
  case "${words_dequoted[argi]}" in
    -?*);;
    *) POSITIONALS+=("${words_dequoted[argi]}");;
  esac
done'''

_OPT_ISSET = '_OPT_ISSET_'


def generate(commandline, variable_manager):
    '''Generate code for parsing the command line.'''

    commandlines = list(reversed(commandline.get_all_commandlines()))
    subcommand_switch_code = make_subcommand_switch_code(commandline)
    long_option_cases = []
    short_option_cases = []

    for cmdline in commandlines:
        option_cases = _generate_option_cases(cmdline, variable_manager)
        command = get_subcommand_path(cmdline)
        if cmdline.inherit_options:
            command += '*'

        if option_cases.long_options:
            r = 'case "$cmd" in %s)\n' % command
            r += '  case "$arg" in\n'
            for case in option_cases.long_options:
                r += '%s\n' % indent(case, 4)
            r += '  esac\n'
            r += 'esac'
            long_option_cases.append(r)

        if option_cases.short_options:
            r = 'case "$cmd" in %s)\n' % command
            r += '  case "$char" in\n'
            for case in option_cases.short_options:
                r += '%s\n' % indent(case, 4)
            r += '  esac\n'
            r += 'esac'
            short_option_cases.append(r)

    s = _PARSER_CODE

    if long_option_cases:
        s = s.replace('%LONG_OPTION_CASES%',
                      indent('\n\n'.join(long_option_cases), 6))
    else:
        s = s.replace('%LONG_OPTION_CASES%\n', '')

    if short_option_cases:
        s = s.replace('%SHORT_OPTION_CASES%',
                      indent('\n\n'.join(short_option_cases), 8))
    else:
        s = s.replace('%SHORT_OPTION_CASES%\n', '')

    if subcommand_switch_code:
        s = s.replace('%SUBCOMMAND_SWITCH_CODE%',
                      indent(subcommand_switch_code, 6))
    else:
        s = s.replace('%SUBCOMMAND_SWITCH_CODE%\n', '')

    return s


def _make_long_option_case(long_options, option, variable):
    r = ''

    if option.has_optional_arg():
        r += '%s)\n'         % CasePatterns.for_long_without_arg(long_options)
        r += '  %s+=(%s);\n' % (variable, _OPT_ISSET)
        r += '  continue;;\n'
        r += '%s)\n'         % CasePatterns.for_long_with_arg(long_options)
        r += '  %s+=("${arg#*=}")\n' % variable
        r += '  continue;;'
    elif option.has_required_arg():
        r += '%s)\n'         % CasePatterns.for_long_without_arg(long_options)
        r += '  %s+=("${words_dequoted[++argi]}")\n' % variable
        r += '  continue;;\n'
        r += '%s)\n'         % CasePatterns.for_long_with_arg(long_options)
        r += '  %s+=("${arg#*=}")\n'        % variable
        r += '  continue;;'
    else:
        r += '%s)\n'        % CasePatterns.for_long_without_arg(long_options)
        r += '  %s+=(%s)\n' % (variable, _OPT_ISSET)
        r += '  continue;;'

    return r


def _make_short_option_case(short_options, option, variable):
    r = ''

    if option.has_optional_arg():
        r += '%s)\n' % CasePatterns.for_short(short_options)
        r += '  if [[ -n "$trailing_chars" ]]\n'
        r += '  then %s+=("$trailing_chars")\n' % variable
        r += '  else %s+=(%s)\n'                % (variable, _OPT_ISSET)
        r += '  fi\n'
        r += '  continue 2;;'
    elif option.has_required_arg():
        r += '%s)\n' % CasePatterns.for_short(short_options)
        r += '  if [[ -n "$trailing_chars" ]]\n'
        r += '  then %s+=("$trailing_chars")\n'            % variable
        r += '  else %s+=("${words_dequoted[++argi]}")\n'  % variable
        r += '  fi\n'
        r += '  continue 2;;'
    else:
        r += '%s)\n'        % CasePatterns.for_short(short_options)
        r += '  %s+=(%s);;' % (variable, _OPT_ISSET)

    return r


def _generate_option_cases(commandline, variable_manager):
    OptionCases = namedtuple('OptionCases', ['long_options', 'short_options'])
    options = commandline.get_options()
    abbreviations = utils.get_option_abbreviator(commandline)
    option_cases = OptionCases([], [])

    for option in options:
        short_options = option.get_short_option_strings()

        long_options = abbreviations.get_many_abbreviations(
                option.get_long_option_strings())

        long_options += abbreviations.get_many_abbreviations(
                option.get_old_option_strings())

        variable = variable_manager.capture_variable(option)

        if long_options:
            option_cases.long_options.append(
                _make_long_option_case(long_options, option, variable))

        if short_options:
            option_cases.short_options.append(
                _make_short_option_case(short_options, option, variable))

    return option_cases
