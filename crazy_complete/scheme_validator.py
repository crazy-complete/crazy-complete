'''Code for validating the structure of a command line definition.'''

from types import NoneType

from .cli import ExtendedBool, is_extended_bool
from .when import parse_when
from .errors import CrazyError, CrazySchemaValidationError
from .value_with_trace import ValueWithTrace
from .str_utils import (
    contains_space, is_empty_or_whitespace,
    is_valid_option_string, is_valid_variable_name,
    is_valid_extended_regex, validate_prog)


_error = CrazySchemaValidationError


# =============================================================================
# Helper functions for validating
# =============================================================================


class Context:
    '''Class for providing context to validation.'''

    TYPE_OPTION = 0
    TYPE_POSITIONAL = 1

    def __init__(self):
        self.definition = None
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

        if self.index < len(self.args.value):
            arg = self.args.value[self.index]
            self.index += 1
            return arg

        raise _error(f'Missing required arg `{name}`', self.args)

    def get_optional_arg(self, default=None):
        '''Return an optional arg, else return a default.'''

        if self.index < len(self.args.value):
            arg = self.args.value[self.index]
            self.index += 1
            return arg

        return ValueWithTrace(default, '<default value>', 1, 1)

    def require_no_more(self):
        '''Raise an exception if there are any arguments left.'''

        if self.index < len(self.args.value):
            raise _error('Too many arguments provided', self.args)


def _has_set(dictionary, key):
    return (key in dictionary.value and dictionary.value[key].value is not None)


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

        if rules[key.value][2]:
            rules[key.value][2](value, key.value)

    for key, rule in rules.items():
        if rule[0] is True and key not in dictionary.value:
            raise _error(f'Missing required key: {key}', dictionary)


def _check_regex(value, parameter):
    if not is_valid_extended_regex(value.value):
        raise _error(f"{parameter}: Not a valid extended regex", value)


def _check_char(value, parameter):
    if len(value.value) != 1:
        raise _error(f'{parameter}: Invalid length. Single character expected.', value)


def _check_non_empty_string(value, parameter):
    if is_empty_or_whitespace(value.value):
        raise _error(f'{parameter}: Cannot be empty', value)


def _check_no_spaces(value, parameter):
    if contains_space(value.value):
        raise _error(f'{parameter}: Cannot contain space', value)


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


def _check_void(_ctxt, arguments):
    arguments.require_no_more()


def _check_none(ctxt, arguments):
    arguments.require_no_more()

    if ctxt.trace and ctxt.trace[-1] in ('combine', 'list', 'prefix'):
        raise _error(f'Command `none` not allowed inside {ctxt.trace[-1]}', arguments.args)


def _check_choices(_ctxt, arguments):
    choices = arguments.get_required_arg('choices')
    _check_type(choices, (list, dict))
    arguments.require_no_more()

    if isinstance(choices.value, dict):
        for value, desc in choices.value.items():
            _check_type(value, (str, int))
            _check_type(desc,  (str, int))

    elif isinstance(choices.value, list):
        for value in choices.value:
            _check_type(value, (str, int))


def _check_command(_ctxt, arguments):
    opts = arguments.get_optional_arg({})
    _check_type(opts, (dict, ))
    arguments.require_no_more()

    _check_dictionary(opts, {
        'path':         (False, (str,), _check_non_empty_string),
        'path_append':  (False, (str,), _check_non_empty_string),
        'path_prepend': (False, (str,), _check_non_empty_string),
    })

    path = opts.value.get('path', None)
    append = opts.value.get('path_append', None)
    prepend = opts.value.get('path_prepend', None)

    if path and (append or prepend):
        raise _error('path_append/path_prepend cannot be used with path', opts)


