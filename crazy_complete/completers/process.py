# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2025-2026 Benjamin Abendroth <braph93@gmx.de>

'''Completer for process names.'''

from .. import bash_versions
from ..bash_complete import BashCompletionFunc
from ..fish_complete import FishCompletionCommand
from ..zsh_complete import ZshComplFunc

CATEGORY = 'basic'

SHORT = 'Complete process names'

ALSO = {
    'pid': 'For completing process IDs',
}

DEFINITION = r'''
prog: 'example'
options:
  - option_strings: ['--process']
    complete: ['process']
'''

OUTPUT = r'''
~ > example --process=s<TAB>
scsi_eh_0         scsi_eh_1       scsi_eh_2      scsi_eh_3  scsi_eh_4
scsi_eh_5         sh              sudo           syndaemon  systemd
systemd-journald  systemd-logind  systemd-udevd
'''

def validate(_ctxt, arguments):
    '''Validate YAML for process completer'''
    arguments.require_no_more()


def bash(_completer, ctxt, _trace):
    '''Implement process for bash'''
    return BashCompletionFunc(ctxt, [bash_versions.pnames(ctxt)])


def fish(_completer, ctxt, _trace):
    '''Implement process for fish'''
    return FishCompletionCommand(ctxt, ["__fish_complete_proc"])


def zsh(_completer, ctxt, _trace):
    '''Implement process for zsh'''
    return ZshComplFunc(ctxt, ['_process_names', '-a'])
