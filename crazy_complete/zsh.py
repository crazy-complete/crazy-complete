'''Code for generating a Zsh auto completion file.'''

from collections import namedtuple, OrderedDict

from . import config as config_
from . import generation
from . import generation_notice
from . import modeline
from . import shell
from . import utils
from . import zsh_complete
from . import zsh_helpers
from . import zsh_utils
from .str_utils import indent

Arg = namedtuple('Arg', ('option', 'when', 'hidden', 'option_spec'))

class ZshQuery:
    '''Helper class for using the `zsh_query` function.'''

    def __init__(self, ctxt):
        self.ctxt = ctxt
        self.used = False

    def use(self, define=None):
        self.used = True
        return self.ctxt.helpers.use_function('zsh_query', define)

    def use_when(self, when):
        if 'option_is' in when:
            self.use('option_is')
        if 'has_option' in when:
            self.use('has_option')
        return self.use()

class ZshCompletionFunction:
    '''Class for generating a zsh completion function.'''

    # pylint: disable=too-many-branches
    # pylint: disable=too-few-public-methods
    # pylint: disable=too-many-instance-attributes

    def __init__(self, ctxt, commandline):
        self.commandline = commandline
        self.ctxt = ctxt
        self.funcname = shell.make_completion_funcname(commandline)
        self.subcommands = commandline.get_subcommands_option()
        self.command_counter = 0
        self.completer = zsh_complete.ZshCompleter()
        self.code = None
        self.query = ZshQuery(ctxt)
        self._generate_completion_code()

    def _complete(self, option, command, *args):
        context = self.ctxt.get_option_context(self.commandline, option)
        return self.completer.complete(context, command, *args)

    def _complete_option(self, option):
        if option.complete:
            action = self._complete(option, *option.complete)
        else:
            action = None

        option_spec = zsh_utils.make_option_spec(
            option.option_strings,
            conflicting_options = option.get_conflicting_option_strings(),
            description = option.help,
            complete = option.complete,
            optional_arg = option.optional_arg,
            repeatable = option.repeatable,
            final = option.final,
            metavar = option.metavar,
            action = action
        )

        return Arg(option, option.when, option.hidden, option_spec)

    def _complete_subcommands(self, option):
        choices = option.get_choices()
        self.command_counter += 1

        option_spec = "%d:command%d:%s" % (
            option.get_positional_num(),
            self.command_counter,
            self._complete(option, 'choices', choices)
        )

        return Arg(option, None, False, option_spec)

    def _complete_positional(self, option):
        positional_num = option.get_positional_num()
        if option.repeatable:
            positional_num = "'*'"

        option_spec = "%s:%s:%s" % (
            positional_num,
            shell.escape(zsh_utils.escape_colon(option.help or option.metavar or ' ')),
            self._complete(option, *option.complete)
        )

        return Arg(option, option.when, False, option_spec)

    def _generate_completion_code(self):
        self.code = OrderedDict()
        self.code['0-init']        = ''
        self.code['1-capture']     = ''
        self.code['2-subcommands'] = ''
        self.code['3-options']     = ''

        # We have to call these functions first, because they tell us if
        # the zsh_query function is used.
        self.code['1-capture']     = self._generate_option_capture()
        self.code['2-subcommands'] = self._generate_subcommand_call()
        self.code['3-options']     = self._generate_option_parsing()

        if self.query.used:
            r  = 'local opts=%s\n' % shell.escape(utils.get_query_option_strings(self.commandline))
            r += "local HAVING_OPTIONS=() OPTION_VALUES=() POSITIONALS=() INCOMPLETE_OPTION=''\n"
            r += '%s init "$opts" "${words[@]}"' % self.query.use()
            self.code['0-init'] = r

    def _generate_option_capture(self):
        local_vars = []
        set_cmds   = []

        for option in self.commandline.options:
            if option.capture:
                local_vars.append(option.capture)
                set_cmds.append('IFS=$"\\n" %s=($(%s get_option %s))' % (
                    option.capture,
                    self.query.use('get_option'),
                    ' '.join(shell.escape(s) for s in option.option_strings)))

        if local_vars:
            r  = 'local %s' % ' '.join(f'{s}=()' for s in local_vars)
            for cmd in set_cmds:
                r += '\n%s' % cmd

            return r

        return ''

    def _generate_subcommand_call(self):
        if not self.subcommands:
            return ''

        zsh_query = self.query.use('get_positional')
        positional_num = self.subcommands.get_positional_num()

        r =  'case "$(%s get_positional %d)" in\n' % (zsh_query, positional_num)
        for subcommand in self.subcommands.subcommands:
            sub_funcname = shell.make_completion_funcname(subcommand)
            cmds = utils.get_all_command_variations(subcommand)
            pattern = '|'.join(shell.escape(s) for s in cmds)
            r += f'  {pattern}) {sub_funcname}; return $?;;\n'
        r += 'esac'

        return r

    def _generate_option_parsing(self):
        args = []

        if self.commandline.inherit_options:
            options = self.commandline.get_options(with_parent_options=True)
        else:
            options = self.commandline.get_options()

        for option in options:
            args.append(self._complete_option(option))

        for cmdline in self.commandline.get_parents():
            for option in cmdline.get_positionals():
                args.append(self._complete_positional(option))

            if cmdline.get_subcommands_option():
                args.append(self._complete_subcommands(cmdline.get_subcommands_option()))

        for option in self.commandline.get_positionals():
            args.append(self._complete_positional(option))

        if self.subcommands:
            args.append(self._complete_subcommands(self.subcommands))

        if not args:
            return ''

        args_with_when = []
        args_without_when = []
        for arg in args:
            if arg.when is None and arg.hidden is False:
                args_without_when.append(arg)
            else:
                args_with_when.append(arg)

        r = ''

        if not args_without_when:
            r += 'local -a args=()\n'
        else:
            r += 'local -a args=(\n'
            for arg in args_without_when:
                r += '  %s\n' % arg.option_spec
            r += ')\n'

        for arg in args_with_when:
            if arg.hidden:
                func = self.query.use('has_option')
                func = self.query.use('with_incomplete')
                r += '%s has_option WITH_INCOMPLETE %s &&\\\n' % (func,
                    ' '.join(shell.escape(o) for o in arg.option.option_strings))

            if arg.when:
                func = self.query.use_when(arg.when)
                r += '%s %s &&\\\n' % (func, arg.when)

            r += '  args+=(%s)\n' % arg.option_spec

        r += '_arguments -S -s -w "${args[@]}"'
        return r

    def get_code(self):
        '''Return the code of the completion function.'''

        return '%s() {\n%s\n}' % (
            self.funcname,
            indent('\n\n'.join(c for c in self.code.values() if c), 2))