def _check_command_arg(ctxt, arguments):
    arguments.require_no_more()

    if ctxt.trace and ctxt.trace[-1] in ('combine', 'list', 'key_value_list'):
        raise _error(f'Command `command_arg` not allowed inside {ctxt.trace[-1]}', arguments.args)

    if ctxt.type != Context.TYPE_POSITIONAL:
        raise _error('command_arg not allowed inside options', arguments.args)

    if (not _has_set(ctxt.positional, 'repeatable') or
        not ctxt.positional.value['repeatable'].value):
        raise _error('The `command_arg` completer requires `repeatable=True`', ctxt.positional)

    def command_is_previous_to_command_arg(positional):
        return (
            _has_set(positional, 'complete') and
            positional.value['complete'].value[0] == 'command' and
            positional.value['number'].value + 1 == ctxt.positional.value['number'].value
        )

    positionals = ctxt.definition.value['positionals'].value
    if not any(filter(command_is_previous_to_command_arg, positionals)):
        raise _error('The `command_arg` completer requires a previous `command` completer', ctxt.positional)


def _check_filedir(_ctxt, arguments, with_extensions=False, with_list_opts=False):
    options = arguments.get_optional_arg({})
    _check_type(options, (dict,))
    arguments.require_no_more()

    spec = {'directory': (False, (str,), _check_non_empty_string)}

    if with_extensions:
        spec['extensions'] = (False, (list,), None)
        spec['fuzzy'] = (False, (bool,), None)

    if with_list_opts:
        spec['separator'] = (False, (str,), _check_char)
        spec['duplicates'] = (False, (bool,), None)

    _check_dictionary(options, spec)

    if _has_set(options, 'directory'):
        if not options.value['directory'].value.startswith('/'):
            raise _error('directory must be an absolute path', options.value['directory'])

    if _has_set(options, 'extensions'):
        if len(options.value['extensions'].value) == 0:
            raise _error('extensions cannot not be empty', options.value['extensions'])

        for extension in options.value['extensions'].value:
            _check_type(extension, (str,), 'extension')

            if extension.value == '':
                raise _error('extension canonot not be empty', extension)

            if contains_space(extension.value):
                raise _error('extension contains space', extension)


def _check_file(ctxt, arguments):
    _check_filedir(ctxt, arguments, with_extensions=True)


def _check_directory(ctxt, arguments):
    _check_filedir(ctxt, arguments)


def _check_file_list(ctxt, arguments):
    if ctxt.trace and ctxt.trace[-1] in ('combine', 'list', 'key_value_list'):
        raise _error(f'Command `file_list` not allowed inside {ctxt.trace[-1]}', arguments.args)

    _check_filedir(ctxt, arguments, with_extensions=True, with_list_opts=True)


def _check_directory_list(ctxt, arguments):
    if ctxt.trace and ctxt.trace[-1] in ('combine', 'list', 'key_value_list'):
        raise _error(f'Command `directory_list` not allowed inside {ctxt.trace[-1]}', arguments.args)

    _check_filedir(ctxt, arguments, with_list_opts=True)


def _check_mime_file(_ctxt, arguments):
    pattern = arguments.get_required_arg("pattern")
    _check_type(pattern, (str,), "pattern")
    arguments.require_no_more()
    _check_regex(pattern, 'pattern')


def _check_range(_ctxt, arguments):
    start = arguments.get_required_arg("start")
    stop  = arguments.get_required_arg("stop")
    step  = arguments.get_optional_arg(1)
    arguments.require_no_more()

    _check_type(start, (int,), "start")
    _check_type(stop, (int,), "stop")
    _check_type(step, (int,), "step")

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


def _check_exec(_ctxt, arguments):
    command = arguments.get_required_arg("command")
    _check_type(command, (str,), "command")
    arguments.require_no_more()


