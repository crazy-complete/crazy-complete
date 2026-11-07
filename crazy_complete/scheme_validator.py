# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2025-2026 Benjamin Abendroth <braph93@gmx.de>

'''Code for validating the structure of a command line definition.'''

from types import NoneType

from .cli import INHERIT, is_extended_bool
from .when import parse_when
from .errors import CrazyError, CrazySchemaValidationError
from .value_with_trace import ValueWithTrace
from .str_utils import (
    contains_space, is_empty_or_whitespace,
    is_valid_option_string, is_valid_variable_name,
    is_valid_extended_regex, validate_prog)
from . import completers
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


def has_set(dictionary, key):
    return (key in dictionary.value and
            dictionary.value[key].value is not None)


def _is_true(dictionary, key):
    return (key in dictionary.value and
            dictionary.value[key].value is True)


def check_type(value, types, parameter_name=None):
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


def check_dictionary(dictionary, rules):
    check_type(dictionary, (dict,))

    for key, value in dictionary.value.items():
        if key.value not in rules:
            raise _error('%s: %s' % (m.unknown_parameter(), key.value), key)

        check_type(value, rules[key.value][1], key.value)

        if rules[key.value][2]:
            rules[key.value][2](value, key.value)

    for key, rule in rules.items():
        if rule[0] is True and key not in dictionary.value:
            raise _error('%s: %s' % (m.missing_arg(), key), dictionary)


def check_regex(value, parameter):
    if not is_valid_extended_regex(value.value):
        raise _error('%s: %s' % (parameter, m.not_an_extended_regex()), value)


def check_char(value, parameter):
    if len(value.value) != 1:
        msg = '%s: %s' % (parameter, m.single_character_expected())
        raise _error(msg, value)

def _check_variable_name(value, parameter):
    if not is_valid_variable_name(value.value):
        raise _error('%s: %s' % (parameter, m.not_a_variable_name()), value)

def check_non_empty_string(value, parameter):
    if is_empty_or_whitespace(value.value):
        raise _error('%s: %s' % (parameter, m.string_cannot_be_empty()), value)


def check_no_spaces(value, parameter):
    if contains_space(value.value):
        msg = '%s: %s' % (parameter, m.string_cannot_contain_space())
        raise _error(msg, value)


def check_non_empty_list(value, parameter):
    if len(value.value) == 0:
        raise _error('%s: %s' % (parameter, m.list_cannot_be_empty()), value)


def check_non_empty_dict(value, parameter):
    if len(value.value) == 0:
        raise _error('%s: %s' % (parameter, m.dict_cannot_be_empty()), value)


def _check_extended_bool(value, parameter):
    if not is_extended_bool(value.value):
        expected = 'true, false or `%s`' % INHERIT
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



def _check_directory(ctxt, arguments):
    check_filedir(ctxt, arguments)


def _load_plugin_checker(name):
    '''Try to load the `validate` function of a completer plugin.

    Returns:
        The `validate` function, or `None` if no such plugin exists.
    '''

    try:
        module = completers.load(name)
    except ImportError:
        return None

    func = getattr(module, 'validate', None)

    if not callable(func):
        return None

    return func


def check_complete(ctxt, args):
    arguments = Arguments(args)
    cmd = arguments.get_required_arg('command')

    check_type(cmd, (str,), 'command')

    checker = _load_plugin_checker(cmd.value)

    if checker is None:
        msg = '%s: %s' % (m.unknown_completer(), cmd.value)
        raise _error(msg, cmd)

    try:
        checker(ctxt, arguments)
    except _error as e:
        msg = '%s: %s' % (cmd.value, e.message)
        raise _error(msg, e.value_with_trace) from e


def _check_positionals_repeatable0(definition_tree, definition):
    if not has_set(definition, 'positionals'):
        return

    positionals = definition.value['positionals'].value
    repeatable_number = None

    for positional in sorted(positionals, key=lambda p: p.value['number'].value):
        repeatable = False
        if has_set(positional, 'repeatable'):
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


def _check_positionals_repeatable(definition_tree, definition):
    try:
        _check_positionals_repeatable0(definition_tree, definition)
    except _error as e:
        prog = definition.value['prog'].value
        msg = '%s: %s' % (prog, e.message)
        raise _error(msg, e.value_with_trace) from e


