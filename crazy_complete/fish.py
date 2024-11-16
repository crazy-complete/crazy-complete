'''
Code for generating a fish auto completion file.
'''

from collections import namedtuple, OrderedDict

from . import config as config_
from . import generation_notice
from . import modeline
from . import utils
from . import algo
from . import fish_complete
from . import fish_helpers
from .fish_utils import *
from . import when
from . import generation

class FishQuery:
    def __init__(self, ctxt):
        self.ctxt = ctxt

    def positional_contains(self, num, words):
        self.ctxt.helpers.use_function('fish_query', 'positional_contains')
        r = "$query '$opts' positional_contains %d %s" % (num, ' '.join(words))
        return r

    def has_option(self, options):
        self.ctxt.helpers.use_function('fish_query', 'has_option')
        r = "$query '$opts' has_option %s" % ' '.join(options)
        return r

    def option_is(self, options, values):
        self.ctxt.helpers.use_function('fish_query', 'option_is')
        r = "$query '$opts' option_is %s -- %s" % (
            ' '.join(options), ' '.join(values))
        return r

    def num_of_positionals(self, operator, num):
        self.ctxt.helpers.use_function('fish_query', 'num_of_positionals')
        r = "$query '$opts' num_of_positionals %s %d" % (operator, num)
        return r

    def by_object(self, obj):
        if isinstance(obj, when.OptionIs):
            return self.option_is(obj.options, obj.values)
        if isinstance(obj, when.HasOption):
            return self.has_option(obj.options)
        raise AssertionError("Should not be reached")

class Conditions:
    NumOfPositionals = namedtuple('NumOfPositionals', ['operator', 'value'])

    def __init__(self, ctxt):
        self.ctxt = ctxt
        self.fish_query = FishQuery(ctxt)
        self.positional_contains = {}
        self.not_has_option = []
        self.num_of_positionals = None
        self.has_hidden_option = []
        self.when = None

    def get(self, unsafe=False):
        conditions = []

        for num, words in self.positional_contains.items():
            if unsafe:
                guard = "__fish_seen_subcommand_from %s" % (' '.join(words))
            else:
                guard = self.fish_query.positional_contains(num, words)
            conditions += [guard]

        if self.not_has_option:
            if unsafe:
                guard = "not __fish_seen_argument"
                for opt in self.not_has_option:
                    if opt.startswith('--'):
                        guard += ' -l %s' % opt.lstrip('-')
                    elif len(opt) == 2:
                        guard += ' -s %s' % opt[1]
                    else:
                        guard += ' -o %s' % opt.lstrip('-')
            else:
                guard = "not %s" % self.fish_query.has_option(self.not_has_option)
            conditions += [guard]

        if self.num_of_positionals is not None:
            if unsafe:
                guard = "test (__fish_number_of_cmd_args_wo_opts) %s %d" % (
                    self.num_of_positionals.operator, self.num_of_positionals.value) # TODO - 1)
            else:
                guard = self.fish_query.num_of_positionals(
                    self.num_of_positionals.operator, self.num_of_positionals.value - 1)
            conditions += [guard]

        if self.has_hidden_option:
            func = self.ctxt.helpers.use_function('fish_query', 'with_incomplete')
            func = self.ctxt.helpers.use_function('fish_query', 'has_option')
            guard = "$query '$opts' has_option WITH_INCOMPLETE %s" % (
                ' '.join(shell.escape(o) for o in self.has_hidden_option))
            conditions += [guard]

        if self.when is not None:
            parsed = when.parse_when(self.when)
            guard = self.fish_query.by_object(parsed)
            conditions += [guard]

        if not conditions:
            return None

        return '"%s"' % ' && '.join(conditions)

class FishCompletionDefinition:
    def __init__(
          self,
          ctxt,
          short_options=[],        # List of short options
          long_options=[],         # List of long options
          old_options=[],          # List of old-style options
          description=None,        # Description
          requires_argument=False, # Option requires an argument
          completion_args=None
        ):
        self.ctxt = ctxt
        self.short_options = short_options
        self.long_options = long_options
        self.old_options = old_options
        self.description = description
        self.requires_argument = requires_argument
        self.completion_args = completion_args
        self.conditions = Conditions(ctxt)

    def get_complete_cmd(self, unsafe=False):
        cmd = FishCompleteCommand()
        cmd.set_command('$prog', raw=True)
        cmd.add_short_options(self.short_options)
        cmd.add_long_options(self.long_options)
        cmd.add_old_options(self.old_options)

        if self.description is not None:
            cmd.set_description(self.description)

        if self.requires_argument:
            cmd.flags.add('r')

        cmd.parse_args(self.completion_args)
        cmd.set_condition(self.conditions.get(unsafe=unsafe), raw=True)

        return cmd

def _get_positional_contains(option):
    cmdlines = option.parent.get_parents(include_self=True)
    del cmdlines[0]

    r = OrderedDict()

    for cmdline in cmdlines:
        cmds = utils.get_all_command_variations(cmdline)
        r[cmdline.parent.get_subcommands_option().get_positional_num()] = cmds

    return r

