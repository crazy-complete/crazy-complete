'''Code for generating a Fish auto completion file.'''

from . import config as config_
from . import utils
from . import algo
from . import fish_complete
from . import fish_helpers
from . import generation
from .output import Output
from .fish_utils import FishCompleteCommand, VariableManager
from .fish_conditions import (
    Conditions, Not,
    HasHiddenOption, HasOption, PositionalNum, PositionalContains
)


class FishCompletionDefinition:
    '''Class holding a completion definition.'''

    # pylint: disable=too-many-instance-attributes
    # pylint: disable=too-many-arguments
    # pylint: disable=too-many-positional-arguments
    # pylint: disable=too-few-public-methods

    def __init__(
          self,
          ctxt,
          short_options=None,       # List of short options
          long_options=None,        # List of long options
          old_options=None,         # List of old-style options
          positional=None,          # Positional number
          description=None,         # Description
          requires_argument=False,  # Option requires an argument
          keep_order=False,         # Do not sort completion suggestions
          completion_obj=None):

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
        self.keep_order = keep_order
        self.completion_obj = completion_obj
        self.conditions = Conditions()

    def get_complete_cmd(self, ctxt):
        '''Return a `complete` command for current definition.'''

        cmd = FishCompleteCommand()
        cmd.set_command('$prog', raw=True)

        cmd.add_old_options(self.old_options)
        cmd.add_long_options(self.long_options)

        # The Fish manual for complete says that if short option stacking is
        # not desired, we should add the short options as old options.
        if not ctxt.config.option_stacking:
            cmd.add_old_options(self.short_options)
        else:
            cmd.add_short_options(self.short_options)

        if self.description is not None:
            cmd.set_description(self.description)

        if self.requires_argument:
            cmd.flags.add('r')

        if self.keep_order:
            cmd.flags.add('k')

        cmd.parse_args(self.completion_obj.get_args())

        if ctxt.config.fish_fast:
            cmd.set_condition(self.conditions.unsafe_code(ctxt), raw=True)
        else:
            cmd.set_condition(self.conditions.query_code(ctxt), raw=True)

        return cmd


def _get_positional_contains(option):
    commandlines = option.parent.get_parents(include_self=True)
    del commandlines[0]

    conditions = []

    for commandline in commandlines:
        cmds = utils.get_all_command_variations(commandline)
        num = commandline.parent.get_subcommands().get_positional_num()
        conditions.append(PositionalContains(num, cmds))

    return conditions