def _check_value_list(_ctxt, arguments):
    options = arguments.get_required_arg('options')
    _check_type(options, (dict,), 'options')
    arguments.require_no_more()

    _check_dictionary(options, {
        'values':    (True,  (list, dict), None),
        'separator': (False, (str,), _check_char),
        'duplicates': (False, (bool,), None),
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


def _check_key_value_list(ctxt, arguments):
    pair_separator = arguments.get_required_arg('pair_separator')
    value_separator = arguments.get_required_arg('value_separator')
    values = arguments.get_required_arg('values')
    arguments.require_no_more()

    _check_type(pair_separator, (str,), 'pair_separator')
    _check_type(value_separator, (str,), 'value_separator')
    _check_type(values, (dict, list), 'values')

    if 'key_value_list' in ctxt.trace:
        raise _error('Nested `key_value_list` not allowed', arguments.arg)

    if 'list' in ctxt.trace:
        raise _error('Command `key_value_list` not allowed inside list', arguments.args)

    ctxt.trace.append('key_value_list')

    _check_char(pair_separator, 'pair_separator')
    _check_char(value_separator, 'value_separator')

    if len(values.value) == 0:
        raise _error('values: cannot be empty', values)

    if isinstance(values.value, dict):
        for key, complete in values.value.items():
            _check_type(key, (str,))
            _check_type(complete, (list, NoneType))

            _check_non_empty_string(key, 'key')
            _check_no_spaces(key, 'key')

            if complete.value is None:
                continue

            if len(complete.value) == 0:
                raise _error('Missing command', complete)

            _check_complete(ctxt, complete)
    else:
        for compldef in values.value:
            _check_type(compldef, (list,))

            if len(compldef.value) != 3:
                raise _error('Completion definition must have 3 fields', compldef)

        for compldef in values.value:
            key = compldef.value[0]
            description = compldef.value[1]
            complete = compldef.value[2]

            _check_type(key, (str,))
            _check_type(description, (str, NoneType))
            _check_type(complete, (list, NoneType))
            _check_non_empty_string(key, 'key')
            _check_no_spaces(key, 'key')

            if complete.value is None:
                continue

            if len(complete.value) == 0:
                raise _error('Missing command', complete)

            _check_complete(ctxt, complete)


def _check_combine(ctxt, arguments):
    commands = arguments.get_required_arg('commands')
    arguments.require_no_more()

    _check_type(commands, (list,))

    if 'combine' in ctxt.trace:
        raise _error('Nested `combine` not allowed', arguments.args)

    ctxt.trace.append('combine')

    for completer in commands.value:
        _check_type(completer, (list,))

        if len(completer.value) == 0:
            raise _error('Missing command', completer)

        _check_complete(ctxt, completer)

    if len(commands.value) == 0:
        raise _error('combine: Cannot be empty', commands)

    if len(commands.value) == 1:
        raise _error('combine: Must contain more than one command', commands)


def _check_list(ctxt, arguments):
    command = arguments.get_required_arg('command')
    options = arguments.get_optional_arg({})
    arguments.require_no_more()

    _check_type(command, (list,))
    _check_type(options, (dict,), 'options')

    _check_dictionary(options, {
        'separator': (False, (str,), _check_char),
        'duplicates': (False, (bool,), None),
    })

    if 'list' in ctxt.trace:
        raise _error('Nested `list` not allowed', arguments.args)

    if 'key_value_list' in ctxt.trace:
        raise _error('Command `list` not allowed inside key_value_list', arguments.args)

    if len(command.value) == 0:
        raise _error('Missing command', command)

    ctxt.trace.append('list')
    _check_complete(ctxt, command)


def _check_prefix(ctxt, arguments):
    prefix = arguments.get_required_arg('prefix')
    command = arguments.get_required_arg('command')
    arguments.require_no_more()

    _check_type(prefix, (str,), 'prefix')
    _check_type(options, (list,), 'command')

    if 'prefix' in ctxt.trace:
        raise _error('Nested `prefix` not allowed', arguments.args)

    if 'key_value_list' in ctxt.trace:
        raise _error('Command `prefix` not allowed inside key_value_list', arguments.args)

    if len(command.value) == 0:
        raise _error('Missing command', command)

    ctxt.trace.append('prefix')
    _check_complete(ctxt, command)


def _check_history(_ctxt, arguments):
    pattern = arguments.get_required_arg("pattern")
    _check_type(pattern, (str,), "pattern")
    arguments.require_no_more()
    _check_regex(pattern, 'pattern')


def _check_date(_ctxt, arguments):
    format_ = arguments.get_required_arg("format")
    _check_type(format_, (str,), "format")
    arguments.require_no_more()
    _check_non_empty_string(format_, 'format')


_COMMANDS = {
    'alsa_card':          _check_void,
    'alsa_device':        _check_void,
    'charset':            _check_void,
    'choices':            _check_choices,
    'combine':            _check_combine,
    'command':            _check_command,
    'command_arg':        _check_command_arg,
    'commandline_string': _check_void,
    'date':               _check_date,
    'date_format':        _check_void,
    'directory':          _check_directory,
    'directory_list':     _check_directory_list,
    'environment':        _check_void,
    'exec':               _check_exec,
    'exec_fast':          _check_exec,
    'exec_internal':      _check_exec,
    'file':               _check_file,
    'file_list':          _check_file_list,
    'filesystem_type':    _check_void,
    'float':              _check_void,
    'gid':                _check_void,
    'group':              _check_void,
    'history':            _check_history,
    'hostname':           _check_void,
    'integer':            _check_void,
    'key_value_list':     _check_key_value_list,
    'list':               _check_list,
    'locale':             _check_void,
    'login_shell':        _check_void,
    'mime_file':          _check_mime_file,
    'mountpoint':         _check_void,
    'net_interface':      _check_void,
    'none':               _check_none,
    'pid':                _check_void,
    'prefix':             _check_prefix,
    'process':            _check_void,
    'range':              _check_range,
    'service':            _check_void,
    'signal':             _check_void,
    'timezone':           _check_void,
    'uid':                _check_void,
    'user':               _check_void,
    'value_list':         _check_value_list,
    'variable':           _check_void,
}


def _check_complete(ctxt, args):
    arguments = Arguments(args)
    cmd = arguments.get_required_arg('command')

    if cmd.value not in _COMMANDS:
        raise _error(f'Invalid command: {cmd.value}', cmd)

    _COMMANDS[cmd.value](ctxt, arguments)


def _check_positionals_repeatable(definition_tree, definition):
    if not _has_set(definition, 'positionals'):
        return

    positionals = definition.value['positionals'].value
    repeatable_number = None

    for positional in sorted(positionals, key=lambda p: p.value['number'].value):
        repeatable = False
        if _has_set(positional, 'repeatable'):
            repeatable = positional.value['repeatable'].value

        positional_number = positional.value['number'].value

        if repeatable:
            if repeatable_number is not None and repeatable_number != positional_number:
                raise _error('Only one positional argument can be marked as repeatable', positional)
            else:
                repeatable_number = positional_number
        elif repeatable_number is not None and positional_number > repeatable_number:
            raise _error('A positional argument cannot follow a repeatable positional argument', positional)

    node = definition_tree.get_definition(definition.value['prog'].value)
    if repeatable_number is not None and len(node.subcommands) > 0:
        raise _error('Repeatable positionals and subcommands cannot be used together', definition)


def _check_option(ctxt, option):
    _check_dictionary(option, {
        'option_strings':       (True,  (list,),                None),
        'metavar':              (False, (str,  NoneType),       None),
        'help':                 (False, (str,  NoneType),       None),
        'optional_arg':         (False, (bool, NoneType),       None),
        'group':                (False, (str,  NoneType),       None),
        'groups':               (False, (list, NoneType),       None),
        'repeatable':           (False, (bool, str, NoneType),  None),
        'final':                (False, (bool, NoneType),       None),
        'hidden':               (False, (bool, NoneType),       None),
        'complete':             (False, (list, NoneType),       None),
        'when':                 (False, (str,  NoneType),       None),
        'capture':              (False, (str,  NoneType),       None),
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
        ctxt.type = Context.TYPE_OPTION
        ctxt.option = option
        ctxt.trace = []
        _check_complete(ctxt, option.value['complete'])

    if _has_set(option, 'when'):
        _check_when(option.value['when'])

    if _has_set(option, 'capture'):
        if not is_valid_variable_name(option.value['capture'].value):
            raise _error('Invalid variable name', option.value['capture'])


def _check_positional(ctxt, positional):
    _check_dictionary(positional, {
        'number':               (True,  (int,),            None),
        'metavar':              (False, (str,  NoneType),  None),
        'help':                 (False, (str,  NoneType),  None),
        'repeatable':           (False, (bool, NoneType),  None),
        'complete':             (False, (list, NoneType),  None),
        'when':                 (False, (str,  NoneType),  None),
        'capture':              (False, (str,  NoneType),  None),
    })

    if positional.value['number'].value < 1:
        raise _error('number cannot be zero or negative', positional.value['number'])

    if _has_set(positional, 'complete'):
        ctxt.type = Context.TYPE_POSITIONAL
        ctxt.positional = positional
        ctxt.trace = []
        _check_complete(ctxt, positional.value['complete'])

    if _has_set(positional, 'when'):
        _check_when(positional.value['when'])

    if _has_set(positional, 'capture'):
        if not is_valid_variable_name(positional.value['capture'].value):
            raise _error('Invalid variable name', positional.value['capture'])


def _check_definition(ctxt, definition):
    _check_dictionary(definition, {
        'prog':                 (True,  (str,),                None),
        'help':                 (False, (str,  NoneType),      None),
        'aliases':              (False, (list, NoneType),      None),
        'wraps':                (False, (str,  NoneType),      None),
        'abbreviate_commands':  (False, (bool, str, NoneType), None),
        'abbreviate_options':   (False, (bool, str, NoneType), None),
        'inherit_options':      (False, (bool, str, NoneType), None),
        'options':              (False, (list, NoneType),      None),
        'positionals':          (False, (list, NoneType),      None),
    })

    try:
        validate_prog(definition.value['prog'].value)
    except CrazyError as e:
        raise _error(f'prog: {e}', definition.value['prog']) from None

    if _has_set(definition, 'aliases'):
        for alias in definition.value['aliases'].value:
            _check_type(alias, (str,), 'alias')

            if contains_space(alias.value):
                raise _error('alias contains space', alias)

    if _has_set(definition, 'wraps'):
        if is_empty_or_whitespace(definition.value['wraps'].value):
            raise _error('wraps is empty', definition.value['wraps'])

        if contains_space(definition.value['wraps'].value):
            raise _error('wraps contains space', definition.value['wraps'])

        if contains_space(definition.value['prog'].value):
            raise _error('wraps not allowed in subcommands', definition.value['wraps'])

    if _has_set(definition, 'abbreviate_commands'):
        _check_extended_bool(definition.value['abbreviate_commands'])

    if _has_set(definition, 'abbreviate_options'):
        _check_extended_bool(definition.value['abbreviate_options'])

    if _has_set(definition, 'inherit_options'):
        _check_extended_bool(definition.value['inherit_options'])

    if _has_set(definition, 'options'):
        for option in definition.value['options'].value:
            _check_option(ctxt, option)

    if _has_set(definition, 'positionals'):
        for positional in definition.value['positionals'].value:
            _check_positional(ctxt, positional)


class DefinitionTree:
    def __init__(self, prog):
        self.prog = prog
        self.subcommands = {}

    def add_definition(self, definition):
        commands = definition.value['prog'].value.split(' ')
        subcommand = commands.pop(-1)

        node = self

        for i, part in enumerate(commands):
            try:
                node = node.subcommands[part]
            except KeyError:
                prog = ' '.join(commands[0:i+1])
                raise _error(f'Missing definition of program `{prog}`', definition) from None

        if subcommand in node.subcommands:
            prog = definition.value['prog'].value
            raise _error(f'Multiple definition of program `{prog}`', definition)

        node.subcommands[subcommand] = DefinitionTree(subcommand)

    def get_definition(self, prog):
        commands = prog.split(' ')
        node = self

        for part in commands:
            node = node.subcommands[part]

        return node

    @staticmethod
    def make_tree(definition_list):
        root = DefinitionTree('<root>')

        for definition in definition_list:
            root.add_definition(definition)

        return root


def validate(definition_list):
    '''Validate a list of definitions.'''

    context = Context()

    for definition in definition_list:
        context.definition = definition
        _check_definition(context, definition)

    tree = DefinitionTree.make_tree(definition_list)

    if len(tree.subcommands) == 0:
        raise _error('No programs defined', ValueWithTrace(None, '', 1, 1))

    if len(tree.subcommands) > 1:
        value = ValueWithTrace(None, '', 1, 1)
        progs = list(tree.subcommands.keys())
        raise _error('Too many main programs defined: %s' % progs, value)

    for definition in definition_list:
        _check_positionals_repeatable(tree, definition)
