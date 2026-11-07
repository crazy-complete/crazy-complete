# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2025-2026 Benjamin Abendroth <braph93@gmx.de>

'''Completer that filters the results of another completer.'''

from .. import shell
from ..bash_complete import BashCompletionCode
from ..fish_complete import FishCompletionCommand
from ..pattern import bash_glob_to_regex, bash_glob_to_zsh_glob
from ..zsh_complete import ZshComplFunc
from ..errors import CrazySchemaValidationError
from ..scheme_validator import (
    check_type, check_non_empty_string, check_non_empty_list,
    check_complete)
from ..helpers import ShellFunction
from ..helpers import FishFunction
from ..bash_helpers import BashHelpers
from ..fish_helpers import FishHelpers
from ..zsh_helpers import ZshHelpers

CATEGORY = 'meta'

SYNOPSIS = r'''
['filter', <GLOB_PATTERNS>, <COMPLETER>]
'''

SHORT = 'Filters (removes) completion candidates from a completer'

LONG = r'''
`GLOB_PATTERNS`:
  A list of Bash glob patterns that are used for removing the candidates.

`COMPLETER`:
  The completer used to generate the completion candidates.
'''

NOTES = [
    'For filtering files or directories, use the `ignore_globs` option of the `file`/`directory` completer',
]

DEFINITION = r'''
prog: 'example'
options:
  - option_strings: ['--filter']
    complete: ['filter', ['a*'], ['choices', ['apple', 'banana', 'cherry']]]
'''

OUTPUT = r'''
~ > example --filter=<TAB>
banana  cherry
'''

_error = CrazySchemaValidationError

_FILTER_BASH = ShellFunction('filter', r'''
local item pattern copy=("${COMPREPLY[@]}")
COMPREPLY=()
for item in "${copy[@]}"; do
  for pattern in "$@"; do
    [[ "$item" == $pattern ]] && continue 2
  done

  COMPREPLY+=("$item")
done
''')

_FILTER_FISH = FishFunction('filter', r'''
set -l pattern $argv[1]
set -l func $argv[2]
set -l line
set -l split

$func | while read line
  set split (string split -m1 -- \t "$line")
  if not string match -qr -- $pattern "$split[1]"
    printf "%s\t%s\n" "$split[1]" "$split[2]"
  end
end
''')

_FILTER_ZSH = ShellFunction('filter', r'''
local _COMPADD_WRAPPER_FILTER="$1" func="$2"
{
  function compadd() { compadd_wrapper "$@"; }
  $func
} always {
  unfunction compadd 2>/dev/null
}
''', ['compadd_wrapper'])

BashHelpers.add_function(_FILTER_BASH)
FishHelpers.add_function(_FILTER_FISH)
ZshHelpers.add_function(_FILTER_ZSH)


def validate(ctxt, arguments):
    '''Validate YAML for filter completer'''
    patterns = arguments.get_required_arg('patterns')
    command = arguments.get_required_arg('command')
    arguments.require_no_more()

    check_type(patterns, (list,), 'patterns')
    check_type(command, (list,), 'command')

    check_non_empty_list(patterns, 'patterns')

    for pattern in patterns.value:
        check_type(pattern, (str,), 'pattern')
        check_non_empty_string(pattern, 'pattern')
        try:
            bash_glob_to_regex(pattern.value)
            bash_glob_to_zsh_glob(pattern.value)
        except ValueError as e:
            raise _error('%s: %s' % ('pattern', e), pattern) from e

    ctxt.trace.append('filter')
    check_complete(ctxt, command)


def bash(completer, ctxt, trace, patterns, command):
    '''Implement filter for bash'''
    obj = completer.complete_from_def(ctxt, trace, command)
    filter_func = ctxt.helpers.use_function('filter')

    code = f'{obj.get_code()}\n'
    code += f'{filter_func} {shell.join_quoted(patterns)}'
    return BashCompletionCode(ctxt, code)


def fish(completer, ctxt, trace, patterns, command):
    '''Implement filter for fish'''
    obj = completer.complete_from_def(ctxt, trace, command)
    func = obj.get_function()
    filter_func = ctxt.helpers.use_function('filter')

    pattern = f'^({"|".join(bash_glob_to_regex(p) for p in patterns)})$'

    return FishCompletionCommand(ctxt, [filter_func, pattern, func])


def zsh(completer, ctxt, trace, patterns, command):
    '''Implement filter for zsh'''
    filter_func = ctxt.helpers.use_function('filter')
    obj = completer.complete_from_def(ctxt, trace, command)
    func = obj.get_function()

    pattern = f'({" ".join(bash_glob_to_zsh_glob(p) for p in patterns)})'

    return ZshComplFunc(ctxt, [filter_func, pattern, func], needs_braces=True)
