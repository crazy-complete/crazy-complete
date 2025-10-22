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

    OPTION = 0
    POSITIONAL = 1

    def __init__(self):
        self.defintion = None
        self.type = None


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


def _check_void(ctxt, arguments):
    arguments.require_no_more()


def _check_choices(ctxt, arguments):
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


def _check_command(ctxt, arguments):
    opts = arguments.get_optional_arg({})
    _check_type(opts, (dict, ))
    arguments.require_no_more()

    _check_dictionary(opts, {
        'path':         (False, (str,)),
        'path_append':  (False, (str,)),
        'path_prepend': (False, (str,)),
    })

    path = None
    append = None
    prepend = None

    if _has_set(opts, 'path'):
        path = opts.value['path']
        if is_empty_or_whitespace(path.value):
            raise _error('path cannot be empty', path)

    if _has_set(opts, 'path_append'):
        path_append = opts.value['path_append']
        if is_empty_or_whitespace(path_append.value):
            raise _error('path_append cannot be empty', path_append)

    if _has_set(opts, 'path_prepend'):
        path_prepend = opts.value['path_prepend']
        if is_empty_or_whitespace(path_prepend.value):
            raise _error('path_prepend cannot be empty', path_prepend)

    if path and (append or prepend):
        raise _error('path_append/path_prepend cannot be used with path', opts)


def _check_filedir(ctxt, arguments, with_extensions=False, with_separator=False):
    options = arguments.get_optional_arg({})
    _check_type(options, (dict,))
    arguments.require_no_more()

    spec = {'directory': (False, (str,))}

    if with_extensions:
        spec['extensions'] = (False, (list,))
        spec['fuzzy'] = (False, (bool,))

    if with_separator:
        spec['separator'] = (False, (str,))
        spec['duplicates'] = (False, (bool,))

    _check_dictionary(options, spec)

    if _has_set(options, 'directory'):
        if options.value['directory'].value == '':
            raise _error('directory cannot not be empty', options.value['directory'])

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

    if _has_set(options, 'separator'):
        separator = options.value['separator']

        if len(separator.value) != 1:
            raise _error('Invalid length for separator', separator)


def _check_file(ctxt, arguments):
    _check_filedir(ctxt, arguments, with_extensions=True)


def _check_directory(ctxt, arguments):
    _check_filedir(ctxt, arguments)


def _check_file_list(ctxt, arguments):
    _check_filedir(ctxt, arguments, with_extensions=True, with_separator=True)


def _check_directory_list(ctxt, arguments):
    _check_filedir(ctxt, arguments, with_separator=True)


def _check_mime_file(ctxt, arguments):
    pattern = arguments.get_required_arg("pattern")
    _check_type(pattern, (str,), "pattern")
    arguments.require_no_more()

    if not is_valid_extended_regex(pattern.value):
        raise _error('Pattern: Not a valid extended regex', pattern)


def _check_range(ctxt, arguments):
    start = arguments.get_required_arg("start")
    _check_type(start, (int,), "start")

    stop  = arguments.get_required_arg("stop")
    _check_type(stop,  (int,), "stop")

    step  = arguments.get_optional_arg(1)
    _check_type(step,  (int,), "step")

    arguments.require_no_more()

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


def _check_exec(ctxt, arguments):
    command = arguments.get_required_arg("command")
    _check_type(command, (str,), "command")
    arguments.require_no_more()


def _check_value_list(ctxt, arguments):
    options = arguments.get_required_arg('options')
    _check_type(options, (dict,), 'options')
    arguments.require_no_more()

    _check_dictionary(options, {
        'values':    (True,  (list, dict)),
        'separator': (False, (str,)),
        'duplicates': (False, (bool,)),
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


def _check_combine(ctxt, arguments):
    commands = arguments.get_required_arg('commands')
    arguments.require_no_more()

    _check_type(commands, (list,))

    for subcommand_args in commands.value:
        _check_type(subcommand_args, (list,))

        if len(subcommand_args.value) == 0:
            raise _error('Missing command', subcommand_args)

        if subcommand_args.value[0] == 'combine':
            raise _error('Nested `combine` not allowed', subcommand_args)

        if subcommand_args.value[0] == 'none':
            raise _error('Command `none` not allowed inside combine', subcommand_args)

        if subcommand_args.value[0] == 'command_arg':
            raise _error('Command `command_arg` not allowed inside combine', subcommand_args)

        if subcommand_args.value[0] == 'list':
            raise _error('Command `list` not allowed inside combine', subcommand_args)

        _check_complete(ctxt, subcommand_args)

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
        'separator': (False, (str,)),
        'duplicates': (False, (bool,)),
    })

    if len(command.value) == 0:
        raise _error('Missing command', command)

    if command.value[0] == 'list':
        raise _error('Nested `list` not allowed', command)

    if command.value[0] == 'none':
        raise _error('Command `none` not allowed inside list', command)

    if command.value[0] == 'command_arg':
        raise _error('Command `command_arg` not allowed inside list', command)

    if command.value[0] == 'file':
        raise _error('Command `file` not allowed inside list. Use `file_list` instead', command)

    if command.value[0] == 'directory':
        raise _error('Command `directory` not allowed inside list. Use `directory_list` instead', command)

    if _has_set(options, 'separator'):
        separator = options.value['separator']

        if len(separator.value) != 1:
            raise _error('Invalid length for separator', separator)

    _check_complete(ctxt, command)


