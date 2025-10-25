'''This module contains code for validating the `complete` attribute.'''

from types import NoneType

from .errors import CrazyError, CrazyTypeError
from .type_utils import is_dict_type, is_list_type
from .str_utils import (
    is_valid_extended_regex, contains_space, is_empty_or_whitespace
)


# =============================================================================
# Helper functions
# =============================================================================


class Context:
    '''Class for providing context to validation.'''

    TYPE_OPTION = 0
    TYPE_POSITIONAL = 1

    def __init__(self):
        self.cmdline = None
        self.option = None
        self.positional = None
        self.type = None
        self.trace = None


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


def _validate_none(ctxt, args):
    if ctxt.trace and ctxt.trace[-1] in ('combine', 'list', 'prefix'):
        raise CrazyError(f'Command `none` not allowed inside {ctxt.trace[-1]}')


def _validate_command_arg(ctxt, args):
    args.require_no_more()

    if ctxt.trace and ctxt.trace[-1] in ('combine', 'list', 'key_value_list'):
        raise CrazyError(f'Command `command_arg` not allowed inside {ctxt.trace[-1]}')

    if ctxt.type != Context.TYPE_POSITIONAL:
        raise CrazyError('command_arg not allowed inside options')

    if not ctxt.positional.repeatable:
        raise CrazyError('The `command_arg` completer requires `repeatable=True`')

    def command_is_previous_to_command_arg(positional):
        return (
            positional.complete and
            positional.complete[0] == 'command' and
            positional.number + 1 == ctxt.positional.number
        )

    if not any(filter(command_is_previous_to_command_arg, ctxt.cmdline.positionals)):
        raise CrazyError('The `command_arg` completer requires a previous `command` completer')


def _validate_void(_ctxt, args):
    args.require_no_more()


def _validate_choices(_ctxt, args):
    choices = args.get_required_arg('values')
    args.require_no_more()

    if is_dict_type(choices):
        for item, desc in choices.items():
            if not isinstance(item, (str, int)):
                raise CrazyError(f'Item not a string/int: {item}')

            if not isinstance(desc, (str, int)):
                raise CrazyError(f'Description not a string/int: {desc}')

    elif is_list_type(choices):
        for item in choices:
            if not isinstance(item, (str, int)):
                raise CrazyError(f'Item not a string/int: {item}')

    else:
        raise CrazyError('values: Not a list or dictionary')


def _validate_command(_ctxt, args):
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


def _validate_filedir(_ctxt, args, with_extensions=False, with_list_opts=False):
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

        elif with_list_opts and key == 'separator':
            if not isinstance(value, str):
                raise CrazyError(f'separator: Not a string: {value}')

            if len(value) != 1:
                raise CrazyError(f'Invalid length for separator: {value}')

        elif with_list_opts and key == 'duplicates':
            if not isinstance(value, bool):
                raise CrazyError(f"duplicates: Not a bool: {value}")

        else:
            raise CrazyError(f'Unknown option: {key}')


def _validate_file(ctxt, args):
    _validate_filedir(ctxt, args, with_extensions=True)


def _validate_directory(ctxt, args):
    _validate_filedir(ctxt, args)


def _validate_file_list(ctxt, args):
    if ctxt.trace and ctxt.trace[-1] in ('combine', 'list', 'key_value_list'):
        raise CrazyError(f'Command `file_list` not allowed inside {ctxt.trace[-1]}')

    _validate_filedir(ctxt, args, with_extensions=True, with_list_opts=True)


def _validate_directory_list(ctxt, args):
    if ctxt.trace and ctxt.trace[-1] in ('combine', 'list', 'key_value_list'):
        raise CrazyError(f'Command `directory_list` not allowed inside {ctxt.trace[-1]}')

    _validate_filedir(ctxt, args, with_list_opts=True)


def _validate_mime_file(_ctxt, args):
    pattern = args.get_required_arg('pattern')
    args.require_no_more()

    if not isinstance(pattern, str):
        raise CrazyError(f"Pattern is not a string: {pattern}")

    if not is_valid_extended_regex(pattern):
        raise CrazyError(f"Pattern is not a valid extended regex: {pattern}")


def _validate_range(_ctxt, args):
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


def _validate_exec(_ctxt, args):
    cmd = args.get_required_arg('command')
    args.require_no_more()

    if not isinstance(cmd, str):
        raise CrazyError(f"Command is not a string: {cmd}")


def _validate_value_list(_ctxt, args):
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
        elif key == 'duplicates':
            if not isinstance(value, bool):
                raise CrazyError(f"duplicates: Not a bool: {value}")
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


