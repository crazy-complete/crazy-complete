'''This module contains code for validating the `complete` attribute.'''

from .errors import CrazyError, CrazyTypeError
from .type_utils import is_dict_type, is_list_type
from .str_utils import (
    is_valid_extended_regex, contains_space, is_empty_or_whitespace
)

# =============================================================================
# Helper functions
# =============================================================================


class Arguments:
    '''Class for accessing arguments.'''

    def __init__(self, args):
        self.args = args
        self.index = 0

    def get_required_arg(self, name):
        '''Return a required argument, else raise an exception.'''

        if self.index < len(self.args):
            arg = self.args[self.index]
            self.index += 1
            return arg

        raise CrazyError(f'Missing argument: {name}')

    def get_optional_arg(self, default=None):
        '''Return an optional arg, else return a default.'''

        if self.index < len(self.args):
            arg = self.args[self.index]
            self.index += 1
            return arg

        return default

    def require_no_more(self):
        '''Raise an exception if there are any arguments left.'''

        if self.index < len(self.args):
            raise CrazyError(f'Too many arguments: {self.args[self.index:]}')


# =============================================================================
# Command validation functions
# =============================================================================


def _validate_none(_args):
    pass


def _validate_void(args):
    args.require_no_more()


def _validate_choices(args):
    choices = args.get_required_arg('values')
    args.require_no_more()

    if is_dict_type(choices):
        for item, desc in choices.items():
            if not isinstance(item, (str, int, float)):
                raise CrazyError(f'Item not a string/int/float: {item}')

            if not isinstance(desc, (str, int, float)):
                raise CrazyError(f'Description not a string/int/float: {desc}')

    elif is_list_type(choices):
        for item in choices:
            if not isinstance(item, (str, int, float)):
                raise CrazyError(f'Item not a string/int/float: {item}')

    else:
        raise CrazyError('values: Not a list or dictionary')


def _validate_command(args):
    opts = args.get_optional_arg({})
    args.require_no_more()

    path = None
    append = None
    prepend = None

    if not is_dict_type(opts):
        raise CrazyTypeError('options', 'dict', opts)

    for key, value in opts.items():
        if key == 'path':
            path = value
        elif key == 'path_append':
            append = value
        elif key == 'path_prepend':
            prepend = value
        else:
            raise CrazyError(f'Unknown option: {key}')

        if not isinstance(value, str):
            raise CrazyError(f'{key}: Not a string: {value}')

        if is_empty_or_whitespace(value):
            raise CrazyError(f'{key}: Cannot be empty')

    if path and (append or prepend):
        raise CrazyError('command: path_append/path_prepend cannot be used with path')


def _validate_filedir(args, with_extensions=False, with_separator=False):
    opts = args.get_optional_arg({})
    args.require_no_more()

    if not is_dict_type(opts):
        raise CrazyTypeError('options', 'dict', opts)

    for key, value in opts.items():
        if key == 'directory':
            if not isinstance(value, str):
                raise CrazyError(f"directory: Not a string: {value}")

            if value == '':
                raise CrazyError('directory: Cannot be empty')

            if not value.startswith('/'):
                raise CrazyError('directory: Must be an absolute path')

        elif with_extensions and key == 'extensions':
            if not is_list_type(value):
                raise CrazyError(f"extensions: Not a list: {value}")

            if len(value) == 0:
                raise CrazyError("extensions: Cannot be empty")

            for i, subval in enumerate(value):
                if not isinstance(subval, str):
                    raise CrazyError(f"extensions[{i}]: Not a string: {subval}")

                if subval == '':
                    raise CrazyError(f"extensions[{i}]: Cannot be empty")

                if contains_space(subval):
                    raise CrazyError(f"extensions[{i}]: Contains space: {subval}")

        elif with_extensions and key == 'fuzzy':
            if not isinstance(value, bool):
                raise CrazyError(f"fuzzy: Not a bool: {value}")

        elif with_separator and key == 'separator':
            if not isinstance(value, str):
                raise CrazyError(f'separator: Not a string: {value}')

            if len(value) != 1:
                raise CrazyError(f'Invalid length for separator: {value}')

        else:
            raise CrazyError(f'Unknown option: {key}')


