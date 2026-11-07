# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2025-2026 Benjamin Abendroth <braph93@gmx.de>

'''Completer for system users.'''

from ..bash_complete import BashCompletionCompgen
from ..fish_complete import FishCompletionCommand
from ..zsh_complete import ZshComplFunc

CATEGORY = 'basic'

SHORT = 'Complete user names'

ALSO = {
    'uid': 'For completing user IDs',
}

DEFINITION = r'''
prog: 'example'
options:
  - option_strings: ['--user']
    complete: ['user']
'''

OUTPUT = r'''
~ > example --user=<TAB>
avahi         bin          braph
colord        daemon       dbus
dhcpcd        ftp          git
[...]
'''

def validate(_ctxt, arguments):
    '''Validate YAML for user completer'''
    arguments.require_no_more()


def bash(_completer, ctxt, _trace):
    '''Implement user for bash'''
    return BashCompletionCompgen(ctxt, '-A user')


def fish(_completer, ctxt, _trace):
    '''Implement user for fish'''
    return FishCompletionCommand(ctxt, ["__fish_complete_users"])


def zsh(_completer, ctxt, _trace):
    '''Implement user for zsh'''
    return ZshComplFunc(ctxt, ['_users'])
