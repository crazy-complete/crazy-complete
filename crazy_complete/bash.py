'''Code for generating a bash auto completion file.'''

from collections import OrderedDict

from . import config as config_
from . import generation_notice
from . import modeline
from . import shell
from . import algo
from . import utils
from . import helpers
from . import bash_helpers
from . import bash_complete
from . import bash_parser
from . import bash_parser_v2
from . import bash_option_completion
from . import bash_when
from .str_utils import indent
from .bash_utils import VariableManager
from . import generation

class BashCompletionGenerator:
    def __init__(self, ctxt, commandline):
        self.commandline = commandline
        self.ctxt        = ctxt
        self.options     = commandline.get_options()
        self.positionals = commandline.get_positionals()
        self.subcommands = commandline.get_subcommands_option()
        self.completer   = bash_complete.BashCompleter()
        self.variable_manager = VariableManager('OPT_')
        self._generate()

    def _complete_option(self, option, append=True):
        context = self.ctxt.get_option_context(self.commandline, option)
        return self.completer.complete(context, *option.complete).get_code(append)

    def _generate_commandline_parsing(self):
        options = self.commandline.get_options(with_parent_options=True)

        r = 'local END_OF_OPTIONS POSITIONALS POSITIONAL_NUM\n'

        if options:
            local_vars = [self.variable_manager.make_variable(o) for o in options]
            r += 'local -a %s\n' % ' '.join(local_vars)

        r +=  '\n%s' % self.ctxt.helpers.use_function('parse_commandline')
        return r

    def _generate_option_strings_completion(self):
        def make_option_strings(option):
            r = []
            for option_string in option.option_strings:
                if len(option_string) != 2 and option.complete:
                    r.append(f'{option_string}=')
                else:
                    r.append(option_string)
            return ' '.join(shell.escape(option_string) for option_string in r)

        r  = 'if (( ! END_OF_OPTIONS )) && [[ "$cur" = -* ]]; then\n'
        r += '  local -a opts\n'
        for option in self.options:
            if option.hidden:
                continue

            conditions = []

            for final_option in self.commandline.get_final_options():
                conditions += ["! ${#%s[@]}" % self.variable_manager.make_variable(final_option)]

            for exclusive_option in option.get_conflicting_options():
                conditions += ["! ${#%s[@]}" % self.variable_manager.make_variable(exclusive_option)]

            if not option.repeatable:
                conditions += ["! ${#%s[@]}" % self.variable_manager.make_variable(option)]

            if conditions:
                conditions = '(( %s )) && ' % ' && '.join(algo.uniq(conditions))
            else:
                conditions = ''

            when_guard = ''
            if option.when is not None:
                when_guard = bash_when.generate_when_conditions(self.commandline, self.variable_manager, option.when)
                when_guard = '%s && ' % when_guard

            r += '  %s%sopts+=(%s)\n' % (conditions, when_guard, make_option_strings(option))

        r += '  COMPREPLY+=($(compgen -W "${opts[*]}" -- "$cur"))\n'
        r += '  [[ ${COMPREPLY-} == *= ]] && compopt -o nospace\n'
        r += '  return 1\n'
        r += 'fi'
        return r

    def _generate_positionals_completion(self):
        def make_block(code):
            if code:
                return '{\n%s\n  return 0;\n}' % indent(code, 2)
            else:
                return '{\n  return 0;\n}'

        r = ''
        for positional in self.positionals:
            operator = '=='
            if positional.repeatable:
                operator = '>='
            r += '(( POSITIONAL_NUM %s %d )) && ' % (operator, positional.get_positional_num())
            if positional.when:
                r += '%s && ' % bash_when.generate_when_conditions(self.commandline, self.variable_manager, positional.when)
            r += '%s\n\n' % make_block(self._complete_option(positional, False))

        if self.subcommands:
            cmds = self.subcommands.get_choices().keys()
            complete = self.completer.choices(self.ctxt, cmds).get_code()
            r += '(( POSITIONAL_NUM == %d )) && ' % self.subcommands.get_positional_num()
            r += '%s\n\n' % make_block(complete)
        return r.strip()

    def _generate_subcommand_call(self):
        # This code is used to call subcommand functions

        r  = 'if (( %i < POSITIONAL_NUM )); then\n' % (self.subcommands.get_positional_num() - 1)
        r += '  case "${POSITIONALS[%i]}" in\n' % (self.subcommands.get_positional_num() - 1)
        for subcommand in self.subcommands.subcommands:
            cmds = utils.get_all_command_variations(subcommand)
            pattern = '|'.join(shell.escape(s) for s in cmds)
            if self.commandline.inherit_options:
                r += '    %s) %s && return 0;;\n' % (pattern, shell.make_completion_funcname(subcommand))
            else:
                r += '    %s) %s && return 0 || return 1;;\n' % (pattern, shell.make_completion_funcname(subcommand))
        r += '  esac\n'
        r += 'fi'
        return r

    def _generate(self):
        # The completion function returns 0 (success) if there was a completion match.
        # This return code is used for dealing with subcommands.

        if not utils.is_worth_a_function(self.commandline):
            r  = '%s() {\n' % shell.make_completion_funcname(self.commandline)
            r += '  return 0\n'
            r += '}'
            self.result = r
            return

        code = OrderedDict()

        if self.commandline.parent is None:
            # The root parser makes those variables local and sets up the completion.
            r  = 'local cur prev words cword split\n'
            r += '_init_completion -n = || return'
            code['init_completion'] = r

            v1 = bash_parser.generate(self.commandline)
            v2 = bash_parser_v2.generate(self.commandline)
            c  = v1 if len(v1) < len(v2) else v2

            func = helpers.ShellFunction('parse_commandline', c)
            self.ctxt.helpers.add_function(func)

        # Here we want to parse commandline options. We set this to None because
        # we have to delay this call for collecting info.
        code['command_line_parsing'] = None

        code['set_wordbreaks'] = "local COMP_WORDBREAKS=''"

        if self.subcommands:
            code['subcommand_call'] = self._generate_subcommand_call()

        if len(self.options):
            # This code is used to complete arguments of options
            code['option_completion'] = bash_option_completion.generate_option_completion(self)

            # This code is used to complete option strings (--foo, ...)
            code['option_strings_completion'] = self._generate_option_strings_completion()

        if len(self.positionals) or self.subcommands:
            # This code is used to complete positionals
            code['positional_completion'] = self._generate_positionals_completion()

        # This sets up END_OF_OPTIONS, POSITIONALS, POSITIONAL_NUM and the OPT_* variables.
        code['command_line_parsing'] = self._generate_commandline_parsing()

        r  = '%s() {\n' % shell.make_completion_funcname(self.commandline)
        r += '%s\n\n'   % indent('\n\n'.join(c for c in code.values() if c), 2)
        r += '  return 1\n'
        r += '}'

        self.result = r

def generate_completion(commandline, config=None):
    '''Code for generating a Bash auto completion file.'''

    if config is None:
        config = config_.Config()

    commandline = generation.enhance_commandline(commandline, config)
    helpers = bash_helpers.BashHelpers(commandline.prog)
    ctxt = generation.GenerationContext(config, helpers)
    result = generation.visit_commandlines(BashCompletionGenerator, ctxt, commandline)

    output = []
    output += [generation_notice.GENERATION_NOTICE]
    output += config.get_included_files_content()
    output += helpers.get_used_functions_code()
    output += [generator.result for generator in result]
    output += ['complete -F %s %s' % (
        shell.make_completion_funcname(commandline),
        ' '.join([commandline.prog] + commandline.aliases)
    )]

    if config.vim_modeline:
        output += [modeline.get_vim_modeline('sh')]

    return '\n\n'.join(output)
