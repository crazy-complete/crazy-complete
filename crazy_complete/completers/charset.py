# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2025-2026 Benjamin Abendroth <braph93@gmx.de>

'''Completer for character sets.'''

from ..bash_complete import BashCompletionFunc
from ..zsh_complete import ZshComplFunc
from ..helpers import ShellFunction
from ..bash_helpers import BashHelpers
from ..zsh_helpers import ZshHelpers

CATEGORY = 'basic'

SHORT = 'Complete character sets'

DEFINITION = r'''
prog: 'example'
options:
  - option_strings: ['--charset']
    complete: ['charset']
'''

OUTPUT = r'''
~ > example --charset=A<TAB>
ANSI_X3.110-1983  ANSI_X3.4-1968    ARMSCII-8         ASMO_449
'''

_CHARSETS_BASH = ShellFunction('''charsets''', r'''
COMPREPLY=($(compgen -W "$(command locale -m)" -- "$cur"))
''')

_CHARSET_LIST_ZSH = ShellFunction('charset_list', r'''
local items=($(command locale -m))
_describe 'charsets' items
''')

BashHelpers.add_function(_CHARSETS_BASH)
ZshHelpers.add_function(_CHARSET_LIST_ZSH)


def validate(_ctxt, arguments):
    '''Validate YAML for charset completer'''
    arguments.require_no_more()


def bash(_completer, ctxt, _trace):
    '''Implement charset for bash'''
    func = ctxt.helpers.use_function('charsets')
    return BashCompletionFunc(ctxt, [func])


def fish(completer, ctxt, trace):
    '''Implement charset for fish'''
    return completer.complete(ctxt, trace, 'exec', "command locale -m")


def zsh(_completer, ctxt, _trace):
    '''Implement charset for zsh'''
    func = ctxt.helpers.use_function('charset_list')
    return ZshComplFunc(ctxt, [func], needs_braces=True)
