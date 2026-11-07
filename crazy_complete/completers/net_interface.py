# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2025-2026 Benjamin Abendroth <braph93@gmx.de>

'''Completer for network interfaces.'''

from .. import bash_versions
from ..bash_complete import BashCompletionFunc
from ..fish_complete import FishCompletionCommand
from ..zsh_complete import ZshComplFunc

CATEGORY = 'basic'

SHORT = 'Complete network interfaces'

ALSO = {
    'ip_address': 'For completing IP addresses',
}

DEFINITION = r'''
prog: 'example'
options:
  - option_strings: ['--net-interface']
    complete: ['net_interface']
'''

OUTPUT = r'''
~ > example --net-interface=<TAB>
eno1  enp1s0  lo  wlo1  wlp2s0
[...]
'''

def validate(_ctxt, arguments):
    '''Validate YAML for net_interface completer'''
    arguments.require_no_more()


def bash(_completer, ctxt, _trace):
    '''Implement net_interface for bash'''
    func = bash_versions.available_interfaces(ctxt)
    return BashCompletionFunc(ctxt, [func])


def fish(_completer, ctxt, _trace):
    '''Implement net_interface for fish'''
    return FishCompletionCommand(ctxt, ['__fish_print_interfaces'])


def zsh(_completer, ctxt, _trace):
    '''Implement net_interface for zsh'''
    return ZshComplFunc(ctxt, ['_net_interfaces'])
