'''
Code for generating a zsh auto completion file
'''

from . import config as config_
from . import generation
from . import generation_notice
from . import modeline
from . import shell
from . import utils
from . import zsh_complete
from . import zsh_helpers

def escape_colon(s):
    return s.replace(':', '\\:')

def escape_square_brackets(s):
    return s.replace('[', '\\[').replace(']', '\\]')

def make_argument_option_spec(
        option_strings,
        conflicting_options = [],
        description = None,
        complete = None,
        optional_arg = False,
        multiple_option = False,
        final = False,
        metavar = None,
        action = None
    ):
    '''
    Return something like this:
        (--option -o){--option=,-o+}[Option description]:Metavar:Action
    '''

    result = []

    # Not options =============================================================
    not_options = []

    for o in sorted(conflicting_options):
        not_options.append(escape_colon(o))

    if not multiple_option:
        for o in sorted(option_strings):
            not_options.append(escape_colon(o))

    if final:
        not_options = ['- *']

    if not_options:
        result.append(shell.escape('(%s)' % ' '.join(not_options)))

    # Multiple option =========================================================
    if multiple_option:
        result.append("'*'")

    # Option strings ==========================================================
    if complete and optional_arg is True:
        opts = [o+'-' if len(o) == 2 else o+'=-' for o in option_strings]
    elif complete:
        opts = [o+'+' if len(o) == 2 else o+'=' for o in option_strings]
    else:
        opts = option_strings

    if len(opts) == 1:
        result.append(opts[0])
    else:
        result.append('{%s}' % ','.join(opts))

    # Description =============================================================
    if description is not None:
        result.append(shell.escape('[%s]' % escape_colon(escape_square_brackets(description))))

    if complete:
        if metavar is None:
            metavar = ' '

        result.append(':%s:%s' % (shell.escape(escape_colon(metavar)), action))

    return ''.join(result)

