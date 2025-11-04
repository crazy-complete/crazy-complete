'''Code for generating a Bash auto completion file.'''

from collections import OrderedDict

from . import config as config_
from . import shell
from . import algo
from . import utils
from . import helpers
from . import bash_helpers
from . import bash_complete
from . import bash_parser
from . import bash_parser_v2
from . import bash_option_completion
from . import bash_option_strings_completion
from . import bash_positionals_completion
from . import bash_versions
from . import bash_patterns
from .str_utils import indent, join_with_wrap
from .bash_utils import VariableManager
from .output import Output
from . import generation


class BashCompletionGenerator:
    '''Class for generating completions.'''

    # pylint: disable=too-few-public-methods
    # pylint: disable=too-many-instance-attributes

    def __init__(self, ctxt, commandline):
        self.ctxt = ctxt
        self.commandline = commandline
        self.options = commandline.get_options()
        self.positionals = commandline.get_positionals()
        self.subcommands = commandline.get_subcommands()
        self.completer = bash_complete.BashCompleter()
        self.variable_manager = VariableManager('OPT_')
        self._generate()

    def complete_option(self, option):
        '''Complete an option.'''
        context = self.ctxt.get_option_context(self.commandline, option)
        obj = self.completer.complete(context, [], *option.complete)
        code = obj.get_code(False)
        if code and option.nosort:
            code += '\ncompopt -o nosort'
        return code

    def _generate_commandline_parsing(self):
        local_vars = []
        for cmdline in self.commandline.get_all_commandlines():
            for option in cmdline.options:
                if option.capture is not None:
                    local_vars.append(option.capture)

        r = 'local END_OF_OPTIONS POSITIONALS\n'

        if local_vars:
            local_vars = algo.uniq(local_vars)
            line_length = self.ctxt.config.line_length - 2
            r += join_with_wrap(' ', '\n', line_length, local_vars, 'local -a')

        r += '\n%s' % self.ctxt.helpers.use_function('parse_commandline')
        return r

    def _generate_subcommand_call(self):
        if not self.subcommands:
            return None

        positional_num = self.subcommands.get_positional_num()
        r  = 'if (( %i < ${#POSITIONALS[@]} )); then\n' % (positional_num - 1)
        r += '  case "${POSITIONALS[%i]}" in\n' % (positional_num - 1)
        for subcommand in self.subcommands.subcommands:
            cmds = utils.get_all_command_variations(subcommand)
            pattern = bash_patterns.make_pattern([shell.quote(s) for s in cmds])
            funcname = self.ctxt.helpers.make_completion_funcname(subcommand)
            if utils.is_worth_a_function(subcommand):
                if self.commandline.inherit_options:
                    r += '    %s) %s && return 0;;\n' % (pattern, funcname)
                else:
                    r += '    %s) %s && return 0 || return 1;;\n' % (pattern, funcname)
            else:
                if self.commandline.inherit_options:
                    r += '    %s);;\n' % pattern
                else:
                    r += '    %s) return 0;;\n' % pattern
        r += '  esac\n'
        r += 'fi'
        return r

    def _generate_command_arg_call(self):
        def is_command_arg(positional):
            return (positional.complete and
                    positional.complete[0] == 'command_arg')

        try:
            positional = list(filter(is_command_arg, self.positionals))[0]
        except IndexError:
            return None

        num = positional.get_positional_num()
        r  = 'if (( ${#POSITIONALS[@]} >= %d )); then\n' % num
        r += '  local realpos\n'
        r += '  for realpos in "${!COMP_WORDS[@]}"; do\n'
        r += '    [[ "${COMP_WORDS[realpos]}" == "${POSITIONALS[%d]}" ]] && {\n' % (num - 2)
        r += '      %s $realpos\n' % bash_versions.command_offset(self.ctxt)
        r += '      return 0;\n'
        r += '    }\n'
        r += '  done\n'
        r += 'fi'
        return r

    def _generate(self):
        # The completion function returns 0 (success) if there was a completion match.
        # This return code is used for dealing with subcommands.

        if not utils.is_worth_a_function(self.commandline):
            self.result = ''
            return

        code = OrderedDict()
        code['init_completion'] = None
        code['command_line_parsing'] = None
        code['subcommand_call'] = None
        code['command_arg'] = None
        code['option_completion'] = None
        code['option_strings_completion'] = None
        code['positional_completion'] = None

        code['subcommand_call'] = self._generate_subcommand_call()
        code['command_arg'] = self._generate_command_arg_call()
        code['option_completion'] = bash_option_completion.generate_option_completion(self)
        code['option_strings_completion'] = bash_option_strings_completion.generate(self)
        code['positional_completion'] = bash_positionals_completion.generate(self)

        if self.commandline.parent is None:
            # The root parser makes those variables local and sets up the completion.
            r  = 'local cur prev words cword split words_dequoted\n'
            r += '%s -n =: || return\n' % bash_versions.init_completion(self.ctxt)
            r += self.ctxt.helpers.use_function('dequote_words')
            code['init_completion'] = r

            v1 = bash_parser.generate(self.commandline, self.variable_manager)
            v2 = bash_parser_v2.generate(self.commandline, self.variable_manager)
            c  = v1 if len(v1) < len(v2) else v2

            func = helpers.ShellFunction('parse_commandline', c)
            self.ctxt.helpers.add_function(func)

            # This sets up END_OF_OPTIONS, POSITIONALS and the OPT_* variables.
            code['command_line_parsing'] = self._generate_commandline_parsing()

        r  = '%s() {\n' % self.ctxt.helpers.make_completion_funcname(self.commandline)
        r += '%s\n\n'   % indent('\n\n'.join(c for c in code.values() if c), 2)
        r += '  return 1\n'
        r += '}'

        self.result = r


