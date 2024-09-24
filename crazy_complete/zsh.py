'''
Code for generating a zsh auto completion file
'''

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
        takes_args = False,
        multiple_option = False,
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

    if not_options:
        result.append(shell.escape('(%s)' % ' '.join(not_options)))

    # Multiple option =========================================================
    if multiple_option:
        result.append("'*'")

    # Option strings ==========================================================
    if takes_args == '?':
        opts = [o+'-' if len(o) == 2 else o+'=-' for o in option_strings]
    elif takes_args:
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

    if takes_args is True or takes_args == '?':
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
        self.helper_used = False
        self._generate_completion_function()

    def _get_option_strings(self):
        r = []
        for o in self.commandline.get_options(with_parent_options=True):
            if o.takes_args == '?':
                r.extend('%s=?' % s for s in o.option_strings)
            elif o.takes_args:
                r.extend('%s=' % s for s in o.option_strings)
            else:
                r.extend('%s' % s for s in o.option_strings)
        return ','.join(r)

    def complete(self, option, command, *args):
        context = self.ctxt.getOptionGenerationContext(self.commandline, option)
        return self.completer.complete(context, command, *args)

    def complete_option(self, option):
        option_spec = make_argument_option_spec(
            option.option_strings,
            conflicting_options = option.get_conflicting_option_strings(),
            description = option.help,
            takes_args = option.takes_args,
            multiple_option = option.multiple_option,
            metavar = option.metavar,
            action = self.complete(option, *option.complete)
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
        # the zsh_helper function is used.
        subcommand_code = self._generate_subcommand()
        options_code = self._generate_option_parsing()

        if self.helper_used:
            zsh_helper = self.ctxt.helpers.use_function('zsh_helper')
            r  = 'local opts=%s\n' % shell.escape(self._get_option_strings())
            r += 'local -a HAVING_OPTIONS=() OPTION_VALUES=() POSITIONALS=()\n'
            r += '%s setup "$opts" "${words[@]}"' % zsh_helper
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

        self.helper_used = True
        zsh_helper = self.ctxt.helpers.use_function('zsh_helper')
        r =  'case "$(%s get_positional %d)" in\n' % (zsh_helper, self.subcommands.get_positional_num())
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

        # TODO: describe why we need this
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
            self.helper_used = True
            zsh_helper = self.ctxt.helpers.use_function('zsh_helper')
            r += '%s %s &&\\\n' % (zsh_helper, when)
            r += '  args+=(%s)\n' % option_spec

        r += '_arguments -S -s -w "${args[@]}"'
        return r

def generate_completion(commandline, program_name=None, config=None):
    result = shell.CompletionGenerator(ZshCompletionGenerator, zsh_helpers.ZSH_Helpers, commandline, program_name, config)
    functions = result.result

    output = []

    if config.zsh_compdef:
        output += ['#compdef %s' % functions[0].commandline.prog]

    output.append(generation_notice.GENERATION_NOTICE)

    output.extend(result.include_files_content)

    for code in result.ctxt.helpers.get_used_functions_code():
        output.append(code)

    output += [r.result for r in functions]

    if config.zsh_compdef:
        output += ['%s "$@"' % functions[0].funcname]
    else:
        output += ['compdef %s %s' % (functions[0].funcname, functions[0].commandline.prog)]

    if config.vim_modeline:
        output += [modeline.get_vim_modeline('zsh')]

    return '\n\n'.join(output)