class ZshCompletionGenerator:
    def __init__(self, ctxt, commandline):
        self.commandline = commandline
        self.ctxt = ctxt
        self.funcname = shell.make_completion_funcname(commandline)
        self.subcommands = commandline.get_subcommands_option()
        self.command_counter = 0
        self.completer = zsh_complete.ZshCompleter()
        self.query_used = False
        self._generate_completion_function()

    def _get_option_strings(self):
        r = []
        for o in self.commandline.get_options(with_parent_options=True):
            if o.complete and o.optional_arg is True:
                r.extend('%s=?' % s for s in o.option_strings)
            elif o.complete:
                r.extend('%s=' % s for s in o.option_strings)
            else:
                r.extend('%s' % s for s in o.option_strings)
        return ','.join(r)

    def complete(self, option, command, *args):
        context = self.ctxt.getOptionGenerationContext(self.commandline, option)
        return self.completer.complete(context, command, *args)

    def complete_option(self, option):
        if option.complete:
            action = self.complete(option, *option.complete)
        else:
            action = None

        option_spec = make_argument_option_spec(
            option.option_strings,
            conflicting_options = option.get_conflicting_option_strings(),
            description = option.help,
            complete = option.complete,
            optional_arg = option.optional_arg,
            multiple_option = option.multiple_option,
            final = option.final,
            metavar = option.metavar,
            action = action
        )

        return (option.when, option_spec)

    def complete_subcommands(self, option):
        choices = option.get_choices()
        self.command_counter += 1

        option_spec = "%d:command%d:%s" % (
            option.get_positional_num(),
            self.command_counter,
            self.complete(option, 'choices', choices)
        )

        return (None, option_spec)

    def complete_positional(self, option):
        positional_num = option.get_positional_num()
        if option.repeatable:
            positional_num = "'*'"
        option_spec = "%s:%s:%s" % (
            positional_num,
            shell.escape(escape_colon(option.help or ' ')),
            self.complete(option, *option.complete)
        )

        return (option.when, option_spec)

    def _generate_completion_function(self):
        code = []

        # We have to call these functions first, because they tell us if
        # the zsh_query function is used.
        subcommand_code = self._generate_subcommand()
        options_code = self._generate_option_parsing()

        if self.query_used:
            zsh_query = self.ctxt.helpers.use_function('zsh_query')
            r  = 'local opts=%s\n' % shell.escape(self._get_option_strings())
            r += 'local -a HAVING_OPTIONS=() OPTION_VALUES=() POSITIONALS=()\n'
            r += '%s setup "$opts" "${words[@]}"' % zsh_query
            code.append(r)

        if subcommand_code:
            code.append(subcommand_code)

        if options_code:
            code.append(options_code)

        self.result = '%s() {\n%s\n}' % (
            self.funcname,
            utils.indent('\n\n'.join(code), 2))

    def _generate_subcommand(self):
        if not self.subcommands:
            return ''

        self.query_used = True
        zsh_query = self.ctxt.helpers.use_function('zsh_query')
        positional_num = self.subcommands.get_positional_num()

        r =  'case "$(%s get_positional %d)" in\n' % (zsh_query, positional_num)
        for subcommand in self.subcommands.subcommands:
            sub_funcname = shell.make_completion_funcname(subcommand)
            cmds = utils.get_all_command_variations(subcommand)
            pattern = '|'.join(shell.escape(s) for s in cmds)
            r += f'  ({pattern}) {sub_funcname}; return $?;;\n'
        r += 'esac'

        return r

    def _generate_option_parsing(self):
        args = []

        if self.commandline.inherit_options:
            options = self.commandline.get_options(with_parent_options=True)
        else:
            options = self.commandline.get_options()

        for option in options:
            args.append(self.complete_option(option))

        for cmdline in self.commandline.get_parents():
            for option in cmdline.get_positionals():
                args.append(self.complete_positional(option))

            if cmdline.get_subcommands_option():
                args.append(self.complete_subcommands(cmdline.get_subcommands_option()))

        for option in self.commandline.get_positionals():
            args.append(self.complete_positional(option))

        if self.subcommands:
            args.append(self.complete_subcommands(self.subcommands))

        if not args:
            return ''

        args_with_when = []
        args_without_when = []
        for arg in args:
            if arg[0] is None:
                args_without_when.append(arg)
            else:
                args_with_when.append(arg)

        r = ''

        if not args_without_when:
            r += 'local -a args=()\n'
        else:
            r += 'local -a args=(\n'
            for when, option_spec in args_without_when:
                r += '  %s\n' % option_spec
            r += ')\n'

        for when, option_spec in args_with_when:
            self.query_used = True
            zsh_query = self.ctxt.helpers.use_function('zsh_query')
            r += '%s %s &&\\\n' % (zsh_query, when)
            r += '  args+=(%s)\n' % option_spec

        r += '_arguments -S -s -w "${args[@]}"'
        return r

def _define_option_types(ctxt, commandline):
    for option in commandline.options:
        for option_string in option.option_strings:
            if option_string.startswith('--'):
                ctxt.helpers.use_function('zsh_query', 'long_options')
            elif len(option_string) == 2:
                ctxt.helpers.use_function('zsh_query', 'short_options')
            else:
                ctxt.helpers.use_function('zsh_query', 'old_options')

def generate_completion(commandline, program_name=None, config=None):
    if config is None:
        config = config_.Config()

    commandline = generation.enhance_commandline(commandline, program_name, config)
    helpers = zsh_helpers.ZshHelpers(commandline.prog)
    ctxt = generation.GenerationContext(config, helpers)
    result = generation.visit_commandlines(ZshCompletionGenerator, ctxt, commandline)

    if helpers.is_used('zsh_query'):
        commandline.visit_commandlines(
            lambda cmdline: _define_option_types(ctxt, cmdline))

    output = []

    if config.zsh_compdef:
        output += ['#compdef %s' % commandline.prog]

    output.append(generation_notice.GENERATION_NOTICE)

    output.extend(config.get_included_files_content())

    for code in helpers.get_used_functions_code():
        output.append(code)

    output += [generator.result for generator in result]

    if config.zsh_compdef:
        output += ['%s "$@"' % result[0].funcname]
    else:
        output += ['compdef %s %s' % (result[0].funcname, commandline.prog)]

    if config.vim_modeline:
        output += [modeline.get_vim_modeline('zsh')]

    return '\n\n'.join(output)
