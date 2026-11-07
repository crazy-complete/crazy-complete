# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2025-2026 Benjamin Abendroth <braph93@gmx.de>

'''Completer for system groups.'''

from ..bash_complete import BashCompletionCompgen
from ..fish_complete import FishCompletionCommand
from ..zsh_complete import ZshComplFunc

CATEGORY = 'basic'

SHORT = 'Complete group names'

ALSO = {
    'gid': 'For completing group IDs',
}

DEFINITION = r'''
prog: 'example'
options:
  - option_strings: ['--group']
    complete: ['group']
'''

OUTPUT = r'''
~ > example --group=<TAB>
adm           audio        avahi
bin           braph        colord
daemon        dbus         dhcpcd
disk          floppy       ftp
games         git          groups
[...]
'''

def validate(_ctxt, arguments):
    '''Validate YAML for group completer'''
    arguments.require_no_more()


def bash(_completer, ctxt, _trace):
    '''Implement group for bash'''
    return BashCompletionCompgen(ctxt, '-A group')


def fish(_completer, ctxt, _trace):
    '''Implement group for fish'''
    return FishCompletionCommand(ctxt, ["__fish_complete_groups"])


def zsh(_completer, ctxt, _trace):
    '''Implement group for zsh'''
    return ZshComplFunc(ctxt, ['_groups'])
