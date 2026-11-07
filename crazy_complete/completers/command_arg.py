# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2025-2026 Benjamin Abendroth <braph93@gmx.de>

'''Completer for the command itself.'''

from .. import messages as m
from ..bash_complete import BashCompletionCode
from ..fish_complete import FishCompleteCommandArg
from ..zsh_complete import ZshComplFunc
from ..errors import CrazySchemaValidationError
from ..scheme_validator import Context, has_set

CATEGORY = 'basic'

SHORT = 'Complete command arguments'

NOTES = [
    'This completer can only be used in combination with a previously defined `command` completer.',
    'This completer requires `repeatable: true`.',
]

ALSO = {
    'command': 'For completing command names',
    'commandline_string': 'For completing command lines as strings',
}

DEFINITION = r'''
prog: 'example'
positionals:
  - number: 1
    complete: ['command']

  - number: 2
    complete: ['command_arg']
    repeatable: true
'''

OUTPUT = r'''
~ > example sudo bas<TAB>
base32    base64    basename  basenc    bash      bashbug
'''

_error = CrazySchemaValidationError


def validate(ctxt, arguments):
    '''Validate YAML for command_arg completer'''
    arguments.require_no_more()

    if ctxt.trace and ctxt.trace[-1] in ('combine', 'list', 'key_value_list', 'key_value_pair'):
        msg = m.completer_not_allowed_in('command_arg', ctxt.trace[-1])
        raise _error(msg, arguments.args)

    if ctxt.type != Context.TYPE_POSITIONAL:
        msg = m.completer_not_allowed_in_option('command_arg')
        raise _error(msg, arguments.args)

    if (not has_set(ctxt.positional, 'repeatable') or
        not ctxt.positional.value['repeatable'].value):
        msg = m.completer_requires_repeatable('command_arg')
        raise _error(msg, ctxt.positional)

    def command_is_previous_to_command_arg(positional):
        return (
            has_set(positional, 'complete') and
            positional.value['complete'].value[0] == 'command' and
            positional.value['number'].value + 1 == ctxt.positional.value['number'].value
        )

    positionals = ctxt.definition.value['positionals'].value
    if not any(filter(command_is_previous_to_command_arg, positionals)):
        msg = m.command_arg_without_command()
        raise _error(msg, ctxt.positional)


def bash(_completer, ctxt, _trace):
    '''Implement command_arg for bash'''
    return BashCompletionCode(ctxt, '')


def fish(_completer, ctxt, _trace):
    '''Implement command_arg for fish'''
    return FishCompleteCommandArg(ctxt)


def zsh(_completer, ctxt, _trace):
    '''Implement command_arg for zsh'''
    return ZshComplFunc(ctxt, ['_normal'])