def _validate_key_value_list(ctxt, args):
    pair_separator = args.get_required_arg('pair_separator')
    value_separator = args.get_required_arg('value_separator')
    values = args.get_required_arg('values')
    args.require_no_more()

    if 'key_value_list' in ctxt.trace:
        raise CrazyError('Nested `key_value_list` not allowed')

    if 'list' in ctxt.trace:
        raise CrazyError('Command `key_value_list` not allowed inside list')

    ctxt.trace.append('key_value_list')

    if not isinstance(pair_separator, str):
        raise CrazyError('pair_separator: Not a string')

    if not isinstance(value_separator, str):
        raise CrazyError('value_separator: Not a string')

    if not is_dict_type(values) and not is_list_type(values):
        raise CrazyError('values: Not a dict or list')

    if len(pair_separator) != 1:
        raise CrazyError('Invalid length for pair_separator')

    if len(value_separator) != 1:
        raise CrazyError('Invalid length for value_separator')

    if len(values) == 0:
        raise CrazyError('values: cannot be empty')

    if is_dict_type(values):
        for key, complete in values.items():
            if not isinstance(key, str):
                raise CrazyError(f'key: Not a string: {key}')

            if not isinstance(complete, (list, NoneType)):
                raise CrazyError(f'complete: Not a list or None: {complete}')

            if is_empty_or_whitespace(key):
                raise CrazyError('Key cannot be empty')

            if contains_space(key):
                raise CrazyError(f'Key cannot contain space: {key}')

            if complete is None:
                continue

            if len(complete) == 0:
                raise CrazyError('Missing command')

            validate_complete(ctxt, complete)
    else:
        for compldef in values:
            if not is_list_type(compldef):
                raise CrazyError(f'Completion definition not a list: {compldef}')

            if len(compldef) != 3:
                raise CrazyError(f'Completion definition must have 3 fields: {compldef}')

        for key, description, complete in values:
            if not isinstance(key, str):
                raise CrazyError(f'key: Not a string: {key}')

            if not isinstance(description, (str, NoneType)):
                raise CrazyError(f'description: Not a string or None: {description}')

            if not isinstance(complete, (list, NoneType)):
                raise CrazyError(f'complete: Not a list or None: {complete}')

            if is_empty_or_whitespace(key):
                raise CrazyError('Key cannot be empty')

            if contains_space(key):
                raise CrazyError(f'Key cannot contain space: {key}')

            if complete is None:
                continue

            if len(complete) == 0:
                raise CrazyError('Missing command')

            validate_complete(ctxt, complete)


def _validate_combine(ctxt, args):
    commands = args.get_required_arg('commands')
    args.require_no_more()

    if 'combine' in ctxt.trace:
        raise CrazyError('Nested `combine` not allowed')

    ctxt.trace.append('combine')

    if not isinstance(commands, list):
        raise CrazyError(f'combine: Not a list: {commands}')

    for subcommand_args in commands:
        if not isinstance(subcommand_args, list):
            raise CrazyError(f'combine: Not a list: {subcommand_args}')

        if len(subcommand_args) == 0:
            raise CrazyError('combine: Missing command')

        validate_complete(ctxt, subcommand_args)

    if len(commands) == 0:
        raise CrazyError('combine: Cannot be empty')

    if len(commands) == 1:
        raise CrazyError('combine: Must contain more than one command')


def _validate_list(ctxt, args):
    command = args.get_required_arg('command')
    opts = args.get_optional_arg({})
    args.require_no_more()

    if 'list' in ctxt.trace:
        raise CrazyError('Nested `list` not allowed')

    if 'key_value_list' in ctxt.trace:
        raise CrazyError('Command `list` not allowed inside key_value_list')

    ctxt.trace.append('list')

    if not isinstance(command, list):
        raise CrazyError(f'list: Not a list: {command}')

    if len(command) == 0:
        raise CrazyError('list: Missing command')

    if not is_dict_type(opts):
        raise CrazyTypeError('options', 'dict', opts)

    for key, value in opts.items():
        if key == 'separator':
            if not isinstance(value, str):
                raise CrazyError(f'separator: Not a string: {value}')

            if len(value) != 1:
                raise CrazyError(f'Invalid length for separator: {value}')
        elif key == 'duplicates':
            if not isinstance(value, bool):
                raise CrazyError(f"duplicates: Not a bool: {value}")
        else:
            raise CrazyError(f'Unknown option: {key}')

    validate_complete(ctxt, command)


