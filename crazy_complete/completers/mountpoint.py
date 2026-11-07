# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2025-2026 Benjamin Abendroth <braph93@gmx.de>

'''Completer for mount points.'''

from ..bash_complete import BashCompletionFunc
from ..fish_complete import FishCompletionCommand
from ..zsh_complete import ZshComplFunc
from ..helpers import ShellFunction
from ..bash_helpers import BashHelpers
from ..zsh_helpers import ZshHelpers

CATEGORY = 'basic'

SHORT = 'Complete mount points'

DEFINITION = r'''
prog: 'example'
options:
  - option_strings: ['--mountpoint']
    complete: ['mountpoint']
'''

OUTPUT = r'''
~ > example --mountpoint=<TAB>
/  /boot  /home  /proc  /run  /sys  /tmp
[...]
'''

_MOUNTPOINT_BASH = ShellFunction('mountpoint', r'''
local REPLY

COMPREPLY=()

while read -r REPLY; do
  COMPREPLY+=("$(printf '%q' "$REPLY")")
done < <(command findmnt -lno TARGET)
''')

_MOUNTPOINT_ZSH = ShellFunction('mountpoint', r'''
local item=''

command findmnt -lno TARGET | while read -r item; do
  compadd -- "$item"
done
''')

BashHelpers.add_function(_MOUNTPOINT_BASH)
ZshHelpers.add_function(_MOUNTPOINT_ZSH)


def validate(_ctxt, arguments):
    '''Validate YAML for mountpoint completer'''
    arguments.require_no_more()


def bash(_completer, ctxt, _trace):
    '''Implement mountpoint for bash'''
    func = ctxt.helpers.use_function('mountpoint')
    return BashCompletionFunc(ctxt, [func])


def fish(_completer, ctxt, _trace):
    '''Implement mountpoint for fish'''
    return FishCompletionCommand(ctxt, ['__fish_print_mounted'])


def zsh(_completer, ctxt, _trace):
    '''Implement mountpoint for zsh'''
    func = ctxt.helpers.use_function('mountpoint')
    return ZshComplFunc(ctxt, [func], needs_braces=True)
