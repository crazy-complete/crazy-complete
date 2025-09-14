'''This module contains code for validating the `complete` attribute.'''

from .errors import CrazyError, CrazyTypeError

# =============================================================================
# Helper functions
# =============================================================================

def _get_required_arg(args, name):
    try:
        return args.pop(0)
    except IndexError:
        raise CrazyError(f'Missing argument: {name}') from None

def _get_optional_arg(args, default=None):
    try:
        return args.pop(0)
    except IndexError:
        return default

def _require_no_more(args):
    if args:
        raise CrazyError(f'Too many arguments: {args}')

# =============================================================================
# Command validation functions
# =============================================================================

def _validate_none(_args):
    pass

def _validate_void(args):
    _require_no_more(args)

def _validate_choices(args):
    choices = _get_required_arg(args, 'values')
    _require_no_more(args)

    if hasattr(choices, 'items'):
        for item, desc in choices.items():
            if not isinstance(item, (str, int, float)):
                raise CrazyError(f'Item not a string/int/float: {item}')

            if not isinstance(desc, (str, int, float)):
                raise CrazyError(f'Description not a string/int/float: {desc}')

    elif isinstance(choices, (list, tuple)):
        for item in choices:
            if not isinstance(item, (str, int, float)):
                raise CrazyError(f'Item not a string/int/float: {item}')

    else:
        raise CrazyError('values: Not a list or dictionary')

def _validate_file(args):
    opts = _get_optional_arg(args, {})
    _require_no_more(args)

    if not isinstance(opts, dict):
        raise CrazyTypeError('options', 'dict', opts)

    for key, value in opts.items():
        if key == 'directory':
            if not isinstance(value, str):
                raise CrazyError(f"directory: Not a string: {value}")

            if value == '':
                raise CrazyError('directory: Cannot be empty')
        else:
            raise CrazyError(f'Unknown option: {key}')

def _validate_range(args):
    start = _get_required_arg(args, "start")
    stop  = _get_required_arg(args, "stop")
    step  = _get_optional_arg(args, 1)
    _require_no_more(args)

    if not isinstance(start, int):
        raise CrazyError(f"start: not an int: {start}")

    if not isinstance(stop, int):
        raise CrazyError(f"stop: not an int: {stop}")

    if not isinstance(step, int):
        raise CrazyError(f"step: not an int: {step}")

    if step > 0:
        if start > stop:
            raise CrazyError(f"start > stop: {start} > {stop} (step={step})")
    elif step < 0:
        if stop > start:
            raise CrazyError(f"stop > start: {stop} > {start} (step={step})")
    else:
        raise CrazyError("step: cannot be 0")

def _validate_exec(args):
    cmd = _get_required_arg(args, 'command')
    _require_no_more(args)

    if not isinstance(cmd, str):
        raise CrazyError(f"Command is not a string: {cmd}")

def _validate_value_list(args):
    opts = _get_required_arg(args, 'options')
    _require_no_more(args)

    values = None
    separator = ','

    for key, value in opts.items():
        if key == 'values':
            values = value
        elif key == 'separator':
            separator = value
        else:
            raise CrazyError(f'Unknown option: {key}')

    if values is None:
        raise CrazyError(f'Missing `values` option: {opts}')

    if not isinstance(values, (list, tuple)) and not hasattr(values, 'items'):
        raise CrazyError(f'values: not a list|dictionary: {values}')

    if len(values) == 0:
        raise CrazyError('values: cannot be empty')

    if hasattr(values, 'items'):
        for item, desc in values.items():
            if not isinstance(item, str):
                raise CrazyError(f'values: Not a string: {item}')

            if not isinstance(desc, str):
                raise CrazyError(f'values: Not a string: {desc}')
    else:
        for index, value in enumerate(values):
            if not isinstance(value, str):
                raise CrazyError(f'values[{index}]: Not a string: {value}')

    if not isinstance(separator, str):
        raise CrazyError(f'separator: Not a string: {separator}')

    if len(separator) != 1:
        raise CrazyError(f'Invalid length for separator: {separator}')

def _validate_combine(args):
    commands = _get_required_arg(args, 'commands')
    _require_no_more(args)

    if not isinstance(commands, list):
        raise CrazyError(f'commands: Not a list: {commands}')

    for subcommand_args in commands:
        if not isinstance(subcommand_args, list):
            raise CrazyError(f'combine: Not a list: {subcommand_args}')

        if len(subcommand_args) == 0:
            raise CrazyError('combine: Missing command')

        if subcommand_args[0] == 'combine':
            raise CrazyError('Nested `combine` not allowed')

        if subcommand_args[0] == 'none':
            raise CrazyError('Command `none` not allowed inside combine')

        validate_complete(subcommand_args)

    if len(commands) == 0:
        raise CrazyError('commands: Cannot be empty')

    if len(commands) == 1:
        raise CrazyError('commands: Must contain more than one command')

# =============================================================================
# Real validation functions
# =============================================================================

def validate_complete(complete):
    '''Validate a completion command.'''

    if not complete:
        return

    command, *args = complete

    if not isinstance(command, str):
        raise CrazyError(f"Command is not a string: {command}")

    validate_commands = {
        'none':          _validate_none,
        'integer':       _validate_void,
        'float':         _validate_void,
        'command':       _validate_void,
        'group':         _validate_void,
        'hostname':      _validate_void,
        'pid':           _validate_void,
        'process':       _validate_void,
        'user':          _validate_void,
        'service':       _validate_void,
        'signal':        _validate_void,
        'variable':      _validate_void,
        'environment':   _validate_void,
        'choices':       _validate_choices,
        'file':          _validate_file,
        'directory':     _validate_file,
        'range':         _validate_range,
        'exec':          _validate_exec,
        'exec_fast':     _validate_exec,
        'exec_internal': _validate_exec,
        'value_list':    _validate_value_list,
        'combine':       _validate_combine,
    }

    if command not in validate_commands:
        raise CrazyError(f"Unknown command for `complete`: {command}")

    validate_commands[command](args)

def validate_commandline(cmdline):
    '''Validate completion commands of options/positionals in a commandline.'''

    for option in cmdline.get_options():
        try:
            validate_complete(option.complete)
        except CrazyError as e:
            raise CrazyError("%s: %s: %s" % (
                cmdline.get_command_path(),
                '|'.join(option.option_strings),
                e)) from e

    for positional in cmdline.get_positionals():
        try:
            validate_complete(positional.complete)
        except CrazyError as e:
            raise CrazyError("%s: %d (%s): %s" % (
                cmdline.get_command_path(),
                positional.number,
                positional.metavar,
                e)) from e

def validate_commandlines(cmdline):
    '''Validate completion commands of options/positionals in all commandlines.'''

    cmdline.visit_commandlines(validate_commandline)