def _validate_prefix(ctxt, args):
    prefix = args.get_required_arg('prefix')
    command = args.get_required_arg('command')
    args.require_no_more()

    if 'prefix' in ctxt.trace:
        raise CrazyError('Nested `prefix` not allowed')

    if 'key_value_list' in ctxt.trace:
        raise CrazyError('Command `list` not allowed inside key_value_list')

    if not isinstance(command, list):
        raise CrazyError(f'prefix: Not a list: {command}')

    if len(command) == 0:
        raise CrazyError('prefix: Missing command')

    ctxt.trace.append('prefix')
    validate_complete(ctxt, command)


def _validate_history(_ctxt, args):
    pattern = args.get_required_arg('pattern')
    args.require_no_more()

    if not isinstance(pattern, str):
        raise CrazyError(f"Pattern is not a string: {pattern}")

    if not is_valid_extended_regex(pattern):
        raise CrazyError(f"Pattern is not a valid extended regex: {pattern}")


def _validate_date(_ctxt, args):
    format_ = args.get_required_arg('format')
    args.require_no_more()

    if not isinstance(format_, str):
        raise CrazyError(f"Format is not a string: {format_}")

    if is_empty_or_whitespace(format_):
        raise CrazyError('Format: Cannot be empty')


# =============================================================================
# Real validation functions
# =============================================================================


_COMMANDS = {
    'alsa_card':          _validate_void,
    'alsa_device':        _validate_void,
    'charset':            _validate_void,
    'choices':            _validate_choices,
    'combine':            _validate_combine,
    'command':            _validate_command,
    'command_arg':        _validate_command_arg,
    'commandline_string': _validate_void,
    'date':               _validate_date,
    'date_format':        _validate_void,
    'directory':          _validate_directory,
    'directory_list':     _validate_directory_list,
    'environment':        _validate_void,
    'exec':               _validate_exec,
    'exec_fast':          _validate_exec,
    'exec_internal':      _validate_exec,
    'file':               _validate_file,
    'file_list':          _validate_file_list,
    'filesystem_type':    _validate_void,
    'float':              _validate_void,
    'gid':                _validate_void,
    'group':              _validate_void,
    'history':            _validate_history,
    'hostname':           _validate_void,
    'integer':            _validate_void,
    'key_value_list':     _validate_key_value_list,
    'list':               _validate_list,
    'locale':             _validate_void,
    'login_shell':        _validate_void,
    'mime_file':          _validate_mime_file,
    'mountpoint':         _validate_void,
    'net_interface':      _validate_void,
    'none':               _validate_none,
    'pid':                _validate_void,
    'process':            _validate_void,
    'prefix':             _validate_prefix,
    'range':              _validate_range,
    'service':            _validate_void,
    'signal':             _validate_void,
    'timezone':           _validate_void,
    'uid':                _validate_void,
    'user':               _validate_void,
    'value_list':         _validate_value_list,
    'variable':           _validate_void,
}


def validate_complete(ctxt, complete):
    '''Validate a completion command.'''

    if not complete:
        return

    args = Arguments(complete)
    command = args.get_required_arg('command')

    if not isinstance(command, str):
        raise CrazyError(f"Command is not a string: {command}")

    if command not in _COMMANDS:
        raise CrazyError(f"Unknown command for `complete`: {command}")

    _COMMANDS[command](ctxt, args)


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


def validate_wraps(cmdline):
    '''Check for the right usage of `wraps`.'''

    if cmdline.wraps is not None:
        if is_empty_or_whitespace(cmdline.wraps):
            raise CrazyError('wraps is empty')

        if contains_space(cmdline.get_command_path()):
            raise CrazyError('wraps not allowed in subcommands')


def validate_commandline(cmdline):
    '''Validate completion commands of options/positionals in a commandline.'''

    context = Context()
    context.cmdline = cmdline

    context.type = Context.TYPE_OPTION
    for option in cmdline.get_options():
        try:
            context.trace = []
            context.option = option
            validate_complete(context, option.complete)
        except CrazyError as e:
            raise CrazyError("%s: %s: %s" % (
                cmdline.get_command_path(),
                '|'.join(option.option_strings),
                e)) from e

    context.type = Context.TYPE_POSITIONAL
    for positional in cmdline.get_positionals():
        try:
            context.trace = []
            context.positional = positional
            validate_complete(context, positional.complete)
        except CrazyError as e:
            raise CrazyError("%s: positional %d (%s): %s" % (
                cmdline.get_command_path(),
                positional.number,
                positional.metavar or 'unnamed',
                e)) from e

    try:
        validate_positionals_repeatable(cmdline)
        validate_wraps(cmdline)
    except CrazyError as e:
        raise CrazyError("%s: %s" % (cmdline.get_command_path(), e)) from e


def validate_commandlines(cmdline):
    '''Validate completion commands of options/positionals in all commandlines.'''

    cmdline.visit_commandlines(validate_commandline)
