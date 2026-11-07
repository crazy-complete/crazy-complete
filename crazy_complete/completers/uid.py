# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2025-2026 Benjamin Abendroth <braph93@gmx.de>

'''Completer for user ids.'''

from .. import bash_versions
from ..bash_complete import BashCompletionFunc
from ..fish_complete import FishCompletionCommand
from ..zsh_complete import ZshComplFunc
from ..helpers import ShellFunction
from ..zsh_helpers import ZshHelpers

CATEGORY = 'basic'

SHORT = 'Complete user IDs'

ALSO = {
    'user': 'For completing user names',
}

DEFINITION = r'''
prog: 'example'
options:
  - option_strings: ['--uid']
    complete: ['uid']
'''

OUTPUT = r'''
~ > example --uid=<TAB>
0      -- root
1000   -- braph
102    -- polkitd
133    -- rtkit
14     -- ftp
1      -- bin
2      -- daemon
33     -- http
65534  -- nobody
[...]
'''

_UID_LIST_ZSH = ShellFunction('uid_list', r'''
local items=($(command getent passwd | command awk -F: '{printf "%s:%s\n", $3, $1}'))
_describe 'users' items
''')

ZshHelpers.add_function(_UID_LIST_ZSH)


def validate(_ctxt, arguments):
    '''Validate YAML for uid completer'''
    arguments.require_no_more()


def bash(_completer, ctxt, _trace):
    '''Implement uid for bash'''
    return BashCompletionFunc(ctxt, [bash_versions.uids(ctxt)])


def fish(_completer, ctxt, _trace):
    '''Implement uid for fish'''
    return FishCompletionCommand(ctxt, ['__fish_complete_user_ids'])


def zsh(_completer, ctxt, _trace):
    '''Implement uid for zsh'''
    func = ctxt.helpers.use_function('uid_list')
    return ZshComplFunc(ctxt, [func], needs_braces=True)
