'''Code for creating when conditions in Bash.'''

from . import when
from . import shell


class ConditionGenerator:
    '''Class for generating conditions.'''

    def __init__(self, commandline, variable_manager):
        self.commandline = commandline
        self.variable_manager = variable_manager

    def generate(self, tokens):
        '''Turn tokens/objects into condition code.'''

        r = []

        for obj in tokens:
            if isinstance(obj, when.OptionIs):
                r.append(self._gen_option_is(obj))

            elif isinstance(obj, when.HasOption):
                r.append(self._gen_has_option(obj))

            elif obj in ('&&', '||', '!'):
                r.append(obj)

            elif obj == '(':
                r.append('{')

            elif obj == ')':
                r.append(';}')

            else:
                raise AssertionError("Not reached")

        if when.needs_braces(tokens):
            return '{ %s; }' % ' '.join(r)

        return ' '.join(r)

    def _gen_option_is(self, obj):
        conditions = []

        for o in self.commandline.get_options_by_option_strings(obj.options):
            have_option = '(( ${#%s[@]} ))' % self.variable_manager.capture_variable(o)
            value_equals = []

            for value in obj.values:
                value_equals.append('[[ "${%s[-1]}" == %s ]]' % (
                    self.variable_manager.capture_variable(o),
                    shell.escape(value)
                ))

            if len(value_equals) == 1:
                cond = '{ %s && %s; }' % (have_option, value_equals[0])
            else:
                cond = '{ %s && { %s; } }' % (have_option, ' || '.join(value_equals))

            conditions.append(cond)

        if len(conditions) == 1:
            return conditions[0]

        return '{ %s; }' % ' || '.join(conditions)

    def _gen_has_option(self, obj):
        conditions = []

        for o in self.commandline.get_options_by_option_strings(obj.options):
            cond = '(( ${#%s[@]} ))' % self.variable_manager.capture_variable(o)
            conditions.append(cond)

        if len(conditions) == 1:
            return conditions[0]

        return '{ %s; }' % ' || '.join(conditions)


def generate_when_conditions(commandline, variable_manager, when_):
    '''Generate when condition code.'''

    tokens = when.parse_when(when_)
    generator = ConditionGenerator(commandline, variable_manager)
    return generator.generate(tokens)
