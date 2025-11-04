'''Code for validating the structure of a command line definition.'''

from types import NoneType

from .cli import ExtendedBool, is_extended_bool
from .when import parse_when
from .errors import CrazyError, CrazySchemaValidationError
from .pattern import bash_glob_to_regex, bash_glob_to_zsh_glob
from .value_with_trace import ValueWithTrace
from .str_utils import (
    contains_space, is_empty_or_whitespace,
    is_valid_option_string, is_valid_variable_name,
    is_valid_extended_regex, validate_prog)
from . import messages as m


_error = CrazySchemaValidationError


# =============================================================================
# Helper functions for validating
# =============================================================================


class Context:
    '''Class for providing context to validation.'''

    # pylint: disable=too-few-public-methods

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

        raise _error('%s: %s' % (m.missing_arg(), name), self.args)

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
            raise _error(m.too_many_arguments(), self.args)


def _has_set(dictionary, key):
    return (key in dictionary.value and
            dictionary.value[key].value is not None)


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

        msg = m.invalid_type_expected_types(types_string)
        if parameter_name is not None:
            msg = f'{parameter_name}: {msg}'
        raise _error(msg, value)


def _check_dictionary(dictionary, rules):
    _check_type(dictionary, (dict,))

    for key, value in dictionary.value.items():
        if key.value not in rules:
            raise _error('%s: %s' % (m.unknown_parameter(), key.value), key)

        _check_type(value, rules[key.value][1], key.value)

        if rules[key.value][2]:
            rules[key.value][2](value, key.value)

    for key, rule in rules.items():
        if rule[0] is True and key not in dictionary.value:
            raise _error('%s: %s' % (m.missing_arg(), key),  dictionary)


def _check_regex(value, parameter):
    if not is_valid_extended_regex(value.value):
        raise _error('%s: %s' % (parameter, m.not_an_extended_regex()), value)


def _check_char(value, parameter):
    if len(value.value) != 1:
        raise _error('%s: %s' % (parameter, m.single_character_expected()), value)


def _check_variable_name(value, parameter):
    if not is_valid_variable_name(value.value):
        raise _error('%s: %s' % (parameter, m.not_a_variable_name()), value)


def _check_non_empty_string(value, parameter):
    if is_empty_or_whitespace(value.value):
        raise _error('%s: %s' % (parameter, m.string_cannot_be_empty()), value)


def _check_no_spaces(value, parameter):
    if contains_space(value.value):
        raise _error('%s: %s' % (parameter, m.string_cannot_contain_space()), value)


def _check_non_empty_list(value, parameter):
    if len(value.value) == 0:
        raise _error('%s: %s' % (parameter, m.list_cannot_be_empty()), value)


def _check_non_empty_dict(value, parameter):
    if len(value.value) == 0:
        raise _error('%s: %s' % (parameter, m.dict_cannot_be_empty()), value)


def _check_extended_bool(value, parameter):
    if not is_extended_bool(value.value):
        expected = 'true, false or `%s`' % ExtendedBool.INHERIT
        msg = '%s: %s' % (parameter, m.invalid_value_expected_values(expected))
        raise _error(msg, value)


# =============================================================================
# Actual validation code
# =============================================================================


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
        msg = m.completer_not_allowed_in('none', ctxt.trace[-1])
        raise _error(msg, arguments.args)


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

    if path and append:
        msg = m.mutually_exclusive_parameters('path, path_append')
        raise _error(msg, opts)

    if path and prepend:
        msg = m.mutually_exclusive_parameters('path, path_prepend')
        raise _error(msg, opts)