def _check_history(ctxt, arguments):
    pattern = arguments.get_required_arg("pattern")
    _check_type(pattern, (str,), "pattern")
    arguments.require_no_more()

    if not is_valid_extended_regex(pattern.value):
        raise _error('Pattern: Not a valid extended regex', pattern)


def _check_date(ctxt, arguments):
    format_ = arguments.get_required_arg("format")
    _check_type(format_, (str,), "format")
    arguments.require_no_more()

    if is_empty_or_whitespace(format_.value):
        raise _error('format cannot be empty', format_)


def _check_complete(ctxt, args):
    arguments = Arguments(args)
    cmd = arguments.get_required_arg('command')

    if cmd.value == 'command_arg' and ctxt.type == Context.OPTION:
        raise _error('command_arg not allowed inside options', cmd)

    commands = {
        'none':             _check_void,
        'integer':          _check_void,
        'float':            _check_void,
        'command':          _check_command,
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
        'directory':        _check_directory,
        'mime_file':        _check_mime_file,
        'range':            _check_range,
        'exec':             _check_exec,
        'exec_fast':        _check_exec,
        'exec_internal':    _check_exec,
        'value_list':       _check_value_list,
        'combine':          _check_combine,
        'list':             _check_list,
        'history':          _check_history,
        'commandline_string': _check_void,
        'command_arg':      _check_void,
        'date':             _check_date,
        'date_format':      _check_void,
        'file_list':        _check_file_list,
        'directory_list':   _check_directory_list,
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

    commands[cmd.value](ctxt, arguments)


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


def _check_positionals_command_arg(definition):
    '''Check for the right usage of `command_arg`.'''

    if not _has_set(definition, 'positionals'):
        return

    positionals = definition.value['positionals'].value
    command_position = None

    for positional in sorted(positionals, key=lambda p: p.value['number'].value):
        complete = ['none']
        if _has_set(positional, 'complete'):
            complete = positional.value['complete'].value

        repeatable = False
        if _has_set(positional, 'repeatable'):
            repeatable = positional.value['repeatable'].value

        positional_number = positional.value['number'].value

        if complete[0] == 'command':
            command_position = positional_number

        elif complete[0] == 'command_arg':
            if not repeatable:
                raise _error('The `command_arg` completer requires `repeatable=True`', positional)

            if command_position is None or command_position + 1 != positional_number:
                raise _error('The `command_arg` completer requires a previous `command` completer', positional)


def _check_option(ctxt, option):
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
        _check_complete(ctxt, option.value['complete'])

    if _has_set(option, 'when'):
        _check_when(option.value['when'])

    if _has_set(option, 'capture'):
        if not is_valid_variable_name(option.value['capture'].value):
            raise _error('Invalid variable name', option.value['capture'])


def _check_positional(ctxt, positional):
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
        _check_complete(ctxt, positional.value['complete'])

    if _has_set(positional, 'when'):
        _check_when(positional.value['when'])

    if _has_set(positional, 'capture'):
        if not is_valid_variable_name(positional.value['capture'].value):
            raise _error('Invalid variable name', positional.value['capture'])


def _check_definition(ctxt, definition):
    _check_dictionary(definition, {
        'prog':                 (True,  (str,)),
        'help':                 (False, (str,  NoneType)),
        'aliases':              (False, (list, NoneType)),
        'wraps':                (False, (str,  NoneType)),
        'abbreviate_commands':  (False, (bool, str, NoneType)),
        'abbreviate_options':   (False, (bool, str, NoneType)),
        'inherit_options':      (False, (bool, str, NoneType)),
        'options':              (False, (list, NoneType)),
        'positionals':          (False, (list, NoneType)),
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
        ctxt.type = Context.OPTION

        for option in definition.value['options'].value:
            _check_option(ctxt, option)

    if _has_set(definition, 'positionals'):
        ctxt.type = Context.POSITIONAL

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
        _check_positionals_command_arg(definition)
