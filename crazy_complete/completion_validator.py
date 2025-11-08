'''This module contains code for validating completing definitions.'''

# Unlike the `scheme_validator`, this validator operates directly on Python
# objects and therefore does not have access to line and column information.
# To save code and maintain consistency, we reuse the validation logic
# from `scheme_validator` by wrapping the objects in `ValueWithoutTrace`.
# This provides the same structure as used in `scheme_validator`, except that
# we use `ValueWithoutTrace` instead of `ValueWithTrace`.

from types import NoneType

from . import scheme_validator
from .value_with_trace import ValueWithOutTrace


def _mk_value_without_trace(value):
    if isinstance(value, ValueWithOutTrace):
        return value

    if isinstance(value, (NoneType, str, int, float, bool)):
        return ValueWithOutTrace(value)

    mk = _mk_value_without_trace

    if isinstance(value, (list, tuple)):
        return ValueWithOutTrace(list(map(mk, value)))

    if isinstance(value, dict):
        return ValueWithOutTrace({mk(k): mk(v) for k, v in value.items()})

    raise AssertionError(f"Not reached: {value!r}")


def _option_to_definition(option):
    return {
        'option_strings': option.option_strings,
        'metavar':        option.metavar,
        'help':           option.help,
        'complete':       option.complete,
        'nosort':         option.nosort,
        'groups':         option.groups,
        'optional_arg':   option.optional_arg,
        'repeatable':     option.repeatable,
        'final':          option.final,
        'hidden':         option.hidden,
        'when':           option.when,
        'capture':        option.capture,
    }


def _positional_to_definition(positional):
    return {
        'number':     positional.number,
        'metavar':    positional.metavar,
        'help':       positional.help,
        'repeatable': positional.repeatable,
        'complete':   positional.complete,
        'nosort':     positional.nosort,
        'when':       positional.when,
        'capture':    positional.capture,
    }


def _commandline_to_definition(cmdline):
    options = list(map(_option_to_definition, cmdline.options))
    positionals = list(map(_positional_to_definition, cmdline.positionals))

    definition = {
        'prog':                cmdline.get_command_path(),
        'help':                cmdline.help,
        'aliases':             cmdline.aliases,
        'wraps':               cmdline.wraps,
        'abbreviate_commands': cmdline.abbreviate_commands,
        'abbreviate_options':  cmdline.abbreviate_options,
        'inherit_options':     cmdline.inherit_options,
        'options':             options,
        'positionals':         positionals,
    }

    return _mk_value_without_trace(definition)


def _commandlines_to_definition_list(commandline):
    result = []

    def callback(cmdline):
        result.append(_commandline_to_definition(cmdline))

    commandline.visit_commandlines(callback)

    return result


def validate_commandlines(cmdline):
    '''Validate commandlines.'''
    definitions = _commandlines_to_definition_list(cmdline)
    scheme_validator.validate(definitions)
