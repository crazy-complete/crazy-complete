'''Code for generating a fish auto completion file.'''

from . import config as config_
from . import generation_notice
from . import modeline
from . import utils
from . import algo
from . import fish_complete
from . import fish_helpers
from .fish_utils import FishCompleteCommand, VariableManager
from .fish_conditions import (
    Conditions, Not,
    HasHiddenOption, HasOption, PositionalNum, PositionalContains
)
from . import generation


class FishCompletionDefinition:
    def __init__(
          self,
          ctxt,
          short_options=None,      # List of short options
          long_options=None,       # List of long options
          old_options=None,        # List of old-style options
          positional=None,         # Positional number
          description=None,        # Description
          requires_argument=False, # Option requires an argument
          completion_obj=None
        ):
        if short_options is None:
            short_options = []
        if long_options is None:
            long_options = []
        if old_options is None:
            old_options = []
        self.ctxt = ctxt
        self.short_options = short_options
        self.long_options = long_options
        self.old_options = old_options
        self.positional = positional
        self.description = description
        self.requires_argument = requires_argument
        self.completion_obj = completion_obj
        self.conditions = Conditions()

    def get_complete_cmd(self, ctxt, unsafe=False):
        cmd = FishCompleteCommand()
        cmd.set_command('$prog', raw=True)

        cmd.add_old_options(self.old_options)
        cmd.add_long_options(self.long_options)

        if not ctxt.config.option_stacking:
            cmd.add_old_options(self.short_options)
        else:
            cmd.add_short_options(self.short_options)

        if self.description is not None:
            cmd.set_description(self.description)

        if self.requires_argument:
            cmd.flags.add('r')

        cmd.parse_args(self.completion_obj.get_args())

        if unsafe:
            cmd.set_condition(self.conditions.unsafe_code(ctxt), raw=True)
        else:
            cmd.set_condition(self.conditions.query_code(ctxt), raw=True)

        return cmd


def _get_positional_contains(option):
    cmdlines = option.parent.get_parents(include_self=True)
    del cmdlines[0]

    conditions = []

    for cmdline in cmdlines:
        cmds = utils.get_all_command_variations(cmdline)
        num = cmdline.parent.get_subcommands().get_positional_num()
        conditions.append(PositionalContains(num, cmds))

    return conditions


