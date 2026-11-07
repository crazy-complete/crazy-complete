# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2025-2026 Benjamin Abendroth <braph93@gmx.de>

'''Completer for group ids.'''

from .. import bash_versions
from ..bash_complete import BashCompletionFunc
from ..fish_complete import FishCompletionCommand
from ..zsh_complete import ZshComplFunc
from ..helpers import ShellFunction
from ..zsh_helpers import ZshHelpers

CATEGORY = 'basic'

SHORT = 'Complete group IDs'

ALSO = {
    'group': 'For completing group names',
}

DEFINITION = r'''
prog: 'example'
options:
  - option_strings: ['--gid']
    complete: ['gid']
'''

OUTPUT = r'''
~ > example --gid=<TAB>
0      -- root
1000   -- braph
102    -- polkitd
108    -- vboxusers
11     -- ftp
12     -- mail
133    -- rtkit
19     -- log
[...]
'''

_GID_LIST_ZSH = ShellFunction('gid_list', r'''
local items=($(command getent group | command awk -F: '{printf "%s:%s\n", $3, $1}'))
_describe 'groups' items
''')

ZshHelpers.add_function(_GID_LIST_ZSH)


def validate(_ctxt, arguments):
    '''Validate YAML for gid completer'''
    arguments.require_no_more()


def bash(_completer, ctxt, _trace):
    '''Implement gid for bash'''
    return BashCompletionFunc(ctxt, [bash_versions.gids(ctxt)])


def fish(_completer, ctxt, _trace):
    '''Implement gid for fish'''
    return FishCompletionCommand(ctxt, ['__fish_complete_group_ids'])


def zsh(_completer, ctxt, _trace):
    '''Implement gid for zsh'''
    func = ctxt.helpers.use_function('gid_list')
    return ZshComplFunc(ctxt, [func], needs_braces=True)
