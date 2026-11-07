# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2025-2026 Benjamin Abendroth <braph93@gmx.de>

'''Completer for file system types.'''

from .. import bash_versions
from ..bash_complete import BashCompletionFunc
from ..fish_complete import FishCompletionCommand
from ..zsh_complete import ZshComplFunc

CATEGORY = 'basic'

SHORT = 'Complete filesystem types'

DEFINITION = r'''
prog: 'example'
options:
  - option_strings: ['--filesystem-type']
    complete: ['filesystem_type']
'''

OUTPUT = r'''
~ > example --filesystem-type=<TAB>
adfs     autofs   bdev      bfs     binder     binfmt_misc  bpf
cgroup   cgroup2  configfs  cramfs  debugfs    devpts       devtmpfs
[...]
'''

def validate(_ctxt, arguments):
    '''Validate YAML for filesystem_type completer'''
    arguments.require_no_more()


def bash(_completer, ctxt, _trace):
    '''Implement filesystem_type for bash'''
    return BashCompletionFunc(ctxt, [bash_versions.fstypes(ctxt)])


def fish(_completer, ctxt, _trace):
    '''Implement filesystem_type for fish'''
    return FishCompletionCommand(ctxt, ['__fish_print_filesystems'])


def zsh(_completer, ctxt, _trace):
    '''Implement filesystem_type for zsh'''
    return ZshComplFunc(ctxt, ['_file_systems'])