def _check_command_arg(ctxt, arguments):
    arguments.require_no_more()

    if ctxt.trace and ctxt.trace[-1] in ('combine', 'list', 'key_value_list'):
        msg = m.completer_not_allowed_in('command_arg', ctxt.trace[-1])
        raise _error(msg, arguments.args)

    if ctxt.type != Context.TYPE_POSITIONAL:
        msg = m.completer_not_allowed_in_option('command_arg')
        raise _error(msg, arguments.args)

    if (not _has_set(ctxt.positional, 'repeatable') or
        not ctxt.positional.value['repeatable'].value):
        msg = m.completer_requires_repeatable('command_arg')
        raise _error(msg, ctxt.positional)

    def command_is_previous_to_command_arg(positional):
        return (
            _has_set(positional, 'complete') and
            positional.value['complete'].value[0] == 'command' and
            positional.value['number'].value + 1 == ctxt.positional.value['number'].value
        )

    positionals = ctxt.definition.value['positionals'].value
    if not any(filter(command_is_previous_to_command_arg, positionals)):
        msg = m.command_arg_without_command()
        raise _error(msg, ctxt.positional)


def _check_filedir(_ctxt, arguments, with_file_opts=False, with_list_opts=False):
    options = arguments.get_optional_arg({})
    _check_type(options, (dict,))
    arguments.require_no_more()

    spec = {'directory': (False, (str,), _check_non_empty_string)}

    if with_file_opts:
        spec['extensions'] = (False, (list,), _check_non_empty_list)
        spec['fuzzy'] = (False, (bool,), None)
        spec['ignore_globs'] = (False, (list,), _check_non_empty_list)

    if with_list_opts:
        spec['separator'] = (False, (str,), _check_char)
        spec['duplicates'] = (False, (bool,), None)

    _check_dictionary(options, spec)

    if _has_set(options, 'extensions'):
        for extension in options.value['extensions'].value:
            _check_type(extension, (str,), 'extension')
            _check_non_empty_string(extension, 'extension')
            _check_no_spaces(extension, 'extension')

    if _has_set(options, 'ignore_globs'):
        for pattern in options.value['ignore_globs'].value:
            _check_type(pattern, (str,), 'pattern')
            _check_non_empty_string(pattern, 'pattern')
            try:
                bash_glob_to_regex(pattern.value)
                bash_glob_to_zsh_glob(pattern.value)
            except ValueError as e:
                raise _error('%s: %s' % ('pattern', e), pattern) from e


def _check_file(ctxt, arguments):
    _check_filedir(ctxt, arguments, with_file_opts=True)


def _check_directory(ctxt, arguments):
    _check_filedir(ctxt, arguments)


def _check_file_list(ctxt, arguments):
    _check_filedir(ctxt, arguments, with_file_opts=True, with_list_opts=True)


def _check_directory_list(ctxt, arguments):
    _check_filedir(ctxt, arguments, with_list_opts=True)


def _check_mime_file(_ctxt, arguments):
    pattern = arguments.get_required_arg("pattern")
    _check_type(pattern, (str,), "pattern")
    arguments.require_no_more()
    _check_regex(pattern, 'pattern')


def _check_range(_ctxt, arguments):
    start = arguments.get_required_arg("start")
    stop = arguments.get_required_arg("stop")
    step = arguments.get_optional_arg(1)
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
        msg = '%s: %s' % ('step', m.integer_cannot_be_zero())
        raise _error(msg, step)


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

    if isinstance(values.value, dict):
        _check_non_empty_dict(values, 'values')

        for item, desc in values.value.items():
            _check_type(item, (str,))
            _check_type(desc, (str,))
    else:
        _check_non_empty_list(values, 'values')

        for value in values.value:
            _check_type(value, (str,))


def _check_key_value_list(ctxt, arguments):
    pair_separator = arguments.get_required_arg('pair_separator')
    value_separator = arguments.get_required_arg('value_separator')
    values = arguments.get_required_arg('values')
    arguments.require_no_more()

    _check_type(pair_separator, (str,), 'pair_separator')
    _check_type(value_separator, (str,), 'value_separator')
    _check_type(values, (list,), 'values')

    ctxt.trace.append('key_value_list')

    _check_char(pair_separator, 'pair_separator')
    _check_char(value_separator, 'value_separator')
    _check_non_empty_list(values, 'values')

    for compldef in values.value:
        _check_type(compldef, (list,))

        if len(compldef.value) != 3:
            msg = m.list_must_contain_exact_three_items()
            raise _error(msg, compldef)

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

        _check_complete(ctxt, complete)


