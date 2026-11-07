# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2025-2026 Benjamin Abendroth <braph93@gmx.de>

'''Completer for process identifiers.'''

from .. import bash_versions
from ..bash_complete import BashCompletionFunc
from ..fish_complete import FishCompletionCommand
from ..zsh_complete import ZshComplFunc

CATEGORY = 'basic'

SHORT = 'Complete process IDs'

ALSO = {
    'process': 'For completing process names',
}

DEFINITION = r'''
prog: 'example'
options:
  - option_strings: ['--pid']
    complete: ['pid']
'''

OUTPUT = r'''
~ > example --pid=<TAB>
1       13      166     19      254     31      45
1006    133315  166441  19042   26      32      46
10150   1392    166442  195962  27      33      4609
'''

def validate(_ctxt, arguments):
    '''Validate YAML for pid completer'''
    arguments.require_no_more()


def bash(_completer, ctxt, _trace):
    '''Implement pid for bash'''
    return BashCompletionFunc(ctxt, [bash_versions.pids(ctxt)])


def fish(_completer, ctxt, _trace):
    '''Implement pid for fish'''
    return FishCompletionCommand(ctxt, ["__fish_complete_pids"])


def zsh(_completer, ctxt, _trace):
    '''Implement pid for zsh'''
    return ZshComplFunc(ctxt, ['_pids'])
