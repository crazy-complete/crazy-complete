'''This module contains code for validating the `complete` attribute.'''

from types import NoneType

from .errors import CrazyError, CrazyTypeError
from .type_utils import is_dict_type, is_list_type
from .str_utils import (
    is_valid_extended_regex, contains_space, is_empty_or_whitespace
)
from . import messages as m


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

        raise CrazyError('%s: %s' % (m.missing_arg(), name))

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
            args = self.args[self.index:]
            msg = '%s: %s' % (m.too_many_arguments(), args)
            raise CrazyError(msg)


def _validate_type(value, types, parameter_name):
    okay = False

    if list in types and is_list_type(value):
        okay = True

    if not okay and not isinstance(value, types):
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

        raise CrazyTypeError(parameter_name, types_string, value)


def _validate_dictionary(dictionary, rules):
    for key, value in dictionary.items():
        if key not in rules:
            msg = '%s: %s' % (m.unknown_parameter(), key)
            raise CrazyError(msg)

        _validate_type(value, rules[key][1], key)

        if rules[key][2]:
            rules[key][2](value, key)

    for key, rule in rules.items():
        if rule[0] is True and key not in dictionary:
            msg = '%s: %s' % (m.missing_arg(), key)
            raise CrazyError(msg)


def _validate_non_empty_string(string, parameter):
    if is_empty_or_whitespace(string):
        msg = '%s: %s' % (parameter, m.string_cannot_be_empty())
        raise CrazyError(msg)


def _validate_non_empty_list(value, parameter):
    if len(value) == 0:
        raise CrazyError('%s: %s' % (parameter, m.list_cannot_be_empty()))


def _validate_non_empty_dict(value, parameter):
    if len(value) == 0:
        raise CrazyError('%s: %s' % (parameter, m.dict_cannot_be_empty()))


def _validate_char(string, parameter):
    if len(string) != 1:
        msg = '%s: %s' % (parameter, m.single_charater_expected())
        raise CrazyError(msg)


def _validate_regex(pattern, parameter):
    if not is_valid_extended_regex(pattern):
        msg = '%s: %s' % (parameter, m.not_an_extended_regex())
        raise CrazyError(msg)


def _validate_no_spaces(string, parameter):
    if contains_space(string):
        msg = '%s: %s' % (parameter, m.string_cannot_contain_space())
        raise CrazyError(msg)


# =============================================================================
# Command validation functions
# =============================================================================


def _validate_none(ctxt, _args):
    if ctxt.trace and ctxt.trace[-1] in ('combine', 'list', 'prefix'):
        msg = m.completer_not_allowed_in('none', ctxt.trace[-1])
        raise CrazyError(msg)


def _validate_command_arg(ctxt, args):
    args.require_no_more()

    if ctxt.trace and ctxt.trace[-1] in ('combine', 'list', 'key_value_list'):
        msg = m.completer_not_allowed_in('command_arg', ctxt.trace[-1])
        raise CrazyError(msg)

    if ctxt.type != Context.TYPE_POSITIONAL:
        msg = m.completer_not_allowed_in_option('command_arg')
        raise CrazyError(msg)

    if not ctxt.positional.repeatable:
        msg = m.completer_requires_repeatable('command_arg')
        raise CrazyError(msg)

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

    _validate_type(choices, (dict, list), 'values')

    if is_dict_type(choices):
        for item, desc in choices.items():
            _validate_type(item, (str, int), 'item')
            _validate_type(desc, (str, int), 'description')

    elif is_list_type(choices):
        for item in choices:
            _validate_type(item, (str, int), 'item')


def _validate_command(_ctxt, args):
    opts = args.get_optional_arg({})
    args.require_no_more()

    _validate_type(opts, (dict,), 'options')
    _validate_dictionary(opts, {
        'path':         (False, (str,), _validate_non_empty_string),
        'path_append':  (False, (str,), _validate_non_empty_string),
        'path_prepend': (False, (str,), _validate_non_empty_string),
    })

    path = opts.get('path', None)
    append = opts.get('path_append', None)
    prepend = opts.get('path_prepend', None)

    if path and (append or prepend):
        raise CrazyError('path_append/path_prepend cannot be used with path')


def _validate_filedir(_ctxt, args, with_extensions=False, with_list_opts=False):
    opts = args.get_optional_arg({})
    args.require_no_more()

    _validate_type(opts, (dict,), 'options')

    spec = {'directory': (False, (str,), _validate_non_empty_string)}
    if with_extensions:
        spec['extensions'] = (False, (list,), None)
        spec['fuzzy'] = (False, (bool,), None)
    if with_list_opts:
        spec['separator'] = (False, (str,), _validate_char)
        spec['duplicates'] = (False, (bool,), None)

    _validate_dictionary(opts, spec)

    if 'directory' in opts:
        if not opts['directory'].startswith('/'):
            msg = '%s: %s' % ('directory', m.not_an_absolute_path())
            raise CrazyError(msg)

    if 'extensions' in opts:
        value = opts['extensions']

        _validate_non_empty_list(value, 'extensions')

        for i, subval in enumerate(value):
            _validate_type(subval, (str,), f'extensions[{i}]')
            _validate_non_empty_string(subval, f'extensions[{i}]')
            _validate_no_spaces(subval, f'extensions[{i}]')


def _validate_file(ctxt, args):
    _validate_filedir(ctxt, args, with_extensions=True)


def _validate_directory(ctxt, args):
    _validate_filedir(ctxt, args)


def _validate_file_list(ctxt, args):
    _validate_filedir(ctxt, args, with_extensions=True, with_list_opts=True)


def _validate_directory_list(ctxt, args):
    _validate_filedir(ctxt, args, with_list_opts=True)


