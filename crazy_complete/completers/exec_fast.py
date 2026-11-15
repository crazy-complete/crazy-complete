# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2025-2026 Benjamin Abendroth <braph93@gmx.de>

'''Completer that executes a shell command, fast variant.'''

from ..bash_complete import BashCompletionFunc
from ..fish_complete import FishCompletionRawCommand
from ..zsh_complete import ZshComplFunc
from ..completers import _validate
from ..helpers import ShellFunction
from ..bash_helpers import BashHelpers

CATEGORY = 'custom'

HIDDEN = True

SYNOPSIS = r'''
['exec_fast', <COMMAND>]
'''

SHORT = 'Complete values from the output of a command or function (fast and unsafe)'

LONG = r'''
Faster version of `exec` for handling large amounts of data.

Unlike `exec`, this implementation does not safely handle arbitrary output.
Completion items must not contain whitespace or special shell characters.
'''

NOTES = [
    'This completer is deprecated',
    'Functions can be put inside a file and included with `--include-file`',
]

DEFINITION = r'''
prog: 'example'
options:
  - option_strings: ['--exec-fast']
    complete: ['exec_fast', "printf '%s\\t%s\\n' 1 one 2 two"]
'''

OUTPUT = r'''
~ > example --exec-fast=<TAB>
1  -- one
2  -- one
'''


def validate(ctxt, arguments):
    '''Validate YAML for exec_fast completer'''
    _validate.check_exec(ctxt, arguments)


def bash(_completer, ctxt, _trace, command):
    '''Implement exec_fast for bash'''
    func = ctxt.helpers.use_function('exec')
    return BashCompletionFunc(ctxt, [func, command])


def fish(_completer, ctxt, _trace, command):
    '''Implement exec_fast for fish'''
    return FishCompletionRawCommand(ctxt, command)


def zsh(_completer, ctxt, _trace, command):
    '''Implement exec_fast for zsh'''
    funcname = ctxt.helpers.use_function('exec')
    return ZshComplFunc(ctxt, [funcname, command], needs_braces=True)
