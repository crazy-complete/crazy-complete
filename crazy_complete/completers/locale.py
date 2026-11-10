# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2025-2026 Benjamin Abendroth <braph93@gmx.de>

'''Completer for locales.'''

from ..bash_complete import BashCompletionFunc
from ..zsh_complete import ZshComplFunc
from ..helpers import ShellFunction
from ..bash_helpers import BashHelpers

CATEGORY = 'basic'

SHORT = 'Complete locales'

ALSO = {
    'language': 'For completing languages',
}

DEFINITION = r'''
prog: 'example'
options:
  - option_strings: ['--locale']
    complete: ['locale']
'''

OUTPUT = r'''
~ > example --locale=<TAB>
C  C.UTF-8  de_DE  de_DE@euro  de_DE.iso88591  de_DE.iso885915@euro
de_DE.UTF-8  deutsch  en_US  en_US.iso88591  en_US.UTF-8  german  POSIX
'''

_LOCALES_BASH = ShellFunction('''locales''', r'''
COMPREPLY=($(compgen -W "$(command locale -a)" -- "$cur"))
''')

BashHelpers.add_function(_LOCALES_BASH)


def validate(_ctxt, arguments):
    '''Validate YAML for locale completer'''
    arguments.require_no_more()


def bash(_completer, ctxt, _trace):
    '''Implement locale for bash'''
    func = ctxt.helpers.use_function('locales')
    return BashCompletionFunc(ctxt, [func])


def fish(completer, ctxt, trace):
    '''Implement locale for fish'''
    return completer.complete(ctxt, trace, 'exec', "command locale -a")


def zsh(_completer, ctxt, _trace):
    '''Implement locale for zsh'''
    return ZshComplFunc(ctxt, ['_locales'])