class FishCompletionGenerator:
    def __init__(self, ctxt, commandline):
        self.commandline = commandline
        self.ctxt = ctxt
        self.completer = fish_complete.FishCompleter()
        self.lines = []
        self.conditions = VariableManager('C')
        self.command_comment = '# command %s' % self.commandline.get_command_path()
        self.options_for_query = 'set -l opts "%s"' % self._get_option_strings_for_query()

        complete_definitions = []
        for option in self.commandline.get_options():
            complete_definitions.append(self._complete_option(option))

        for positional in self.commandline.get_positionals():
            complete_definitions.append(self._complete_positional(positional))

        if self.commandline.get_subcommands_option():
            complete_definitions.append(self._complete_subcommands(self.commandline.get_subcommands_option()))

        for definition in complete_definitions:
            cmd = definition.get_complete_cmd(self.ctxt.config.fish_fast)

            if cmd.condition is not None and '$query' in cmd.condition.s:
                self.ctxt.helpers.use_function('fish_query')

            if not self.ctxt.config.fish_inline_conditions:
                if cmd.condition is not None:
                    cmd.set_condition(self.conditions.add(cmd.condition.s), raw=True)

            self.lines.append(cmd.get())

    def _get_option_strings_for_query(self):
        r = []
        for option in self.commandline.get_options(with_parent_options=True):
            if option.complete and option.optional_arg is True:
                r.extend('%s=?' % s for s in option.option_strings)
            elif option.complete:
                r.extend('%s=' % s for s in option.option_strings)
            else:
                r.extend(option.option_strings)
        return ','.join(r)

    def _complete_option(self, option):
        context = self.ctxt.getOptionGenerationContext(self.commandline, option)

        if option.complete:
            completion_args = self.completer.complete(context, *option.complete).get_args()
        else:
            completion_args = self.completer.complete(context, 'none').get_args()

        definition = FishCompletionDefinition(
            self.ctxt,
            short_options       = option.get_short_option_strings(),
            long_options        = option.get_long_option_strings(),
            old_options         = option.get_old_option_strings(),
            requires_argument   = (option.complete and not option.optional_arg),
            description         = option.help,
            completion_args     = completion_args)

        final_options = self.commandline.get_final_option_strings()
        definition.conditions.not_has_option.extend(final_options)

        conflicting_options = option.get_conflicting_option_strings()
        definition.conditions.not_has_option.extend(conflicting_options)

        if not option.repeatable:
            definition.conditions.not_has_option.extend(option.option_strings)

        if option.hidden:
            definition.conditions.has_hidden_option = option.option_strings

        definition.conditions.not_has_option = algo.uniq(definition.conditions.not_has_option)

        # If we don't inherit options, add a condition to the option that
        # ensures that we're in the right (sub)command.
        if not self.commandline.inherit_options and self.commandline.get_subcommands_option():
            positional = self.commandline.get_subcommands_option().get_positional_num()
            definition.conditions.num_of_positionals = Conditions.NumOfPositionals('-eq', positional)

        definition.conditions.positional_contains = _get_positional_contains(option)
        definition.conditions.when = option.when

        return definition

    def _complete_positional(self, option):
        context = self.ctxt.getOptionGenerationContext(self.commandline, option)

        if option.complete:
            completion_args = self.completer.complete(context, *option.complete).get_args()
        else:
            completion_args = self.completer.complete(context, 'none').get_args()

        definition = FishCompletionDefinition(
            self.ctxt,
            requires_argument   = True,
            description         = option.help,
            completion_args     = completion_args
        )

        definition.conditions.when = option.when
        definition.conditions.positional_contains = _get_positional_contains(option)

        positional = option.get_positional_num()
        if option.repeatable:
            definition.conditions.num_of_positionals = Conditions.NumOfPositionals('-ge', positional)
        else:
            definition.conditions.num_of_positionals = Conditions.NumOfPositionals('-eq', positional)

        return definition

    def _complete_subcommands(self, option):
        items = option.get_choices()
        context = self.ctxt.getOptionGenerationContext(self.commandline, option)
        completion_args = self.completer.complete(context, 'choices', items).get_args()

        definition = FishCompletionDefinition(
            self.ctxt,
            description    = 'Commands',
            completion_args = completion_args
        )

        positional = option.get_positional_num()
        definition.conditions.num_of_positionals = Conditions.NumOfPositionals('-eq', positional)
        definition.conditions.positional_contains = _get_positional_contains(option)
        return definition

def _define_option_types(ctxt, commandline):
    for option in commandline.options:
        for option_string in option.option_strings:
            if option_string.startswith('--'):
                ctxt.helpers.use_function('fish_query', 'long_options')
            elif len(option_string) == 2:
                ctxt.helpers.use_function('fish_query', 'short_options')
            else:
                ctxt.helpers.use_function('fish_query', 'old_options')

def generate_completion(commandline, program_name=None, config=None):
    if config is None:
        config = _config.Config()

    commandline = generation.enhance_commandline(commandline, program_name, config)
    helpers = fish_helpers.FishHelpers(commandline.prog)
    ctxt = generation.GenerationContext(config, helpers)
    result = generation.visit_commandlines(FishCompletionGenerator, ctxt, commandline)

    if helpers.is_used('fish_query'):
       commandline.visit_commandlines(
            lambda cmdline: _define_option_types(ctxt, cmdline))

    output = []

    output.append(generation_notice.GENERATION_NOTICE)
    output.append('')

    for code in config.get_included_files_content():
        output.append(code)
        output.append('')

    for code in helpers.get_used_functions_code():
        output.append(code)
        output.append('')

    output.append('set -l prog "%s"' % commandline.prog)
    if helpers.is_used('fish_query'):
        output.append('set -l query "%s"' % helpers.use_function('fish_query'))

    output.append('')
    output.append('# Generally disable file completion')
    output.append('complete -c $prog -x')

    for generator in result:
        output.append('')
        output.append(generator.command_comment)
        output.append(generator.options_for_query)
        output.extend(generator.conditions.get_lines())
        output.extend(generator.lines)

    if config.vim_modeline:
        output.append('')
        output.append(modeline.get_vim_modeline('fish'))

    return '\n'.join(output)