def generate_completion(commandline, config=None):
    '''Code for generating a Zsh auto completion file.'''

    if config is None:
        config = config_.Config()

    commandline = generation.enhance_commandline(commandline, config)
    helpers = zsh_helpers.ZshHelpers(commandline.prog)
    ctxt = generation.GenerationContext(config, helpers)
    functions = generation.visit_commandlines(ZshCompletionFunction, ctxt, commandline)
    all_progs = ' '.join([commandline.prog] + commandline.aliases)

    if helpers.is_used('zsh_query'):
        types = utils.get_defined_option_types(commandline)
        if types.short:
            ctxt.helpers.use_function('zsh_query', 'short_options')
        if types.long:
            ctxt.helpers.use_function('zsh_query', 'long_options')
        if types.old:
            ctxt.helpers.use_function('zsh_query', 'old_options')

    output = []

    if config.zsh_compdef:
        output += ['#compdef %s' % all_progs]

    output.append(generation_notice.GENERATION_NOTICE)

    output.extend(config.get_included_files_content())

    for code in helpers.get_used_functions_code():
        output.append(code)

    output += [function.get_code() for function in functions]

    if config.zsh_compdef:
        output += ['%s "$@"' % functions[0].funcname]
    else:
        output += ['compdef %s %s' % (functions[0].funcname, all_progs)]

    if config.vim_modeline:
        output += [modeline.get_vim_modeline('zsh')]

    return '\n\n'.join(output)