class FishCompletionGenerator:
    '''Class for generating completions.'''

    # pylint: disable=too-many-instance-attributes

    def __init__(self, ctxt, commandline, parent=None):
        self.ctxt = ctxt
        self.commandline = commandline
        self.parent = parent
        self.children = []

        self.completer = fish_complete.FishCompleter()
        self.subcommands = self.commandline.get_subcommands()
        self.lines = []
        self.conditions = VariableManager('C')
        self.complete_definitions = []

        for option in self.commandline.get_options():
            self.complete_definitions.append(
                self._complete_option(option))

        for positional in self.commandline.get_positionals():
            self.complete_definitions.append(
                self._complete_positional(positional))

        if self.subcommands:
            self.complete_definitions.append(self._complete_subcommands())

            for sub in self.subcommands.subcommands:
                self.children.append(FishCompletionGenerator(ctxt, sub, self))

        for definition in self.complete_definitions:
            if isinstance(definition.completion_obj, fish_complete.FishCompleteCommandArg):
                cmdline = self
                while cmdline:
                    cmdline._fix_command_arg(definition.positional)
                    cmdline = cmdline.parent

        for definition in self.complete_definitions:
            cmd = definition.get_complete_cmd(self.ctxt)

            if not self.ctxt.config.fish_inline_conditions:
                if cmd.condition is not None:
                    cmd.set_condition(self.conditions.add(cmd.condition.string), raw=True)

            self.lines.append(cmd.get())

    def _complete(self, context, *args):
        return self.completer.complete(context, [], *args)

    def _fix_command_arg(self, positional):
        for definition in self.complete_definitions:
            if not (definition.short_options or
                    definition.long_options or
                    definition.old_options):
                continue

            definition.conditions.add(Not(PositionalNum('>=', positional)))

    def visit(self, callback):
        '''Execute callback for generator objects.'''

        callback(self)
        for child in self.children:
            callback(child)

    def get_all(self):
        '''Return all generator objects.'''

        r = []
        self.visit(r.append)
        return r

    def _complete_option(self, option):
        context = self.ctxt.get_option_context(self.commandline, option)

        if option.complete:
            completion_obj = self._complete(context, *option.complete)
        else:
            completion_obj = self._complete(context, 'none')

        definition = FishCompletionDefinition(
            self.ctxt,
            short_options     = option.get_short_option_strings(),
            long_options      = option.get_long_option_strings(),
            old_options       = option.get_old_option_strings(),
            requires_argument = option.has_required_arg(),
            keep_order        = option.nosort,
            description       = option.help,
            completion_obj    = completion_obj)

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
        if not self.commandline.inherit_options and self.subcommands:
            positional = self.subcommands.get_positional_num()
            definition.conditions.add(PositionalNum('==', positional))

        definition.conditions.extend(_get_positional_contains(option))
        definition.conditions.add_when(option.when_parsed)

        return definition

    def _complete_positional(self, positional):
        context = self.ctxt.get_option_context(self.commandline, positional)

        if positional.complete:
            completion_obj = self._complete(context, *positional.complete)
        else:
            completion_obj = self._complete(context, 'none')

        definition = FishCompletionDefinition(
            self.ctxt,
            positional        = positional.get_positional_num(),
            requires_argument = True,
            keep_order        = positional.nosort,
            description       = positional.help,
            completion_obj    = completion_obj
        )

        definition.conditions.add_when(positional.when_parsed)
        definition.conditions.extend(_get_positional_contains(positional))

        positional_num = positional.get_positional_num()
        operator = '>=' if positional.repeatable else '=='
        definition.conditions.add(PositionalNum(operator, positional_num))

        return definition

    def _complete_subcommands(self):
        positional = self.subcommands
        items = positional.get_choices()
        context = self.ctxt.get_option_context(self.commandline, positional)
        completion_obj = self._complete(context, 'choices', items)

        definition = FishCompletionDefinition(
            self.ctxt,
            description = 'Commands',
            completion_obj = completion_obj
        )

        positional_num = positional.get_positional_num()
        definition.conditions.add(PositionalNum('==', positional_num))
        definition.conditions.extend(_get_positional_contains(positional))
        return definition

    def get_command_comment(self):
        '''Return a comment for the current command.'''
        return '# command %s' % self.commandline.get_command_path()

    def get_options_for_query(self):
        '''Return the options for the query command.'''
        return 'set -l opts "%s"' % (
            utils.get_query_option_strings(self.commandline))


def generate_completion(commandline, config=None):
    '''Code for generating a Fish auto completion file.'''

    if config is None:
        config = config_.Config()

    commandline = generation.enhance_commandline(commandline, config)
    helpers = fish_helpers.FishHelpers(config, commandline.prog)
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

    output = Output(config, helpers)
    output.add_generation_notice()
    output.add_comments()
    output.add_included_files()
    output.add_helper_functions_code()

    with output.add_as_block() as block:
        block.add("set -l prog '%s'" % commandline.prog)

        if helpers.is_used('query'):
            block.add("set -l query '%s'" % helpers.use_function('query'))

        block.add('')
        block.add('# Delete existing completions')
        block.add('complete -c $prog -e')
        block.add('')
        block.add('# Generally disable file completion')
        block.add('complete -c $prog -x')

    if result.commandline.wraps:
        with output.add_as_block() as block:
            block.add('# Wrap command')
            block.add('complete -c $prog -w %s' % result.commandline.wraps)

    for generator in result.get_all():
        if generator.lines:
            with output.add_as_block() as block:
                block.add(generator.get_command_comment())
                block.add(generator.get_options_for_query())
                block.extend(generator.conditions.get_lines())
                block.extend(generator.lines)

    if commandline.aliases:
        with output.add_as_block() as block:
            for alias in commandline.aliases:
                block.add('complete -c %s -e' % alias)
                block.add('complete -c %s -w %s' % (alias, commandline.prog))

    output.add_vim_modeline('fish')

    return output.get()
