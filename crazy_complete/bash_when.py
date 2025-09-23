'''Code for creating when conditions in Bash.'''

from . import when
from . import shell

def _generate_option_is(commandline, variable_manager, obj):
    conditions = []

    for o in commandline.get_options_by_option_strings(obj.options):
        have_option = '(( ${#[%s]} ))' % variable_manager.make_variable(o)
        value_equals = []

        for value in obj.values:
            value_equals.append('[[ "${%s[-1]}" == %s ]]' % (
                variable_manager.make_variable(o),
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

def _generate_has_option(commandline, variable_manager, obj):
    conditions = []

    for o in commandline.get_options_by_option_strings(obj.options):
        cond = '(( ${#[%s]} ))' % variable_manager.make_variable(o)
        conditions.append(cond)

    if len(conditions) == 1:
        return conditions[0]

    return '{ %s; }' % ' || '.join(conditions)

def generate_when_conditions(commandline, variable_manager, when_):
    '''Generate when condition code.'''

    parsed = when.parse_when(when_)

    if isinstance(parsed, when.OptionIs):
        return _generate_option_is(commandline, variable_manager, parsed)

    if isinstance(parsed, when.HasOption):
        return _generate_has_option(commandline, variable_manager, parsed)

    raise AssertionError('invalid instance of `parse`')