def _generate_wrapper(ctxt, commandline):
    make_completion_funcname = ctxt.helpers.make_completion_funcname
    completion_funcname = make_completion_funcname(commandline)
    wrapper_funcname = make_completion_funcname(commandline, '__wrapper')

    if not commandline.wraps:
        return (completion_funcname, None)

    r  = '%s %s\n' % (bash_versions.completion_loader(ctxt), commandline.wraps)
    r += '\n'
    r += '%s() {\n' % wrapper_funcname
    r += '  local WRAPS=%s\n' % shell.quote(commandline.wraps)
    r += '  local COMP_LINE_OLD="$COMP_LINE"\n'
    r += '  local COMP_POINT_OLD="$COMP_POINT"\n'
    r += '  local COMP_WORDS_OLD=("${COMP_WORDS[@]}")\n'
    r += '\n'
    r += '  COMP_LINE="${COMP_LINE/$1/$WRAPS}"\n'
    r += '  COMP_WORDS[0]=%s\n' % shell.quote(commandline.wraps)
    r += '  COMP_POINT=$(( COMP_POINT + ${#WRAPS} - ${#1} ))\n'
    r += '\n'
    r += '  %s 0\n' % bash_versions.command_offset(ctxt)
    r += '\n'
    r += '  COMP_LINE="$COMP_LINE_OLD"\n'
    r += '  COMP_POINT="$COMP_POINT_OLD"\n'
    r += '  COMP_WORDS=("${COMP_WORDS_OLD[@]}")\n'
    r += '  local COMPREPLY_OLD=("${COMPREPLY[@]}")\n'
    r += '  %s "$@"\n' % completion_funcname
    r += '\n'
    r += '  COMPREPLY=("${COMPREPLY_OLD[@]}" "${COMPREPLY[@]}")\n'
    r += '}'

    return (wrapper_funcname, r)


def generate_completion(commandline, config=None):
    '''Code for generating a Bash auto completion file.'''

    if config is None:
        config = config_.Config()

    commandline = generation.enhance_commandline(commandline, config)
    helpers = bash_helpers.BashHelpers(config, commandline.prog)
    ctxt = generation.GenerationContext(config, helpers)

    if ctxt.config.bash_completions_version >= (2, 12):
        helpers.define('bash_completions_v_2_12')

    result = generation.visit_commandlines(BashCompletionGenerator, ctxt, commandline)

    completion_func, wrapper_code = _generate_wrapper(ctxt, commandline)

    output = Output(config, helpers)
    output.add_generation_notice()
    output.add_comments()
    output.add_included_files()
    output.add_helper_functions_code()
    output.extend(generator.result for generator in result)
    output.add(wrapper_code)
    output.add('complete -F %s %s' % (
        completion_func, ' '.join([commandline.prog] + commandline.aliases)
    ))
    output.add_vim_modeline('sh')

    return output.get()