def _validate_mime_file(_ctxt, args):
    pattern = args.get_required_arg('pattern')
    args.require_no_more()
    _validate_type(pattern, (str,), 'pattern')
    _validate_regex(pattern, 'pattern')


def _validate_range(_ctxt, args):
    start = args.get_required_arg("start")
    stop = args.get_required_arg("stop")
    step = args.get_optional_arg(1)
    args.require_no_more()

    _validate_type(start, (int,), 'start')
    _validate_type(stop, (int,), 'stop')
    _validate_type(step, (int,), 'step')

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
    _validate_type(cmd, (str,), 'command')


def _validate_value_list(_ctxt, args):
    opts = args.get_required_arg('options')
    args.require_no_more()

    _validate_type(opts, (dict,), 'options')
    _validate_dictionary(opts, {
        'values':     (True,  (dict, list), None),
        'separator':  (False, (str,), _validate_char),
        'duplicates': (False, (bool,), None)
    })

    values = opts['values']

    if is_dict_type(values):
        _validate_non_empty_dict(values, 'values')

        for item, desc in values.items():
            _validate_type(item, (str,), 'values (item)')
            _validate_type(desc, (str,), 'values (description)')
    else:
        _validate_non_empty_list(values, 'values')

        for index, value in enumerate(values):
            _validate_type(value, (str,), f'values[{index}]')


def _validate_key_value_list(ctxt, args):
    pair_separator = args.get_required_arg('pair_separator')
    value_separator = args.get_required_arg('value_separator')
    values = args.get_required_arg('values')
    args.require_no_more()

    ctxt.trace.append('key_value_list')

    _validate_type(pair_separator, (str,), 'pair_separator')
    _validate_type(value_separator, (str,), 'value_separator')
    _validate_type(values, (dict, list), 'values')

    _validate_char(pair_separator, 'pair_separator')
    _validate_char(value_separator, 'value_separator')

    if is_dict_type(values):
        _validate_non_empty_dict(values, 'values')

        for key, complete in values.items():
            _validate_type(key, (str,), 'key')
            _validate_type(complete, (list, NoneType), 'completer')
            _validate_non_empty_string(key, 'key')
            _validate_no_spaces(key, 'key')

            if complete is None:
                continue

            validate_complete(ctxt, complete)
    else:
        _validate_non_empty_list(values, 'values')

        for compldef in values:
            if not is_list_type(compldef):
                raise CrazyError(f'Completion definition not a list: {compldef}')

            if len(compldef) != 3:
                raise CrazyError(f'Completion definition must have 3 fields: {compldef}')

        for key, description, complete in values:
            _validate_type(key, (str,), 'key')
            _validate_non_empty_string(key, 'key')
            _validate_no_spaces(key, 'key')
            _validate_type(description, (str, NoneType), 'description')
            _validate_type(complete, (list, NoneType), 'completer')

            if complete is None:
                continue

            validate_complete(ctxt, complete)


def _validate_combine(ctxt, args):
    commands = args.get_required_arg('commands')
    args.require_no_more()

    _validate_type(commands, (list,), 'commands')
    _validate_non_empty_list(commands, 'commands')

    if len(commands) == 1:
        msg = '%s: %s' % ('commands', m.list_must_contain_at_least_two_items())
        raise CrazyError(msg)

    ctxt.trace.append('combine')

    for subcommand_args in commands:
        _validate_type(subcommand_args, (list,), 'subcommand')
        validate_complete(ctxt, subcommand_args)


def _validate_list(ctxt, args):
    command = args.get_required_arg('command')
    opts = args.get_optional_arg({})
    args.require_no_more()

    _validate_type(command, (list,), 'command')

    _validate_type(opts, (dict,), 'options')
    _validate_dictionary(opts, {
        'separator': (False, (str,), _validate_char),
        'duplicates': (False, (bool,), None)
     })

    ctxt.trace.append('list')
    validate_complete(ctxt, command)


def _validate_prefix(ctxt, args):
    prefix = args.get_required_arg('prefix')
    command = args.get_required_arg('command')
    args.require_no_more()

    _validate_non_empty_string(prefix, 'prefix')
    _validate_type(command, (list,), 'command')
    ctxt.trace.append('prefix')
    validate_complete(ctxt, command)


def _validate_history(_ctxt, args):
    pattern = args.get_required_arg('pattern')
    args.require_no_more()
    _validate_type(pattern, (str,), 'pattern')
    _validate_regex(pattern, 'pattern')


def _validate_date(_ctxt, args):
    format_ = args.get_required_arg('format')
    args.require_no_more()
    _validate_type(format_, (str,), 'format')
    _validate_non_empty_string(format_, 'format')


def _validate_ip_address(_ctxt, args):
    type_ = args.get_optional_arg('all')
    args.require_no_more()
    _validate_type(type_, (str,), 'type')

    if type_ not in ('ipv4', 'ipv6', 'all'):
        msg = '%s: %s' % ('type', m.invalid_value('ipv4, ipv6, all'))
        raise CrazyError(msg)


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
    'ip_address':         _validate_ip_address,
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

    if complete is None:
        return

    args = Arguments(complete)
    command = args.get_required_arg('command')

    _validate_type(command, (str,), 'command')

    if command not in _COMMANDS:
        msg = '%s: %s' % (m.unknown_completer(), command)
        raise CrazyError(msg)

    try:
        _COMMANDS[command](ctxt, args)
    except CrazyError as e:
        raise CrazyError(f'{command}: {e}') from e


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
        _validate_non_empty_string(cmdline.wraps, 'wraps')

        if contains_space(cmdline.get_command_path()):
            msg = m.parameter_not_allowed_in_subcommand('wraps')
            raise CrazyError(msg)


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
