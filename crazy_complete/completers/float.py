# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2025-2026 Benjamin Abendroth <braph93@gmx.de>

'''Completer for floating point numbers.'''

from ..zsh_complete import ZshComplFunc
from ..completers import _validate

CATEGORY = 'basic'

SYNOPSIS = r'''
['float']

['float', <OPTIONS>]
'''

SHORT = 'Complete floating-point values'

LONG = r'''
`OPTIONS`:
  A dictionary containing additional options for configuring the completion.

  - `min`: The minimum allowed value.

  - `max`: The maximum allowed value.

  - `suffixes`: A dictionary of suffixes and their descriptions. The suffix is appended to the completed value.

  - `help`: The help text shown during completion. If not specified, the `help` attribute of the option is used.
'''

ALSO = {
    'integer': 'For completing integer values',
}

DEFINITION = r'''
prog: 'example'
options:
  - option_strings: ['--time']
    complete: ['float', {'suffixes': {'s': 'seconds', 'm': 'minutes', 'h': 'hours'}}]
'''

OUTPUT = r'''
~ > example --time=3.0<TAB>
s -- seconds  m -- minutes  h -- hours
'''

def validate(_ctxt, arguments):
    '''Validate YAML for float completer'''
    _validate.check_float(_ctxt, arguments)


def bash(completer, ctxt, trace, options=None):
    '''Implement float for bash'''
    return completer.complete(ctxt, trace, 'integer', options)


def fish(completer, ctxt, trace, options=None):
    '''Implement float for fish'''
    return completer.complete(ctxt, trace, 'integer', options)


def zsh(_completer, ctxt, _trace, options=None):
    '''Implement float for zsh'''
    args = ['-f']
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
