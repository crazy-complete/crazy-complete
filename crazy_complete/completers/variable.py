# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2025-2026 Benjamin Abendroth <braph93@gmx.de>

'''Completer for shell variables.'''

from ..bash_complete import BashCompletionCompgen
from ..fish_complete import FishCompletionCommand
from ..zsh_complete import ZshComplFunc

CATEGORY = 'basic'

SHORT = 'Complete shell variable names'

ALSO = {
    'environment': 'For completing environment variable names',
}

DEFINITION = r'''
prog: 'example'
options:
  - option_strings: ['--variable']
    complete: ['variable']
'''

OUTPUT = r'''
~ > example --variable=HO<TAB>
HOME      HOSTNAME  HOSTTYPE
'''

def validate(_ctxt, arguments):
    '''Validate YAML for variable completer'''
    arguments.require_no_more()


def bash(_completer, ctxt, _trace):
    '''Implement variable for bash'''
    return BashCompletionCompgen(ctxt, '-A variable')


def fish(_completer, ctxt, _trace):
    '''Implement variable for fish'''
    return FishCompletionCommand(ctxt, ["set", "-n"])


def zsh(_completer, ctxt, _trace):
    '''Implement variable for zsh'''
    return ZshComplFunc(ctxt, ['_vars'])
