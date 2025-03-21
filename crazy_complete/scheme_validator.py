from types import NoneType

from .cli import ExtendedBool, is_extended_bool, validate_option_string
from .errors import CrazySchemaValidationError
from .value_with_trace import ValueWithTrace

_error = CrazySchemaValidationError

# =============================================================================
# Helper functions for validating
# =============================================================================

def _has_set(dictionary, key):
    return (key in dictionary.value and dictionary.value[key].value is not None)

def _get_required_arg(args, name):
    try:
        return args.value.pop(0)
    except IndexError:
        raise _error(f'Missing required arg `{name}`', args) from None

def _get_optional_arg(args, default=None):
    try:
        return args.value.pop(0)
    except IndexError:
        return ValueWithTrace(default, '<default value>', 1, 1)

def _require_no_more(args):
    if len(args.value) > 0:
        raise _error('Too many arguments provided', args)

def _check_type(value, types, parameter_name=None):
    if not isinstance(value.value, types):
        types_strings = []
        for t in types:
            types_strings.append({
                str:      'string',
                int:      'integer',
                float:    'float',
                list:     'list',
                dict:     'dictionary',
                bool:     'boolean',
                NoneType: 'none'}[t])
        types_string = '|'.join(types_strings)

        msg = f'Invalid type. Expected types: {types_string}'
        if parameter_name is not None:
            msg = f'{parameter_name}: {msg}'
        raise _error(msg, value)

def _check_dictionary(dictionary, rules):
    _check_type(dictionary, (dict,))

    for key, value in dictionary.value.items():
        if key.value not in rules:
            raise _error(f'Unknown key: {key.value}', key)

        _check_type(value, rules[key.value][1], key.value)

    for key, rule in rules.items():
        if rule[0] is True and key not in dictionary.value:
            raise _error(f'Missing required key: {key}', dictionary)

def _is_empty_or_whitespace(string):
    return not string.strip()

def _contains_space(string):
    return (' ' in string or '\t' in string or '\n' in string)

# =============================================================================
# Actual validation code
# =============================================================================

def _check_extended_bool(value):
    if not is_extended_bool(value.value):
        msg = f'Invalid value. Expected true, false or "{ExtendedBool.INHERIT}"'
        raise _error(msg, value)

def _check_complete(args):
    cmd = _get_required_arg(args, 'command')

    no_args_commands = (
        'none', 'integer', 'float',
        'command', 'environment', 'group', 'hostname', 'pid', 'process',
        'service', 'signal', 'user', 'variable',
    )

    if cmd.value in no_args_commands:
        _require_no_more(args)
    elif cmd.value == 'choices':
        choices = _get_required_arg(args, 'choices')
        _check_type(choices, (list, dict))
        _require_no_more(args)

        if isinstance(choices.value, dict):
            for value, desc in choices.value.items():
                _check_type(value, (str,int,float))
                _check_type(desc,  (str,int,float))

        elif isinstance(choices.value, list):
            for value in choices.value:
                _check_type(value, (str,int,float))

    elif cmd.value in ('file', 'directory'):
        options = _get_optional_arg(args, {})
        _check_type(options, (dict,))
        _require_no_more(args)
        _check_dictionary(options, {'directory': (False, (str,))})

        if _has_set(options, 'directory'):
            if options.value['directory'].value == '':
                raise _error('directory may not be empty', options.value['directory'])

    elif cmd.value == 'range':
        start = _get_required_arg(args, "start")
        _check_type(start, (int,), "start")

        stop  = _get_required_arg(args, "stop")
        _check_type(stop,  (int,), "stop")

        step  = _get_optional_arg(args, 1)
        _check_type(step,  (int,), "step")

        _require_no_more(args)

        if step.value > 0:
            if start.value > stop.value:
                msg = f"start > stop: {start.value} > {stop.value} (step={step.value})"
                raise _error(msg, step)
        elif step.value < 0:
            if stop.value > start.value:
                msg = f"stop > start: {stop.value} > {start.value} (step={step.value})"
                raise _error(msg, step)
        else:
            raise _error("step: cannot be 0", step)

    elif cmd.value in ('exec', 'exec_fast', 'exec_internal'):
        command = _get_required_arg(args, "command")
        _check_type(command, (str,), "command")
        _require_no_more(args)

    elif cmd.value == 'value_list':
        options = _get_required_arg(args, 'options')
        _require_no_more(args)

        _check_dictionary(options, {
            'values':    (True,  (list, dict)),
            'separator': (False, (str,)),
        })

        values = options.value['values']

        if len(values.value) == 0:
            raise _error('values: cannot be empty', values)

        if isinstance(values.value, dict):
            for item, desc in values.value.items():
                _check_type(item, (str,))
                _check_type(desc, (str,))
        else:
            for value in values.value:
                _check_type(value, (str,))

        if _has_set(options, 'separator'):
            separator = options.value['separator']

            if len(separator.value) != 1:
                raise _error('Invalid length for separator', separator)

    elif cmd.value == 'combine':
        commands = _get_required_arg(args, 'commands')
        _require_no_more(args)

        _check_type(commands, (list,))

        for subcommand_args in commands.value:
            _check_type(subcommand_args, (list,))

            if len(subcommand_args.value) == 0:
                raise _error('Missing command', subcommand_args)

            if subcommand_args.value[0] == 'combine':
                raise _error('Nested `combine` not allowed', subcommand_args)

            if subcommand_args.value[0] == 'none':
                raise _error('Command `none` not allowed inside combine', subcommand_args)

            _check_complete(subcommand_args)

        if len(commands.value) == 0:
            raise _error('commands: Cannot be empty', commands)

        if len(commands.value) == 1:
            raise _error('commands: Must contain more than one command', commands)

    else:
        raise _error(f'Invalid command: {cmd.value}', cmd)

