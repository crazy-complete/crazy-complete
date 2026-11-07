# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2025-2026 Benjamin Abendroth <braph93@gmx.de>

'''Completer for integers.'''

from ..bash_complete import BashCompletionCode, BashCompletionFunc
from ..fish_complete import FishCompleteNone, FishCompletionCommand
from ..zsh_complete import ZshComplFunc
from ..completers import _validate
from ..helpers import ShellFunction
from ..helpers import FishFunction
from ..bash_helpers import BashHelpers
from ..fish_helpers import FishHelpers

CATEGORY = 'basic'

SYNOPSIS = r'''
['integer']

['integer', <OPTIONS>]
'''

SHORT = 'Complete integer values'

LONG = r'''
`OPTIONS`:
  A dictionary containing additional options for configuring the completion.

  - `min`: The minimum allowed value.

  - `max`: The maximum allowed value.

  - `suffixes`: A dictionary of suffixes and their descriptions. The suffix is appended to the completed value.

  - `help`: The help text shown during completion. If not specified, the `help` attribute of the option is used.
'''

ALSO = {
    'float': 'For completing floating-point values',
    'range': 'For completing sequences of integers',
}

DEFINITION = r'''
prog: 'example'
options:
  - option_strings: ['--time']
    complete: ['integer', {'suffixes': {'s': 'seconds', 'm': 'minutes', 'h': 'hours'}}]
'''

OUTPUT = r'''
~ > example --integer=3<TAB>
s -- seconds  m -- minutes  h -- hours
'''

_NUMBER_BASH = ShellFunction('number', '''
local number="$(command grep -E -o '^[0-9,.]+' <<< "$cur")" suffix_and_desc

[[ -z "$number" ]] && return

COMPREPLY=("$number")

for suffix_and_desc; do
  COMPREPLY+=("${number}${suffix_and_desc%%:*}")
done
''')

_NUMBER_FISH = FishFunction('number', r'''
set -l comp (get_completing_arg)
set -l number (string match -r -- '^[0-9,.]*' $comp)

if test -z "$number"
  return
end

set -l suffix_and_desc
for suffix_and_desc in $argv
  set suffix_and_desc (string split -m 1 -- ':' $suffix_and_desc)
  printf '%s%s\t%s\n' $number $suffix_and_desc[1] $suffix_and_desc[2]
end
''', ['get_completing_arg'])

BashHelpers.add_function(_NUMBER_BASH)
FishHelpers.add_function(_NUMBER_FISH)


def validate(_ctxt, arguments):
    '''Validate YAML for integer completer'''
    _validate.check_integer(_ctxt, arguments)


def bash(_completer, ctxt, _trace, options=None):
    '''Implement integer for bash'''
    suffixes = []

    if options:
        if 'suffixes' in options:
            for suffix, description in options['suffixes'].items():
                suffixes.append(f'{suffix}:{description}')

    if not suffixes:
        return BashCompletionCode(ctxt, '')

    func = ctxt.helpers.use_function('number')
    return BashCompletionFunc(ctxt, [func, *suffixes])


def fish(_completer, ctxt, _trace, options=None):
    '''Implement integer for fish'''
    suffixes = []

    if options:
        if 'suffixes' in options:
            for suffix, description in options['suffixes'].items():
                suffixes.append(f'{suffix}:{description}')

    if not suffixes:
        return FishCompleteNone(ctxt)

    func = ctxt.helpers.use_function('number')
    return FishCompletionCommand(ctxt, [func, *suffixes])


def zsh(_completer, ctxt, _trace, options=None):
    '''Implement integer for zsh'''
    args = []
    suffixes = []
    help_ = ctxt.option.help or ctxt.option.metavar or ''

    if options:
        if 'min' in options:
            args += ['-l', str(options['min'])]
        if 'max' in options:
            args += ['-m', str(options['max'])]
        if 'suffixes' in options:
            for suffix, description in options['suffixes'].items():
                suffixes.append(f'{suffix}:{description}')
        if 'help' in options:
            help_ = options['help']

    return ZshComplFunc(ctxt, ['_numbers', *args, help_, *suffixes])