class FishCompletionGenerator:
    def __init__(self, ctxt, commandline, parent=None):
        self.parent = parent
        self.children = []

        self.commandline = commandline
        self.ctxt = ctxt
        self.completer = fish_complete.FishCompleter()
        self.lines = []
        self.conditions = VariableManager('C')
        self.command_comment = '# command %s' % self.commandline.get_command_path()
        self.options_for_query = 'set -l opts "%s"' % utils.get_query_option_strings(self.commandline)
        self.complete_definitions = []

        for option in self.commandline.get_options():
            self.complete_definitions.append(self._complete_option(option))

        for positional in self.commandline.get_positionals():
            self.complete_definitions.append(self._complete_positional(positional))

        if self.commandline.get_subcommands():
            self.complete_definitions.append(self._complete_subcommands(self.commandline.get_subcommands()))

        if self.commandline.get_subcommands():
            for subcmd in self.commandline.get_subcommands().subcommands:
                self.children.append(FishCompletionGenerator(ctxt, subcmd, self))

        for definition in self.complete_definitions:
            if isinstance(definition.completion_obj, fish_complete.FishCompleteCommandArg):
                cmdline = self
                while cmdline:
                    cmdline.fix_command_arg(definition.positional)
                    cmdline = cmdline.parent

        for definition in self.complete_definitions:
            cmd = definition.get_complete_cmd(self.ctxt, self.ctxt.config.fish_fast)

            if not self.ctxt.config.fish_inline_conditions:
                if cmd.condition is not None:
                    cmd.set_condition(self.conditions.add(cmd.condition.s), raw=True)

            self.lines.append(cmd.get())

    def fix_command_arg(self, positional):
        for definition in self.complete_definitions:
            if not (definition.short_options or definition.long_options or definition.old_options):
                continue

            definition.conditions.add(Not(PositionalNum('>=', positional)))

    def visit(self, callback):
        callback(self)
        for child in self.children:
            callback(child)

    def get_all(self):
        r = []
        self.visit(r.append)
        return r

    def _complete_option(self, option):
        context = self.ctxt.get_option_context(self.commandline, option)

        if option.complete:
            completion_obj = self.completer.complete(context, [], *option.complete)
        else:
            completion_obj = self.completer.complete(context, [], 'none')

        definition = FishCompletionDefinition(
            self.ctxt,
            short_options       = option.get_short_option_strings(),
            long_options        = option.get_long_option_strings(),
            old_options         = option.get_old_option_strings(),
            requires_argument   = (option.complete and not option.optional_arg),
            description         = option.help,
            completion_obj      = completion_obj)

        not_has_options = []

        final_options = self.commandline.get_final_option_strings()
        not_has_options.extend(final_options)

        conflicting_options = option.get_conflicting_option_strings()
        not_has_options.extend(conflicting_options)

        if not option.repeatable:
            not_has_options.extend(option.option_strings)

        if not_has_options:
            not_has_options = algo.uniq(not_has_options)
            definition.conditions.add(Not(HasOption(not_has_options)))

        if option.hidden:
            definition.conditions.add(HasHiddenOption(option.option_strings))

        # If we don't inherit options, add a condition to the option that
        # ensures that we're in the right (sub)command.
        if not self.commandline.inherit_options and self.commandline.get_subcommands():
            positional = self.commandline.get_subcommands().get_positional_num()
            definition.conditions.add(PositionalNum('==', positional))

        definition.conditions.extend(_get_positional_contains(option))
        definition.conditions.add_when(option.when_parsed)

        return definition

    def _complete_positional(self, option):
        context = self.ctxt.get_option_context(self.commandline, option)

        if option.complete:
            completion_obj = self.completer.complete(context, [], *option.complete)
        else:
            completion_obj = self.completer.complete(context, [], 'none')

        definition = FishCompletionDefinition(
            self.ctxt,
            positional          = option.get_positional_num(),
            requires_argument   = True,
            description         = option.help,
            completion_obj      = completion_obj
        )

        definition.conditions.add_when(option.when_parsed)
        definition.conditions.extend(_get_positional_contains(option))

        positional = option.get_positional_num()
        operator = '>=' if option.repeatable else '=='
        definition.conditions.add(PositionalNum(operator, positional))

        return definition

    def _complete_subcommands(self, option):
        items = option.get_choices()
        context = self.ctxt.get_option_context(self.commandline, option)
        completion_obj = self.completer.complete(context, [], 'choices', items)

        definition = FishCompletionDefinition(
            self.ctxt,
            description    = 'Commands',
            completion_obj = completion_obj
        )

        positional = option.get_positional_num()
        definition.conditions.add(PositionalNum('==', positional))
        definition.conditions.extend(_get_positional_contains(option))
        return definition


def generate_completion(commandline, config=None):
    '''Code for generating a Fish auto completion file.'''

    if config is None:
        config = config_.Config()

    commandline = generation.enhance_commandline(commandline, config)
    helpers = fish_helpers.FishHelpers(commandline.prog)
    ctxt = generation.GenerationContext(config, helpers)
    result = FishCompletionGenerator(ctxt, commandline)

    if helpers.is_used('query'):
        types = utils.get_defined_option_types(commandline)
        if types.short:
            ctxt.helpers.use_function('query', 'short_options')
        if types.long:
            ctxt.helpers.use_function('query', 'long_options')
        if types.old:
            ctxt.helpers.use_function('query', 'old_options')

    output = []

    output.append(generation_notice.GENERATION_NOTICE)
    output.append('')

    if config.comments:
        output += [config.get_comments_as_string()]
        output.append('')

    for code in config.get_included_files_content():
        output.append(code)
        output.append('')

    for code in helpers.get_used_functions_code():
        output.append(code)
        output.append('')

    output.append("set -l prog '%s'" % commandline.prog)
    if helpers.is_used('query'):
        output.append("set -l query '%s'" % helpers.use_function('query'))

    output.append('')
    output.append('# Delete existing completions')
    output.append('complete -c $prog -e')
    output.append('')
    output.append('# Generally disable file completion')
    output.append('complete -c $prog -x')

    if result.commandline.wraps:
        output.append('')
        output.append('# Wrap command')
        output.append('complete -c $prog -w %s' % result.commandline.wraps)

    for generator in result.get_all():
        if generator.lines:
            output.append('')
            output.append(generator.command_comment)
            output.append(generator.options_for_query)
            output.extend(generator.conditions.get_lines())
            output.extend(generator.lines)

    if commandline.aliases:
        output.append('')
        for alias in commandline.aliases:
            output.append('complete -c %s -e' % alias)
            output.append('complete -c %s -w %s' % (alias, commandline.prog))

    if config.vim_modeline:
        output.append('')
        output.append(modeline.get_vim_modeline('fish'))

    return '\n'.join(output)
