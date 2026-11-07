# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2025-2026 Benjamin Abendroth <braph93@gmx.de>

'''Completer for dates.'''

from ..bash_complete import BashCompletionCode
from ..fish_complete import FishCompleteNone
from ..zsh_complete import ZshComplFunc
from ..scheme_validator import check_type, check_non_empty_string

CATEGORY = 'basic'

SYNOPSIS = r'''
['date', <FORMAT>]
'''

SHORT = 'Complete date strings'

LONG = r'''
`FORMAT`:
  The date format as described in `strftime(3)`.
'''

ALSO = {
    'date_format': 'For completing date format strings',
}

IMPLEMENTED = [
    'Zsh',
]

DEFINITION = r'''
prog: 'example'
options:
  - option_strings: ['--date']
    complete: ['date', '%Y-%m-%d']
'''

OUTPUT = r'''
~ > example --date=<TAB>

         November
Mo  Tu  We  Th  Fr  Sa  Su
     1   2   3   4   5   6
 7   8   9  10  11  12  13
14  15  16  17  18  19  20
21  22  23  24  25  26  27
28  29  30
'''

def validate(_ctxt, arguments):
    '''Validate YAML for date completer'''
    format_ = arguments.get_required_arg("format")
    check_type(format_, (str,), "format")
    arguments.require_no_more()
    check_non_empty_string(format_, 'format')


def bash(_completer, ctxt, _trace, _format):
    '''Implement date for bash'''
    return BashCompletionCode(ctxt, '')


def fish(_completer, ctxt, _trace, _format):
    '''Implement date for fish'''
    return FishCompleteNone(ctxt)


def zsh(_completer, ctxt, _trace, format_):
    '''Implement date for zsh'''
    return ZshComplFunc(ctxt, ['_dates', '-f', format_])
