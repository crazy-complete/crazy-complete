# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2025-2026 Benjamin Abendroth <braph93@gmx.de>

'''Completer for environment variables.'''

from ..bash_complete import BashCompletionCompgen
from ..fish_complete import FishCompletionCommand
from ..zsh_complete import ZshComplFunc

CATEGORY = 'basic'

SHORT = 'Complete environment variable names'

ALSO = {
    'variable': 'For completing shell variable names',
}

DEFINITION = r'''
prog: 'example'
options:
  - option_strings: ['--environment']
    complete: ['environment']
'''

OUTPUT = r'''
~ > example --environment=X<TAB>
XDG_RUNTIME_DIR  XDG_SEAT  XDG_SESSION_CLASS  XDG_SESSION_ID
XDG_SESSION_TYPE XDG_VTNR
'''

def validate(_ctxt, arguments):
    '''Validate YAML for environment completer'''
    arguments.require_no_more()


def bash(_completer, ctxt, _trace):
    '''Implement environment for bash'''
    return BashCompletionCompgen(ctxt, '-A export')


def fish(_completer, ctxt, _trace):
    '''Implement environment for fish'''
    return FishCompletionCommand(ctxt, ["set", "-n", "-x"])


def zsh(_completer, ctxt, _trace):
    '''Implement environment for zsh'''
    return ZshComplFunc(ctxt, ['_parameters', '-g', '*export*'])
