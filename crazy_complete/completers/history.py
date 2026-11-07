# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2025-2026 Benjamin Abendroth <braph93@gmx.de>

'''Completer for history entries matching a pattern.'''

from ..bash_complete import BashCompletionFunc
from ..fish_complete import FishCompletionCommand
from ..zsh_complete import ZshComplFunc
from ..scheme_validator import check_type, check_regex
from ..helpers import ShellFunction
from ..helpers import FishFunction
from ..bash_helpers import BashHelpers
from ..fish_helpers import FishHelpers
from ..zsh_helpers import ZshHelpers

CATEGORY = 'basic'

SYNOPSIS = r'''
['history', <REGEX>]
'''

SHORT = "Complete based on a shell's history"

LONG = r'''
`REGEX`:
  An extended regular expression used to filter history entries.
  The regular expression is passed to `grep -E`.
'''

DEFINITION = r'''
prog: 'example'
options:
  - option_strings: ['--history']
    complete: ['history', '[a-zA-Z0-9]+@[a-zA-Z0-9]+']
'''

OUTPUT = r'''
~ > example --history=<TAB>
foo@bar  mymail@myprovider
'''

_HISTORY_BASH = ShellFunction('history', r'''
[[ -f "$HISTFILE" ]] || return

local match

while read -r match; do
  if [[ "$match" == "$cur"* ]]; then
    COMPREPLY+=("$(printf '%q' "$match")")
  fi
done < <(command grep -E -o -- "$1" "$HISTFILE")
''')

_HISTORY_FISH = FishFunction('history', r'''
builtin history | command grep -E -o -- $argv[1]
''')

_HISTORY_ZSH = ShellFunction('history', r'''
[[ -f "$HISTFILE" ]] || return

local match=''

command grep -E -o -- "$1" "$HISTFILE" | while read -r match; do
  compadd -- "$match"
done
''')

BashHelpers.add_function(_HISTORY_BASH)
FishHelpers.add_function(_HISTORY_FISH)
ZshHelpers.add_function(_HISTORY_ZSH)


def validate(_ctxt, arguments):
    '''Validate YAML for history completer'''
    pattern = arguments.get_required_arg("pattern")
    check_type(pattern, (str,), "pattern")
    arguments.require_no_more()
    check_regex(pattern, 'pattern')


def bash(_completer, ctxt, _trace, pattern):
    '''Implement history for bash'''
    func = ctxt.helpers.use_function('history')
    return BashCompletionFunc(ctxt, [func, pattern])


def fish(_completer, ctxt, _trace, pattern):
    '''Implement history for fish'''
    func = ctxt.helpers.use_function('history')
    return FishCompletionCommand(ctxt, [func, pattern])


def zsh(_completer, ctxt, _trace, pattern):
    '''Implement history for zsh'''
    func = ctxt.helpers.use_function('history')
    return ZshComplFunc(ctxt, [func, pattern], needs_braces=True)
