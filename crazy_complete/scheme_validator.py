'''Code for validating the structure of a command line definition.'''

from types import NoneType

from .cli import ExtendedBool, is_extended_bool
from .when import parse_when
from .errors import CrazyError, CrazySchemaValidationError
from .str_utils import contains_space, is_empty_or_whitespace, is_valid_option_string, is_valid_variable_name
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


# =============================================================================
# Actual validation code
# =============================================================================


def _check_extended_bool(value):
    if not is_extended_bool(value.value):
        msg = f'Invalid value. Expected true, false or "{ExtendedBool.INHERIT}"'
        raise _error(msg, value)


def _check_when(value):
    try:
        parse_when(value.value)
    except CrazyError as e:
        raise _error(f'when: {e}', value) from e


def _check_void(args):
    _require_no_more(args)


def _check_choices(args):
    choices = _get_required_arg(args, 'choices')
    _check_type(choices, (list, dict))
    _require_no_more(args)

    if isinstance(choices.value, dict):
        for value, desc in choices.value.items():
            _check_type(value, (str, int, float))
            _check_type(desc,  (str, int, float))

    elif isinstance(choices.value, list):
        for value in choices.value:
            _check_type(value, (str, int, float))


def _check_file(args):
    options = _get_optional_arg(args, {})
    _check_type(options, (dict,))
    _require_no_more(args)
    _check_dictionary(options, {'directory': (False, (str,))})

    if _has_set(options, 'directory'):
        if options.value['directory'].value == '':
            raise _error('directory may not be empty', options.value['directory'])


def _check_range(args):
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


def _check_exec(args):
    command = _get_required_arg(args, "command")
    _check_type(command, (str,), "command")
    _require_no_more(args)


def _check_value_list(args):
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


def _check_combine(args):
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


def _check_history(args):
    command = _get_required_arg(args, "pattern")
    _check_type(command, (str,), "pattern")
    _require_no_more(args)


def _check_complete(args):
    cmd = _get_required_arg(args, 'command')

    commands = {
        'none':             _check_void,
        'integer':          _check_void,
        'float':            _check_void,
        'command':          _check_void,
        'environment':      _check_void,
        'group':            _check_void,
        'hostname':         _check_void,
        'pid':              _check_void,
        'process':          _check_void,
        'service':          _check_void,
        'signal':           _check_void,
        'user':             _check_void,
        'variable':         _check_void,
        'choices':          _check_choices,
        'file':             _check_file,
        'directory':        _check_file,
        'range':            _check_range,
        'exec':             _check_exec,
        'exec_fast':        _check_exec,
        'exec_internal':    _check_exec,
        'value_list':       _check_value_list,
        'combine':          _check_combine,
        'history':          _check_history,
        # Bonus
        'mountpoint':       _check_void,
        'net_interface':    _check_void,
        'login_shell':      _check_void,
        'locale':           _check_void,
        'charset':          _check_void,
        'timezone':         _check_void,
        'alsa_card':        _check_void,
        'alsa_device':      _check_void,
    }

    if cmd.value not in commands:
        raise _error(f'Invalid command: {cmd.value}', cmd)

    commands[cmd.value](args)


def _check_option(option):
    _check_dictionary(option, {
        'option_strings':       (True,  (list,)),
        'metavar':              (False, (str,  NoneType)),
        'help':                 (False, (str,  NoneType)),
        'optional_arg':         (False, (bool, NoneType)),
        'group':                (False, (str,  NoneType)),
        'groups':               (False, (list, NoneType)),
        'repeatable':           (False, (bool, str, NoneType)),
        'final':                (False, (bool, NoneType)),
        'hidden':               (False, (bool, NoneType)),
        'complete':             (False, (list, NoneType)),
        'when':                 (False, (str,  NoneType)),
        'capture':              (False, (str,  NoneType)),
    })

    option_strings = option.value['option_strings']

    if len(option_strings.value) == 0:
        raise _error('option_strings: cannot be empty', option_strings)

    for option_string in option_strings.value:
        _check_type(option_string, (str,), "option_string")

        if not is_valid_option_string(option_string.value):
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

    if _has_set(option, 'complete'):
        _check_complete(option.value['complete'])

    if _has_set(option, 'when'):
        _check_when(option.value['when'])

    if _has_set(option, 'capture'):
        if not is_valid_variable_name(option.value['capture'].value):
            raise _error('Invalid variable name', option.value['capture'])


def _check_positional(positional):
    _check_dictionary(positional, {
        'number':               (True,  (int,)),
        'metavar':              (False, (str,  NoneType)),
        'help':                 (False, (str,  NoneType)),
        'repeatable':           (False, (bool, NoneType)),
        'complete':             (False, (list, NoneType)),
        'when':                 (False, (str,  NoneType)),
        'capture':              (False, (str,  NoneType)),
    })

    if positional.value['number'].value < 1:
        raise _error('number cannot be zero or negative', positional.value['number'])

    if _has_set(positional, 'complete'):
        _check_complete(positional.value['complete'])

    if _has_set(positional, 'when'):
        _check_when(positional.value['when'])

    if _has_set(positional, 'capture'):
        if not is_valid_variable_name(positional.value['capture'].value):
            raise _error('Invalid variable name', positional.value['capture'])


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

    if is_empty_or_whitespace(definition.value['prog'].value):
        raise _error('prog is empty', definition.value['prog'])

    if _has_set(definition, 'aliases'):
        for alias in definition.value['aliases'].value:
            _check_type(alias, (str,), 'alias')

            if contains_space(alias.value):
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
    '''Validate a list of definitions.'''

    for definition in definition_list:
        _check_definition(definition)

    if len(definition_list) == 0:
        raise _error('No programs defined', ValueWithTrace(None, '', 1, 1))