def _check_combine(ctxt, arguments):
    commands = arguments.get_required_arg('commands')
    arguments.require_no_more()

    _check_type(commands, (list,))
    _check_non_empty_list(commands, 'commands')

    if len(commands.value) == 1:
        msg = m.list_must_contain_at_least_two_items()
        raise _error(msg, commands)

    ctxt.trace.append('combine')

    for completer in commands.value:
        _check_type(completer, (list,))
        _check_complete(ctxt, completer)


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

    ctxt.trace.append('list')
    _check_complete(ctxt, command)


def _check_prefix(ctxt, arguments):
    prefix = arguments.get_required_arg('prefix')
    command = arguments.get_required_arg('command')
    arguments.require_no_more()

    _check_type(prefix, (str,), 'prefix')
    _check_type(command, (list,), 'command')

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


def _check_ip_address(_ctxt, arguments):
    type_ = arguments.get_optional_arg('all')
    arguments.require_no_more()
    _check_type(type_, (str,), "type")

    if type_.value not in ('ipv4', 'ipv6', 'all'):
        msg = '%s: %s' % ('type', m.invalid_value_expected_values('ipv4, ipv6, all'))
        raise _error(msg, type_)


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
    'ip_address':         _check_ip_address,
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

    _check_type(cmd, (str,), 'command')

    if cmd.value not in _COMMANDS:
        msg = '%s: %s' % (m.unknown_completer(), cmd.value)
        raise _error(msg, cmd)

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
                msg = m.too_many_repeatable_positionals()
                raise _error(msg, positional)

            repeatable_number = positional_number
        elif repeatable_number is not None and positional_number > repeatable_number:
            msg = m.positional_argument_after_repeatable()
            raise _error(msg, positional)

    node = definition_tree.get_definition(definition.value['prog'].value)
    if repeatable_number is not None and len(node.subcommands) > 0:
        msg = m.repeatable_with_subcommands()
        raise _error(msg, definition)


def _check_option(ctxt, option):
    chkbool = _check_extended_bool

    _check_dictionary(option, {
        'option_strings':       (True,  (list,),                None),
        'metavar':              (False, (str,  NoneType),       None),
        'help':                 (False, (str,  NoneType),       None),
        'optional_arg':         (False, (bool, NoneType),       None),
        'group':                (False, (str,  NoneType),       None),
        'groups':               (False, (list, NoneType),       None),
        'repeatable':           (False, (bool, str, NoneType),  chkbool),
        'final':                (False, (bool, NoneType),       None),
        'hidden':               (False, (bool, NoneType),       None),
        'nosort':               (False, (bool, NoneType),       None),
        'complete':             (False, (list, NoneType),       None),
        'when':                 (False, (str,  NoneType),       None),
        'capture':              (False, (str,  NoneType),       None),
    })

    option_strings = option.value['option_strings']

    _check_non_empty_list(option_strings, 'option_strings')

    for option_string in option_strings.value:
        _check_type(option_string, (str,), "option_string")

        if not is_valid_option_string(option_string.value):
            msg = m.invalid_value()
            raise _error(msg, option_string)

    if _has_set(option, 'metavar') and not _has_set(option, 'complete'):
        msg = m.parameter_requires_parameter('metavar', 'complete')
        raise _error(msg, option)

    if _has_set(option, 'optional_arg') and not _has_set(option, 'complete'):
        msg = m.parameter_requires_parameter('optional_arg', 'complete')
        raise _error(msg, option)

    if _has_set(option, 'group') and _has_set(option, 'groups'):
        msg = m.mutually_exclusive_parameters('groups, group')
        raise _error(msg, option)

    if _has_set(option, 'groups'):
        for group in option.value['groups'].value:
            _check_type(group, (str,), "group")

    if _has_set(option, 'complete'):
        ctxt.type = Context.TYPE_OPTION
        ctxt.option = option
        ctxt.trace = []
        _check_complete(ctxt, option.value['complete'])

    if _has_set(option, 'when'):
        _check_when(option.value['when'])

    if _has_set(option, 'capture'):
        _check_variable_name(option.value['capture'], 'capture')


