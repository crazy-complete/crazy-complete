# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2025-2026 Benjamin Abendroth <braph93@gmx.de>

'''Completer for host names.'''

from ..bash_complete import BashCompletionCompgen
from ..fish_complete import FishCompletionCommand
from ..zsh_complete import ZshComplFunc

CATEGORY = 'basic'

SHORT = 'Complete hostnames'

ALSO = {
    'ip_address': 'For completing local IP addresses',
}

DEFINITION = r'''
prog: 'example'
options:
  - option_strings: ['--hostname']
    complete: ['hostname']
'''

OUTPUT = r'''
~ > example --hostname=<TAB>
localhost
'''

def validate(_ctxt, arguments):
    '''Validate YAML for hostname completer'''
    arguments.require_no_more()


def bash(_completer, ctxt, _trace):
    '''Implement hostname for bash'''
    return BashCompletionCompgen(ctxt, '-A hostname')


def fish(_completer, ctxt, _trace):
    '''Implement hostname for fish'''
    return FishCompletionCommand(ctxt, ["__fish_print_hostnames"])


def zsh(_completer, ctxt, _trace):
    '''Implement hostname for zsh'''
    return ZshComplFunc(ctxt, ['_hosts'])