def _check_option0(ctxt, option):
    chkbool = _check_extended_bool

    check_dictionary(option, {
        'option_strings': (True,  (list,),               None),
        'metavar':        (False, (str,  NoneType),      None),
        'help':           (False, (str,  NoneType),      None),
        'optional_arg':   (False, (bool, NoneType),      None),
        'group':          (False, (str,  NoneType),      None),
        'groups':         (False, (list, NoneType),      None),
        'repeatable':     (False, (bool, str, NoneType), chkbool),
        'final':          (False, (bool, NoneType),      None),
        'hidden':         (False, (bool, NoneType),      None),
        'nosort':         (False, (bool, NoneType),      None),
        'complete':       (False, (list, NoneType),      None),
        'when':           (False, (str,  NoneType),      None),
        'capture':        (False, (str,  NoneType),      None),
        'long_opt_arg_sep': (False, (str,),              None),
    })

    option_strings = option.value['option_strings']

    check_non_empty_list(option_strings, 'option_strings')

    for option_string in option_strings.value:
        check_type(option_string, (str,), "option_string")

        if not is_valid_option_string(option_string.value):
            msg = m.invalid_value()
            raise _error(msg, option_string)

    if has_set(option, 'metavar') and not has_set(option, 'complete'):
        msg = m.parameter_requires_parameter('metavar', 'complete')
        raise _error(msg, option)

    if _is_true(option, 'optional_arg') and not has_set(option, 'complete'):
        msg = m.parameter_requires_parameter('optional_arg', 'complete')
        raise _error(msg, option)

    if _is_true(option, 'repeatable') and _is_true(option, 'hidden'):
        msg = m.mutually_exclusive_parameters('repeatable, hidden')
        raise _error(msg, option)

    if has_set(option, 'group') and has_set(option, 'groups'):
        msg = m.mutually_exclusive_parameters('groups, group')
        raise _error(msg, option)

    if has_set(option, 'groups'):
        for group in option.value['groups'].value:
            check_type(group, (str,), "group")

    if has_set(option, 'complete'):
        ctxt.type = Context.TYPE_OPTION
        ctxt.option = option
        ctxt.trace = []
        check_complete(ctxt, option.value['complete'])

    if has_set(option, 'when'):
        _check_when(option.value['when'])

    if has_set(option, 'capture'):
        _check_variable_name(option.value['capture'], 'capture')

    if has_set(option, 'long_opt_arg_sep'):
        if option.value['long_opt_arg_sep'] not in (
                'space', 'equals', 'both', INHERIT):
            expected = f'space, equals, both, {INHERIT}'
            msg = m.invalid_value_expected_values(expected)
            raise _error(msg, option.value['long_opt_arg_sep'])


def _check_option(ctxt, option):
    try:
        _check_option0(ctxt, option)
    except _error as e:
        try:
            option_strings = option.value['option_strings'].value
            option_strings = '|'.join([o.value for o in option_strings])
        except (KeyError, TypeError):
            raise e from None

        msg = '%s: %s' % (option_strings, e.message)
        raise _error(msg, e.value_with_trace) from e


def _check_positional0(ctxt, positional):
    check_dictionary(positional, {
        'number':     (True,  (int,),           None),
        'metavar':    (False, (str,  NoneType), None),
        'help':       (False, (str,  NoneType), None),
        'repeatable': (False, (bool, NoneType), None),
        'nosort':     (False, (bool, NoneType), None),
        'complete':   (False, (list, NoneType), None),
        'when':       (False, (str,  NoneType), None),
        'capture':    (False, (str,  NoneType), None),
    })

    if positional.value['number'].value < 1:
        msg = m.integer_must_be_greater_than_zero()
        raise _error('%s: %s' % ('number', msg), positional.value['number'])

    if has_set(positional, 'complete'):
        ctxt.type = Context.TYPE_POSITIONAL
        ctxt.positional = positional
        ctxt.trace = []
        check_complete(ctxt, positional.value['complete'])

    if has_set(positional, 'when'):
        _check_when(positional.value['when'])

    if has_set(positional, 'capture'):
        _check_variable_name(positional.value['capture'], 'capture')


def _check_positional(ctxt, positional):
    try:
        _check_positional0(ctxt, positional)
    except _error as e:
        metavar = 'unknown'

        try:
            metavar = 'positional #%d' % positional.value['number'].value
        except (KeyError, TypeError):
            pass

        try:
            metavar_ = positional.value['metavar'].value
            assert isinstance(metavar_, str)
            metavar = metavar_
        except (AssertionError, KeyError):
            pass

        msg = '%s: %s' % (metavar, e.message)
        raise _error(msg, e.value_with_trace) from e


