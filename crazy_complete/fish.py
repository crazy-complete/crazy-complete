'''
Code for generating a fish auto completion file
'''

from collections import namedtuple, OrderedDict

from . import generation_notice
from . import modeline
from . import shell
from . import utils
from . import fish_complete
from . import fish_helpers
from .fish_utils import *

class Conditions:
    NumOfPositionals = namedtuple('NumOfPositionals', ['operator', 'value'])

    def __init__(self):
        self.positional_contains = {}
        self.not_has_option = []
        self.num_of_positionals = None
        self.when = None

    def get(self, unsafe=False):
        conditions = []

        for num, words in self.positional_contains.items():
            if unsafe:
                guard = "__fish_seen_subcommand_from %s" % (' '.join(words))
            else:
                guard = "$helper '$options' positional_contains %d %s" % (num, ' '.join(words))
            conditions += [guard]

        if len(self.not_has_option):
            use_helper = False
            if unsafe:
                guard = "__fish_not_contain_opt"
                for opt in self.not_has_option:
                    if opt.startswith('--'):
                        guard += ' %s' % opt.lstrip('-')
                    elif opt.startswith('-') and len(opt) == 2:
                        guard += ' -s %s' % opt[1]
                    else:
                        # __fish_not_contain_opt does not support old-options
                        use_helper = True
            else:
                use_helper = True

            if use_helper:
                guard = "not $helper '$options' has_option %s" % ' '.join(self.not_has_option)
            conditions += [guard]

        if self.num_of_positionals is not None:
            if unsafe:
                guard = "test (__fish_number_of_cmd_args_wo_opts) %s %d" % (
                    self.num_of_positionals.operator, self.num_of_positionals.value) # TODO - 1)
            else:
                guard = "$helper '$options' num_of_positionals %s %d" % (
                    self.num_of_positionals.operator, self.num_of_positionals.value - 1)
            conditions += [guard]

        if self.when is not None:
            guard = "$helper '$options' %s" % self.when
            conditions += [guard]

        if not conditions:
            return None

        return '"%s"' % ' && '.join(conditions)

class FishCompletionDefinition:
    def __init__(
          self,
          short_options=[],           # List of short options
          long_options=[],            # List of long options
          old_options=[],             # List of old-style options
          description=None,           # Description
          requires_argument=False,    # Option requires an argument
          completion_args=None
        ):
        self.short_options = short_options
        self.long_options = long_options
        self.old_options = old_options
        self.description = description
        self.requires_argument = requires_argument
        self.completion_args = completion_args
        self.conds = Conditions()

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
        cmd.set_condition(self.conds.get(unsafe=unsafe), raw=True)

        return cmd

def get_positional_contains(option):
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
        self.conditions = VariableManager('guard')
        self.command_comment = '# command %s' % ' '.join(p.prog for p in self.commandline.get_parents(include_self=True))
        self.options_for_helper = 'set -l options "%s"' % self._get_option_strings_for_helper()

        complete_definitions = []
        for option in self.commandline.get_options():
            complete_definitions.append(self.complete_option(option))

        for positional in self.commandline.get_positionals():
            complete_definitions.append(self.complete_positional(positional))

        if self.commandline.get_subcommands_option():
            complete_definitions.append(self.complete_subcommands(self.commandline.get_subcommands_option()))

        for definition in complete_definitions:
            cmd = definition.get_complete_cmd(self.ctxt.config.fish_fast)

            if cmd.condition is not None and '$helper' in cmd.condition.s:
                self.ctxt.helpers.use_function('fish_helper')

            if not self.ctxt.config.fish_inline_conditions:
                if cmd.condition is not None:
                    cmd.set_condition(self.conditions.add(cmd.condition.s), raw=True)

            self.lines.append(cmd.get())

    def _get_option_strings_for_helper(self):
        r = []
        for option in self.commandline.get_options(with_parent_options=True):
            if option.takes_args == '?':
                r.extend('%s=?' % s for s in option.option_strings)
            elif option.takes_args:
                r.extend('%s=' % s for s in option.option_strings)
            else:
                r.extend(option.option_strings)
        return ','.join(r)

    def complete_option(self, option):
        context = self.ctxt.getOptionGenerationContext(self.commandline, option)
        completion_args = self.completer.complete(context, *option.complete).get_args()

        definition = FishCompletionDefinition(
            short_options       = option.get_short_option_strings(),
            long_options        = option.get_long_option_strings(),
            old_options         = option.get_old_option_strings(),
            requires_argument   = (option.takes_args is True),
            description         = option.help,
            completion_args     = completion_args)

        conflicting_options = option.get_conflicting_option_strings()
        definition.conds.not_has_option.extend(conflicting_options)

        if not option.multiple_option:
            definition.conds.not_has_option.extend(option.option_strings)

        # TODO: fix or at least explain this...
        if not self.commandline.inherit_options and self.commandline.get_subcommands_option():
            positional = self.commandline.get_subcommands_option().get_positional_num()
            definition.conds.num_of_positionals = Conditions.NumOfPositionals('-eq', positional) # -1 TODO

        definition.conds.positional_contains = get_positional_contains(option)
        definition.conds.when = option.when

        return definition

    def complete_positional(self, option):
        context = self.ctxt.getOptionGenerationContext(self.commandline, option)
        completion_args = self.completer.complete(context, *option.complete).get_args()

        definition = FishCompletionDefinition(
            requires_argument   = True,
            description         = option.help,
            completion_args     = completion_args
        )

        definition.conds.when = option.when
        definition.conds.positional_contains = get_positional_contains(option)

        positional = option.get_positional_num()
        if option.repeatable:
            definition.conds.num_of_positionals = Conditions.NumOfPositionals('-ge', positional) # -1 TODO
        else:
            definition.conds.num_of_positionals = Conditions.NumOfPositionals('-eq', positional) # -1 TODO

        return definition

    def complete_subcommands(self, option):
        items = option.get_choices()
        context = self.ctxt.getOptionGenerationContext(self.commandline, option)
        completion_args = self.completer.complete(context, 'choices', items).get_args()

        definition = FishCompletionDefinition(
            description    = 'Commands',
            completion_args = completion_args
        )

        positional = option.get_positional_num()
        definition.conds.num_of_positionals = Conditions.NumOfPositionals('-eq', positional) # -1 TODO
        definition.conds.positional_contains = get_positional_contains(option)
        return definition


def generate_completion(commandline, program_name=None, config=None):
    result = shell.CompletionGenerator(FishCompletionGenerator, fish_helpers.FISH_Helpers, commandline, program_name, config)

    output = []

    output.append(generation_notice.GENERATION_NOTICE)
    output.append('')

    for code in result.include_files_content:
        output.append(code)
        output.append('')

    for code in result.ctxt.helpers.get_used_functions_code():
        output.append(code)
        output.append('')

    output.append('set -l prog "%s"'   % result.result[0].commandline.prog)
    if result.ctxt.helpers.is_used('fish_helper'):
        output.append('set -l helper "%s"' % result.ctxt.helpers.use_function('fish_helper'))

    output.append('')
    output.append('# Generally disable file completion')
    output.append('complete -c $prog -x')

    for generator in result.result:
        output.append('')
        output.append(generator.command_comment)
        output.append(generator.options_for_helper)
        output.extend(generator.conditions.get_lines())
        output.extend(generator.lines)

    if config.vim_modeline:
        output.append('')
        output.append(modeline.get_vim_modeline('fish'))

    return '\n'.join(output)
