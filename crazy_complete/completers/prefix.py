# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2025-2026 Benjamin Abendroth <braph93@gmx.de>

'''Completer that prepends a prefix to another completer.'''

from ..bash_complete import BashCompletionFunc
from ..fish_complete import FishCompletionCommand
from ..zsh_complete import ZshComplFunc
from ..scheme_validator import check_type, check_complete
from ..helpers import ShellFunction
from ..helpers import FishFunction
from ..fish_helpers import FishHelpers
from ..zsh_helpers import ZshHelpers

CATEGORY = 'meta'

SYNOPSIS = r'''
['prefix', <PREFIX>, <COMPLETER>]
'''

SHORT = 'Prefix completions with a string'

LONG = r'''
`PREFIX`:
  The string to prepend to each completion candidate.

`COMPLETER`:
  The completer used to generate the completion candidates.
'''

DEFINITION = r'''
prog: 'example'
options:
  - option_strings: ['--prefix']
    complete: ['prefix', 'input:', ['file']]
'''

OUTPUT = r'''
~ > example --prefix=<TAB>
~ > example --prefix=input:

~ > example --prefix=input:<TAB>
~ > example --prefix=input:file1.txt
'''

_PREFIX_FISH = FishFunction('prefix', r'''
set -l comp (get_completing_arg)
set -l prefix_escaped (string escape --style=regex -- $argv[1])
if string match -qr -- $prefix_escaped $comp
  set -g __fish_stripprefix "^"$prefix_escaped
  printf "%s\n" $argv[1](eval $argv[2])
  set -e __fish_stripprefix
else
  printf "%s\n" $argv[1]
end
''', ['get_completing_arg'])

_PREFIX_ZSH = ShellFunction('prefix', r'''
if [[ "$PREFIX" == "$1"* ]]; then
  PREFIX="${PREFIX#"$1"}"
  IPREFIX="$IPREFIX$1"
  $2
else
  compadd -S '' -- "$1"
fi
''')

FishHelpers.add_function(_PREFIX_FISH)
ZshHelpers.add_function(_PREFIX_ZSH)


def validate(ctxt, arguments):
    '''Validate YAML for prefix completer'''
    prefix = arguments.get_required_arg('prefix')
    command = arguments.get_required_arg('command')
    arguments.require_no_more()

    check_type(prefix, (str,), 'prefix')
    check_type(command, (list,), 'command')

    ctxt.trace.append('prefix')
    check_complete(ctxt, command)


def bash(completer, ctxt, trace, prefix, command):
    '''Implement prefix for bash'''
    obj = completer.complete_from_def(ctxt, trace, command)
    func = obj.get_function()
    prefix_func = ctxt.helpers.use_function('prefix')
    return BashCompletionFunc(ctxt, [prefix_func, prefix, func])


def fish(completer, ctxt, trace, prefix, command):
    '''Implement prefix for fish'''
    obj = completer.complete_from_def(ctxt, trace, command)
    func = obj.get_function()
    prefix_func = ctxt.helpers.use_function('prefix')
    return FishCompletionCommand(ctxt, [prefix_func, prefix, func])


def zsh(completer, ctxt, trace, prefix, command):
    '''Implement prefix for zsh'''
    prefix_func = ctxt.helpers.use_function('prefix')
    obj = completer.complete_from_def(ctxt, trace, command)
    func = obj.get_function()
    return ZshComplFunc(ctxt, [prefix_func, prefix, func], needs_braces=True)
