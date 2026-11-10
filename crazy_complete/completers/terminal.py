# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2025-2026 Benjamin Abendroth <braph93@gmx.de>

'''Completer for terminals.'''

CATEGORY = 'basic'

SHORT = 'Complete terminals that are in use'

DEFINITION = r'''
prog: 'example'
options:
  - option_strings: ['--terminal']
    complete: ['terminal']
'''

OUTPUT = r'''
~ > example --terminal=<TAB>
pts/0  (user)
pts/7  (root)
tty1   (root)
'''

# `ps aux` lists the TTY (7th column) and the owning user (1st column) for
# every running process. Deduplicate the TTYs and offer each one, described
# by the user it belongs to.
_COMMAND = r"""ps aux | awk 'NR>1 && NF>6 && $7!="?" && $7!="" && !seen[$7]++ {printf "%s\t%s\n",$7,$1}' | sort -u"""


def validate(_ctxt, arguments):
    '''Validate YAML for terminal completer'''
    arguments.require_no_more()


def bash(completer, ctxt, trace):
    '''Implement terminal for bash'''
    return completer.complete(ctxt, trace, 'exec', _COMMAND)


def fish(completer, ctxt, trace):
    '''Implement terminal for fish'''
    return completer.complete(ctxt, trace, 'exec', _COMMAND)


def zsh(completer, ctxt, trace):
    '''Implement terminal for zsh'''
    return completer.complete(ctxt, trace, 'exec', _COMMAND)
