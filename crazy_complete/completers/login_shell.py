# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2025-2026 Benjamin Abendroth <braph93@gmx.de>

'''Completer for login shells.'''

from .. import bash_versions
from ..bash_complete import BashCompletionFunc

CATEGORY = 'basic'

SHORT = 'Complete login shells'

DEFINITION = r'''
prog: 'example'
options:
  - option_strings: ['--login-shell']
    complete: ['login_shell']
'''

OUTPUT = r'''
~ > example --login-shell=<TAB>
/bin/bash   /bin/sh         /usr/bin/fish       /usr/bin/sh
[...]
'''

def validate(_ctxt, arguments):
    '''Validate YAML for login_shell completer'''
    arguments.require_no_more()


def bash(_completer, ctxt, _trace):
    '''Implement login_shell for bash'''
    return BashCompletionFunc(ctxt, [bash_versions.shells(ctxt)])


def fish(completer, ctxt, trace):
    '''Implement login_shell for fish'''
    return completer.complete(
        ctxt, trace, 'exec', "command grep -E '^[^#]' /etc/shells")


def zsh(completer, ctxt, trace):
    '''Implement login_shell for zsh'''
    return completer.complete(
        ctxt, trace, 'exec', "command grep -E '^[^#]' /etc/shells")