def _check_option(option):
    _check_dictionary(option, {
        'option_strings':       (True,  (list,)),
        'metavar':              (False, (str,  NoneType)),
        'help':                 (False, (str,  NoneType)),
        'optional_arg':         (False, (bool, NoneType)),
        'group':                (False, (str,  NoneType)),
        'groups':               (False, (list, NoneType)),
        'repeatable':           (False, (bool, str, NoneType)),
        'multiple_option':      (False, (bool, str, NoneType)),
        'final':                (False, (bool, NoneType)),
        'hidden':               (False, (bool, NoneType)),
        'complete':             (False, (list, NoneType)),
        'when':                 (False, (str,  NoneType)),
    })

    option_strings = option.value['option_strings']

    if len(option_strings.value) == 0:
        raise _error('option_strings: cannot be empty', option_strings)

    for option_string in option_strings.value:
        _check_type(option_string, (str,), "option_string")

        if not validate_option_string(option_string.value):
            raise _error('Invalid option string', option_string)

    if _has_set(option, 'metavar') and not _has_set(option, 'complete'):
        raise _error('metavar is set but complete is missing', option)

    if _has_set(option, 'optional_arg') and not _has_set(option, 'complete'):
        raise _error('optional_arg is set but complete is missing', option)

    if _has_set(option, 'group') and _has_set(option, 'groups'):
        raise _error('Both `groups` and `group` are set', option)

    if _has_set(option, 'groups'):
        for group in option.value['groups'].value:
            _check_type(group, (str,), "group")

    if _has_set(option, 'repeatable'):
        _check_extended_bool(option.value['repeatable'])

    if _has_set(option, 'multiple_option'):
        _check_extended_bool(option.value['multiple_option'])

    if _has_set(option, 'repeatable') and _has_set(option, 'multiple_option'):
        raise _error('Both `repeatable` and `multiple_option` are set', option)

    if _has_set(option, 'complete'):
        _check_complete(option.value['complete'])

    if _has_set(option, 'when'):
        pass # TODO

def _check_positional(positional):
    _check_dictionary(positional, {
        'number':               (True,  (int,)),
        'metavar':              (False, (str,  NoneType)),
        'help':                 (False, (str,  NoneType)),
        'repeatable':           (False, (bool, NoneType)),
        'complete':             (False, (list, NoneType)),
        'when':                 (False, (str,  NoneType)),
    })

    if positional.value['number'].value < 1:
        raise _error('number cannot be zero or negative', positional.value['number'])

    if _has_set(positional, 'complete'):
        _check_complete(positional.value['complete'])

    if _has_set(positional, 'when'):
        pass # TODO

def _check_definition(definition):
    _check_dictionary(definition, {
        'prog':                 (True,  (str,)),
        'help':                 (False, (str,  NoneType)),
        'aliases':              (False, (list, NoneType)),
        'abbreviate_commands':  (False, (bool, str, NoneType)),
        'abbreviate_options':   (False, (bool, str, NoneType)),
        'inherit_options':      (False, (bool, str, NoneType)),
        'options':              (False, (list, NoneType)),
        'positionals':          (False, (list, NoneType)),
    })


    if _is_empty_or_whitespace(definition.value['prog'].value):
        raise _error('prog is empty', definition.value['prog'])

    if _has_set(definition, 'aliases'):
        for alias in definition.value['aliases'].value:
            _check_type(alias, (str,), 'alias')

            if _contains_space(alias.value):
                raise _error('alias contains space', alias)

    if _has_set(definition, 'abbreviate_commands'):
        _check_extended_bool(definition.value['abbreviate_commands'])

    if _has_set(definition, 'abbreviate_options'):
        _check_extended_bool(definition.value['abbreviate_options'])

    if _has_set(definition, 'inherit_options'):
        _check_extended_bool(definition.value['inherit_options'])

    if _has_set(definition, 'options'):
        for option in definition.value['options'].value:
            _check_option(option)

    if _has_set(definition, 'positionals'):
        for positional in definition.value['positionals'].value:
            _check_positional(positional)

def validate(definition_list):
    for definition in definition_list:
        _check_definition(definition)

    if len(definition_list) == 0:
        raise _error('No programs defined', ValueWithTrace(None, '', 1, 1))
