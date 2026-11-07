# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2025-2026 Benjamin Abendroth <braph93@gmx.de>

'''Completer for system services.'''

from ..bash_complete import BashCompletionCompgen
from ..fish_complete import FishCompletionCommand

CATEGORY = 'basic'

SHORT = 'Complete systemd service names'

DEFINITION = r'''
prog: 'example'
options:
  - option_strings: ['--service']
    complete: ['service']
'''

OUTPUT = r'''
~ > example --service=<TAB>
TODO
[...]
'''

def validate(_ctxt, arguments):
    '''Validate YAML for service completer'''
    arguments.require_no_more()


def bash(_completer, ctxt, _trace):
    '''Implement service for bash'''
    return BashCompletionCompgen(ctxt, '-A service')


def fish(_completer, ctxt, _trace):
    '''Implement service for fish'''
    return FishCompletionCommand(ctxt, ["__fish_systemctl_services"])