def _check_positional(ctxt, positional):
    _check_dictionary(positional, {
        'number':               (True,  (int,),            None),
        'metavar':              (False, (str,  NoneType),  None),
        'help':                 (False, (str,  NoneType),  None),
        'repeatable':           (False, (bool, NoneType),  None),
        'nosort':               (False, (bool, NoneType),  None),
        'complete':             (False, (list, NoneType),  None),
        'when':                 (False, (str,  NoneType),  None),
        'capture':              (False, (str,  NoneType),  None),
    })

    if positional.value['number'].value < 1:
        msg = m.integer_must_be_greater_than_zero()
        raise _error('%s: %s' % ('number', msg), positional.value['number'])

    if _has_set(positional, 'complete'):
        ctxt.type = Context.TYPE_POSITIONAL
        ctxt.positional = positional
        ctxt.trace = []
        _check_complete(ctxt, positional.value['complete'])

    if _has_set(positional, 'when'):
        _check_when(positional.value['when'])

    if _has_set(positional, 'capture'):
        _check_variable_name(positional.value['capture'], 'capture')


def _check_definition(ctxt, definition):
    chkbool = _check_extended_bool

    _check_dictionary(definition, {
        'prog':                 (True,  (str,),                None),
        'help':                 (False, (str,  NoneType),      None),
        'aliases':              (False, (list, NoneType),      None),
        'wraps':                (False, (str,  NoneType),      None),
        'abbreviate_commands':  (False, (bool, str, NoneType), chkbool),
        'abbreviate_options':   (False, (bool, str, NoneType), chkbool),
        'inherit_options':      (False, (bool, str, NoneType), chkbool),
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
            _check_non_empty_string(alias, 'alias')
            _check_no_spaces(alias, 'alias')

    if _has_set(definition, 'wraps'):
        wraps = definition.value['wraps']
        _check_non_empty_string(wraps, 'wraps')
        _check_no_spaces(wraps, 'wraps')

        if contains_space(definition.value['prog'].value):
            msg = m.parameter_not_allowed_in_subcommand('wraps')
            raise _error(msg, definition.value['wraps'])

    if _has_set(definition, 'options'):
        for option in definition.value['options'].value:
            _check_option(ctxt, option)

    if _has_set(definition, 'positionals'):
        for positional in definition.value['positionals'].value:
            _check_positional(ctxt, positional)


class _DefinitionTree:
    def __init__(self, prog):
        self.prog = prog
        self.subcommands = {}

    def add_definition(self, definition):
        '''Add a definition to the tree.'''

        commands = definition.value['prog'].value.split(' ')
        subcommand = commands.pop(-1)

        node = self

        for i, part in enumerate(commands):
            try:
                node = node.subcommands[part]
            except KeyError:
                prog = ' '.join(commands[0:i+1])
                msg = m.missing_definition_of_program(prog)
                raise _error(msg, definition) from None

        if subcommand in node.subcommands:
            prog = definition.value['prog'].value
            msg = m.multiple_definition_of_program(prog)
            raise _error(msg, definition)

        node.subcommands[subcommand] = _DefinitionTree(subcommand)

    def get_definition(self, prog):
        '''Get definition by prog.'''

        commands = prog.split(' ')
        node = self

        for part in commands:
            node = node.subcommands[part]

        return node

    @staticmethod
    def make_tree(definition_list):
        '''Make a tree out of a list of definitions.'''

        root = _DefinitionTree('<root>')

        for definition in definition_list:
            root.add_definition(definition)

        return root


def validate(definition_list):
    '''Validate a list of definitions.'''

    context = Context()

    for definition in definition_list:
        context.definition = definition
        _check_definition(context, definition)

    tree = _DefinitionTree.make_tree(definition_list)

    if len(tree.subcommands) == 0:
        msg = m.no_programs_defined()
        raise _error(msg, ValueWithTrace(None, '', 1, 1))

    if len(tree.subcommands) > 1:
        value = ValueWithTrace(None, '', 1, 1)
        progs = list(tree.subcommands.keys())
        msg = m.too_many_programs_defined()
        raise _error('%s: %s' % (msg, progs), value)

    for definition in definition_list:
        _check_positionals_repeatable(tree, definition)
