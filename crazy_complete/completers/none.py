# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2025-2026 Benjamin Abendroth <braph93@gmx.de>

'''Completer for explicitly no completion.'''

from .. import messages as m
from ..bash_complete import BashCompletionCode
from ..fish_complete import FishCompleteNone
from ..zsh_complete import ZshComplFunc
from ..errors import CrazySchemaValidationError

CATEGORY = 'meta'

SHORT = 'No completion, but specify that an argument is required'

LONG = r'''
Disables autocompletion for an option but still marks it as requiring an argument.

Without specifying `complete`, the option would not take an argument.
'''

DEFINITION = r'''
prog: 'example'
options:
  - option_strings: ['--none']
    complete: ['none']
'''

OUTPUT = r'''
~ > example --none=<TAB>
<NO OUTPUT>
'''

_error = CrazySchemaValidationError


def validate(ctxt, arguments):
    '''Validate YAML for none completer'''
    arguments.require_no_more()

    if ctxt.trace and ctxt.trace[-1] in ('combine', 'list', 'prefix', 'suffix', 'filter'):
        msg = m.completer_not_allowed_in('none', ctxt.trace[-1])
        raise _error(msg, arguments.args)


def bash(_completer, ctxt, _trace, *_):
    '''Implement none for bash'''
    return BashCompletionCode(ctxt, '')


def fish(_completer, ctxt, _trace, *_):
    '''Implement none for fish'''
    return FishCompleteNone(ctxt)


def zsh(_completer, ctxt, _trace, *_):
    '''Implement none for zsh'''
    return ZshComplFunc(ctxt, [' '])