def _validate_file(args):
    _validate_filedir(args, with_extensions=True)


def _validate_directory(args):
    _validate_filedir(args)


def _validate_file_list(args):
    _validate_filedir(args, with_extensions=True, with_separator=True)


def _validate_directory_list(args):
    _validate_filedir(args, with_separator=True)


def _validate_mime_file(args):
    pattern = args.get_required_arg('pattern')
    args.require_no_more()

    if not isinstance(pattern, str):
        raise CrazyError(f"Pattern is not a string: {pattern}")

    if not is_valid_extended_regex(pattern):
        raise CrazyError(f"Pattern is not a valid extended regex: {pattern}")


def _validate_range(args):
    start = args.get_required_arg("start")
    stop  = args.get_required_arg("stop")
    step  = args.get_optional_arg(1)
    args.require_no_more()

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
    cmd = args.get_required_arg('command')
    args.require_no_more()

    if not isinstance(cmd, str):
        raise CrazyError(f"Command is not a string: {cmd}")


def _validate_value_list(args):
    opts = args.get_required_arg('options')
    args.require_no_more()

    if not is_dict_type(opts):
        raise CrazyTypeError('options', 'dict', opts)

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

    if not is_list_type(values) and not is_dict_type(values):
        raise CrazyError(f'values: not a list|dictionary: {values}')

    if len(values) == 0:
        raise CrazyError('values: cannot be empty')

    if is_dict_type(values):
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
    commands = args.get_required_arg('commands')
    args.require_no_more()

    if not isinstance(commands, list):
        raise CrazyError(f'combine: Not a list: {commands}')

    for subcommand_args in commands:
        if not isinstance(subcommand_args, list):
            raise CrazyError(f'combine: Not a list: {subcommand_args}')

        if len(subcommand_args) == 0:
            raise CrazyError('combine: Missing command')

        if subcommand_args[0] == 'combine':
            raise CrazyError('Nested `combine` not allowed')

        if subcommand_args[0] == 'none':
            raise CrazyError('Command `none` not allowed inside combine')

        if subcommand_args[0] == 'command_arg':
            raise CrazyError('Command `command_arg` not allowed inside combine')

        if subcommand_args[0] == 'list':
            raise CrazyError('Command `list` not allowed inside combine')

        validate_complete(subcommand_args)

    if len(commands) == 0:
        raise CrazyError('combine: Cannot be empty')

    if len(commands) == 1:
        raise CrazyError('combine: Must contain more than one command')


def _validate_list(args):
    command = args.get_required_arg('command')
    opts = args.get_optional_arg({})
    args.require_no_more()

    if not isinstance(command, list):
        raise CrazyError(f'list: Not a list: {command}')

    if len(command) == 0:
        raise CrazyError('list: Missing command')

    if command[0] == 'list':
        raise CrazyError('Nested `list` not allowed')

    if command[0] == 'none':
        raise CrazyError('Command `none` not allowed inside list')

    if command[0] == 'command_arg':
        raise CrazyError('Command `command_arg` not allowed inside list')

    if command[0] == 'file':
        raise CrazyError('Command `file` not allowed inside list. Use `file_list` instead')

    if command[0] == 'directory':
        raise CrazyError('Command `directory` not allowed inside list. Use `directory_list` instead')

    if not is_dict_type(opts):
        raise CrazyTypeError('options', 'dict', opts)

    for key, value in opts.items():
        if key == 'separator':
            if not isinstance(value, str):
                raise CrazyError(f'separator: Not a string: {value}')

            if len(value) != 1:
                raise CrazyError(f'Invalid length for separator: {value}')
        else:
            raise CrazyError(f'Unknown option: {key}')

    validate_complete(command)


def _validate_history(args):
    pattern = args.get_required_arg('pattern')
    args.require_no_more()

    if not isinstance(pattern, str):
        raise CrazyError(f"Pattern is not a string: {pattern}")

    if not is_valid_extended_regex(pattern):
        raise CrazyError(f"Pattern is not a valid extended regex: {pattern}")