def _check_commandline_definition0(ctxt, definition):
    chkbool = _check_extended_bool

    check_dictionary(definition, {
        'prog':                (True,  (str,),                None),
        'help':                (False, (str,  NoneType),      None),
        'aliases':             (False, (list, NoneType),      None),
        'wraps':               (False, (str,  NoneType),      None),
        'abbreviate_commands': (False, (bool, str, NoneType), chkbool),
        'abbreviate_options':  (False, (bool, str, NoneType), chkbool),
        'inherit_options':     (False, (bool, str, NoneType), chkbool),
        'options':             (False, (list, NoneType),      None),
        'positionals':         (False, (list, NoneType),      None),
    })

    try:
        validate_prog(definition.value['prog'].value)
    except CrazyError as e:
        raise _error(f'prog: {e}', definition.value['prog']) from None

    if has_set(definition, 'aliases'):
        for alias in definition.value['aliases'].value:
            check_type(alias, (str,), 'alias')
            check_non_empty_string(alias, 'alias')
            check_no_spaces(alias, 'alias')

    if has_set(definition, 'wraps'):
        wraps = definition.value['wraps']
        check_non_empty_string(wraps, 'wraps')
        check_no_spaces(wraps, 'wraps')

        if contains_space(definition.value['prog'].value):
            msg = m.parameter_not_allowed_in_subcommand('wraps')
            raise _error(msg, definition.value['wraps'])

    if has_set(definition, 'options'):
        for option in definition.value['options'].value:
            _check_option(ctxt, option)

    if has_set(definition, 'positionals'):
        for positional in definition.value['positionals'].value:
            _check_positional(ctxt, positional)


def _check_commandline_definition(ctxt, definition):
    try:
        _check_commandline_definition0(ctxt, definition)
    except _error as e:
        try:
            prog = definition.value['prog'].value
        except (KeyError, TypeError):
            prog = 'unknown'

        msg = '%s: %s' % (prog, e.message)
        raise _error(msg, e.value_with_trace) from e


class DefinitionTree:
    '''Holds a command-line definition with subcommands.'''

    def __init__(self, definition):
        self.definition = definition
        self.subcommands = {}

    def add_definition(self, definition):
        '''Add a definition to subcommands.'''

        check_type(definition, (dict,))

        if not has_set(definition, 'prog'):
            raise _error('%s: %s' % (m.missing_arg(), 'prog'), definition)

        try:
            validate_prog(definition.value['prog'].value)
        except CrazyError as e:
            raise _error(f'prog: {e}', definition.value['prog']) from None

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

        node.subcommands[subcommand] = DefinitionTree(definition)

    def get_definition(self, prog):
        '''Get definition by prog.'''

        commands = prog.split(' ')
        node = self

        for part in commands:
            node = node.subcommands[part]

        return node

    def visit(self, callback):
        '''Call `callback` on each node in the tree.'''
        callback(self)
        for subcommand in self.subcommands.values():
            callback(subcommand)

    def get_all(self):
        '''Return a list of all nodes.'''
        result = []
        self.visit(result.append)
        return result

    def get_first_commandline(self):
        '''Return the first command line in the tree.'''
        return list(self.subcommands.values())[0]

    @staticmethod
    def make_tree(definition_list):
        '''Make a tree out of a list of definitions.'''

        root = DefinitionTree(None)

        for definition in definition_list:
            root.add_definition(definition)

        return root


def validate(definition_list):
    '''Validate a list of definitions.'''

    context = Context()
    commandline_root = DefinitionTree.make_tree(definition_list)

    if len(commandline_root.subcommands) == 0:
        msg = m.no_programs_defined()
        raise _error(msg, ValueWithTrace(None, '', 1, 1))

    if len(commandline_root.subcommands) > 1:
        value = ValueWithTrace(None, '', 1, 1)
        progs = list(commandline_root.subcommands.keys())
        msg = m.too_many_programs_defined()
        raise _error('%s: %s' % (msg, progs), value)

    for cmdline in commandline_root.get_first_commandline().get_all():
        context.definition = cmdline.definition
        _check_commandline_definition(context, cmdline.definition)
        _check_positionals_repeatable(commandline_root, cmdline.definition)
