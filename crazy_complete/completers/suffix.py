# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2025-2026 Benjamin Abendroth <braph93@gmx.de>

'''Completer that appends a suffix to another completer.'''

from ..bash_complete import BashCompletionFunc
from ..fish_complete import FishCompletionCommand
from ..zsh_complete import ZshComplFunc
from ..scheme_validator import (
    check_type, check_complete)
from ..helpers import ShellFunction
from ..helpers import FishFunction
from ..bash_helpers import BashHelpers
from ..fish_helpers import FishHelpers
from ..zsh_helpers import ZshHelpers

CATEGORY = 'meta'

SYNOPSIS = r'''
['suffix', <SUFFIX>, <COMPLETER>]
'''

SHORT = 'Append suffix to completions'

LONG = r'''
`SUFFIX`:
  The string to append to each completion candidate.

`COMPLETER`:
  The completer used to generate the completion candidates.
'''

DEFINITION = r'''
prog: 'example'
options:
  - option_strings: ['--suffix']
    complete: ['suffix', '.suffix', ['file']]
'''

OUTPUT = r'''
~ > example --suffix=file1<TAB>
~ > example --suffix=file1.suffix
'''

_SUFFIX_BASH = ShellFunction('suffix', r'''
local i suffix="$1" func="$2"

$func

for i in "${!COMPREPLY[@]}"; do
  COMPREPLY[i]="${COMPREPLY[i]}$suffix"
done
''')

_SUFFIX_FISH = FishFunction('suffix', r'''
set -l suffix $argv[1]
set -l func $argv[2]
set -l line
set -l split

$func | while read line
  set split (string split -m1 -- \t "$line")
  printf "%s\t%s\n" "$split[1]$suffix" "$split[2]"
end
''')

_SUFFIX_ZSH = ShellFunction('suffix', r'''
local _COMPADD_WRAPPER_SUFFIX="$1" func="$2"
{
  function compadd() { compadd_wrapper "$@"; }
  $func
} always {
  unfunction compadd 2>/dev/null
}
''', ['compadd_wrapper'])

BashHelpers.add_function(_SUFFIX_BASH)
FishHelpers.add_function(_SUFFIX_FISH)
ZshHelpers.add_function(_SUFFIX_ZSH)


def validate(ctxt, arguments):
    '''Validate YAML for suffix completer'''
    suffix = arguments.get_required_arg('suffix')
    command = arguments.get_required_arg('command')
    arguments.require_no_more()

    check_type(suffix, (str,), 'suffix')
    check_type(command, (list,), 'command')

    ctxt.trace.append('suffix')
    check_complete(ctxt, command)


def bash(completer, ctxt, trace, suffix, command):
    '''Implement suffix for bash'''
    obj = completer.complete_from_def(ctxt, trace, command)
    func = obj.get_function()
    suffix_func = ctxt.helpers.use_function('suffix')
    return BashCompletionFunc(ctxt, [suffix_func, suffix, func])


def fish(completer, ctxt, trace, suffix, command):
    '''Implement suffix for fish'''
    obj = completer.complete_from_def(ctxt, trace, command)
    func = obj.get_function()
    suffix_func = ctxt.helpers.use_function('suffix')
    return FishCompletionCommand(ctxt, [suffix_func, suffix, func])


def zsh(completer, ctxt, trace, suffix, command):
    '''Implement suffix for zsh'''
    suffix_func = ctxt.helpers.use_function('suffix')
    obj = completer.complete_from_def(ctxt, trace, command)
    func = obj.get_function()
    return ZshComplFunc(ctxt, [suffix_func, suffix, func], needs_braces=True)
