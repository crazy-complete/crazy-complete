'''Code for parsing a command line in Bash.'''

from collections import namedtuple

from . import utils
from . import shell
from .bash_utils import *

_PARSER_CODE = '''\
POSITIONALS=()
END_OF_OPTIONS=0
POSITIONAL_NUM=0

local cmd="${words[0]}" argi arg i char trailing_chars

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
    -*)
%LONG_OPTION_CASES%
      for ((i=1; i < ${#arg}; ++i)); do
        char="${arg:$i:1}"
        trailing_chars="${arg:$((i + 1))}"
%SHORT_OPTION_CASES%
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
    -) POSITIONALS[POSITIONAL_NUM++]="$arg";;
    -*);;
    *) POSITIONALS[POSITIONAL_NUM++]="$arg";;
  esac
done'''

_OPT_ISSET = '_OPT_ISSET_'

def generate(commandline):
    commandlines = []
    commandline.visit_commandlines(lambda o: commandlines.append(o))
    commandlines = reversed(commandlines)

    long_option_cases = []
    short_option_cases = []
    subcommand_call_code = []

    for commandline in commandlines:
        option_cases = generate_option_cases(commandline)
        command = shell.escape(commandline.get_command_path())
        if commandline.inherit_options:
            command += '*'

        if option_cases.long_options:
            r =  'case "$cmd" in %s)\n' % command
            r += '  case "$arg" in\n'
            for case in option_cases.long_options:
                r += '%s\n' % utils.indent(case, 4)
            r += '  esac\n'
            r += 'esac'
            long_option_cases.append(r)

        if option_cases.short_options:
            r =  'case "$cmd" in %s)\n' % command
            r += '  case "$char" in\n'
            for case in option_cases.short_options:
                r += '%s\n' % utils.indent(case, 4)
            r += '  esac\n'
            r += 'esac'
            short_option_cases.append(r)

        if commandline.get_subcommands_option():
            positional_num = commandline.get_subcommands_option().get_positional_num()
            r =  'if (( POSITIONAL_NUM == %d )); then\n' % positional_num
            r += '  case "$arg" in\n'
            for subcommand in commandline.get_subcommands_option().subcommands:
                r += '    %s)\n' % '|'.join(utils.get_all_command_variations(subcommand))
                r += '      cmd+=" %s";;\n' % subcommand.prog
            r += '    *) cmd+=" $arg";;\n'
            r += '  esac\n'
            r += 'fi'
            subcommand_call_code.append(r)

    s = _PARSER_CODE

    if long_option_cases:
        s = s.replace('%LONG_OPTION_CASES%',
            utils.indent('\n\n'.join(long_option_cases), 6))
    else:
        s = s.replace('%LONG_OPTION_CASES%\n', '')

    if short_option_cases:
        s = s.replace('%SHORT_OPTION_CASES%',
            utils.indent('\n\n'.join(short_option_cases), 8))
    else:
        s = s.replace('%SHORT_OPTION_CASES%\n', '')

    if subcommand_call_code:
        s = s.replace('%SUBCOMMAND_SWITCH_CODE%',
            utils.indent('\n\n'.join(subcommand_call_code), 6))
    else:
        s = s.replace('%SUBCOMMAND_SWITCH_CODE%\n', '')

    return s

def make_long_option_case(
        long_options,
        complete,
        optional_arg,
        value_variable):
    r = ''

    if complete and optional_arg is True:
        r += '%s)\n'                        % CasePatterns.for_long_without_arg(long_options)
        r += '  %s+=(%s);\n'                % (value_variable, _OPT_ISSET)
        r += '  continue;;\n'
        r += '%s)\n'                        % CasePatterns.for_long_with_arg(long_options)
        r += '  %s+=("${arg#*=}")\n'        % value_variable
        r += '  continue;;'
    elif complete:
        r += '%s)\n'                        % CasePatterns.for_long_without_arg(long_options)
        r += '  %s+=("${words[++argi]}")\n' % value_variable
        r += '  continue;;\n'
        r += '%s)\n'                        % CasePatterns.for_long_with_arg(long_options)
        r += '  %s+=("${arg#*=}")\n'        % value_variable
        r += '  continue;;'
    else:
        r += '%s)\n'        % CasePatterns.for_long_without_arg(long_options)
        r += '  %s+=(%s)\n' % (value_variable, _OPT_ISSET)
        r += '  continue;;'

    return r

def make_short_option_case(
        short_options,
        complete,
        optional_arg,
        value_variable):
    r = ''

    if complete and optional_arg is True:
        r += '%s)\n'    % CasePatterns.for_short(short_options)
        r += '  if [[ -n "$trailing_chars" ]]\n'
        r += '  then %s+=("$trailing_chars")\n' % value_variable
        r += '  else %s+=(%s)\n'                % (value_variable,_OPT_ISSET)
        r += '  fi\n'
        r += '  continue 2;;'
    elif complete:
        r += '%s)\n'    % CasePatterns.for_short(short_options)
        r += '  if [[ -n "$trailing_chars" ]]\n'
        r += '  then %s+=("$trailing_chars")\n'   % value_variable
        r += '  else %s+=("${words[++argi]}")\n'  % value_variable
        r += '  fi\n'
        r += '  continue 2;;'
    else:
        r += '%s)\n'        % CasePatterns.for_short(short_options)
        r += '  %s+=(%s);;' % (value_variable, _OPT_ISSET)

    return r

def generate_option_cases(commandline):
    OptionCases = namedtuple('OptionCases', ['long_options', 'short_options'])
    options = commandline.get_options()

    if commandline.abbreviate_options:
        abbreviations = get_OptionAbbreviationGenerator(options)
    else:
        abbreviations = utils.DummyAbbreviationGenerator()

    option_cases = OptionCases([], [])

    for option in options:
        long_options  = abbreviations.get_many_abbreviations(option.get_long_option_strings())
        long_options += abbreviations.get_many_abbreviations(option.get_old_option_strings())
        short_options = option.get_short_option_strings()

        value_variable = make_option_variable_name(option, prefix='OPT_')

        if long_options:
            option_cases.long_options.append(
                make_long_option_case(long_options, option.complete, option.optional_arg, value_variable))

        if short_options:
            option_cases.short_options.append(
                make_short_option_case(short_options, option.complete, option.optional_arg, value_variable))

    return option_cases