def _validate_date(args):
    format_ = args.get_required_arg('format')
    args.require_no_more()

    if not isinstance(format_, str):
        raise CrazyError(f"Format is not a string: {format_}")

    if is_empty_or_whitespace(format_):
        raise CrazyError('Format: Cannot be empty')


# =============================================================================
# Real validation functions
# =============================================================================


def validate_complete(complete):
    '''Validate a completion command.'''

    if not complete:
        return

    args = Arguments(complete)
    command = args.get_required_arg('command')

    if not isinstance(command, str):
        raise CrazyError(f"Command is not a string: {command}")

    validate_commands = {
        'none':          _validate_none,
        'integer':       _validate_void,
        'float':         _validate_void,
        'command':       _validate_command,
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
        'directory':     _validate_directory,
        'mime_file':     _validate_mime_file,
        'range':         _validate_range,
        'exec':          _validate_exec,
        'exec_fast':     _validate_exec,
        'exec_internal': _validate_exec,
        'value_list':    _validate_value_list,
        'combine':       _validate_combine,
        'list':          _validate_list,
        'history':       _validate_history,
        'commandline_string': _validate_void,
        'command_arg':   _validate_void,
        'date':          _validate_date,
        'date_format':   _validate_void,
        'file_list':     _validate_file_list,
        'directory_list': _validate_directory_list,
        # Bonus
        'mountpoint':    _validate_void,
        'net_interface': _validate_void,
        'login_shell':   _validate_void,
        'locale':        _validate_void,
        'charset':       _validate_void,
        'timezone':      _validate_void,
        'alsa_card':     _validate_void,
        'alsa_device':   _validate_void,
    }

    if command not in validate_commands:
        raise CrazyError(f"Unknown command for `complete`: {command}")

    validate_commands[command](args)


def validate_positionals_repeatable(cmdline):
    '''Validate positional argument definitions.'''

    repeatable_number = None
    positionals = cmdline.get_positionals()

    for positional in sorted(positionals, key=lambda p: p.number):
        repeatable = positional.repeatable
        positional_number = positional.get_positional_num()

        if repeatable:
            if repeatable_number is not None and repeatable_number != positional_number:
                raise CrazyError('Only one positional argument can be marked as repeatable')
            else:
                repeatable_number = positional_number
        elif repeatable_number is not None and positional_number > repeatable_number:
            raise CrazyError('A positional argument cannot follow a repeatable positional argument')

    if cmdline.get_subcommands() and repeatable_number is not None:
        raise CrazyError('Repeatable positionals and subcommands cannot be used together')


def validate_positionals_command_arg(cmdline):
    '''Check for the right usage of `command_arg`.'''

    positionals = cmdline.get_positionals()
    command_position = None

    for positional in sorted(positionals, key=lambda p: p.number):
        complete = positional.complete or ['none']
        positional_number = positional.get_positional_num()

        if complete[0] == 'command':
            command_position = positional_number

        elif complete[0] == 'command_arg':
            if not positional.repeatable:
                raise CrazyError('The `command_arg` completer requires `repeatable=True`')

            if command_position is None or command_position + 1 != positional_number:
                raise CrazyError('The `command_arg` completer requires a previous `command` completer')


def validate_wraps(cmdline):
    '''Check for the right usage of `wraps`.'''

    if cmdline.wraps is not None:
        if is_empty_or_whitespace(cmdline.wraps):
            raise CrazyError('wraps is empty')

        if contains_space(cmdline.get_command_path()):
            raise CrazyError('wraps not allowed in subcommands')


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

    try:
        validate_positionals_repeatable(cmdline)
        validate_positionals_command_arg(cmdline)
        validate_wraps(cmdline)
    except CrazyError as e:
        raise CrazyError("%s: %s" % (cmdline.get_command_path(), e)) from e


def validate_commandlines(cmdline):
    '''Validate completion commands of options/positionals in all commandlines.'''

    cmdline.visit_commandlines(validate_commandline)
