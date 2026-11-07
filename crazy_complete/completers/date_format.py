# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2025-2026 Benjamin Abendroth <braph93@gmx.de>

'''Completer for date formats.'''

from ..bash_complete import BashCompletionCode
from ..fish_complete import FishCompletionCommand
from ..zsh_complete import ZshComplFunc
from ..helpers import FishFunction
from ..fish_helpers import FishHelpers

CATEGORY = 'basic'

SHORT = 'Complete date format strings'

ALSO = {
    'date': 'For completing dates',
}

IMPLEMENTED = [
    'Fish',
    'Zsh',
]

DEFINITION = r'''
prog: 'example'
options:
  - option_strings: ['--date-format']
    complete: ['date_format']
'''

OUTPUT = r'''
~ > example --date-format '%<TAB>
a     -- abbreviated day name
A     -- full day name
B     -- full month name
c     -- preferred locale date and time
C     -- 2-digit century
d     -- day of month (01-31)
D     -- American format month/day/year (%m/%d/%y)
e     -- day of month ( 1-31)
[...]
'''

_DATE_FORMAT_FISH = FishFunction('date_format', r'''
set -l comp (get_completing_arg)

if test "$(string sub -s -1 -l 1 -- $comp)" = '%'
  printf '%s%s\t%s\n' \
    "$comp" 'a' 'abbreviated day name' \
    "$comp" 'A' 'full day name' \
    "$comp" 'b' 'abbreviated month name' \
    "$comp" 'h' 'abbreviated month name' \
    "$comp" 'B' 'full month name' \
    "$comp" 'c' 'preferred locale date and time' \
    "$comp" 'C' '2-digit century' \
    "$comp" 'd' 'day of month (01-31)' \
    "$comp" 'D' 'American format month/day/year (%m/%d/%y)' \
    "$comp" 'e' 'day of month ( 1-31)' \
    "$comp" 'F' 'ISO 8601 year-month-date (%Y-%m-%d)' \
    "$comp" 'G' '4-digit ISO 8601 week-based year' \
    "$comp" 'g' '2-digit ISO 8601 week-based year' \
    "$comp" 'H' 'hour (00-23)' \
    "$comp" 'I' 'hour (01-12)' \
    "$comp" 'j' 'day of year (001-366)' \
    "$comp" 'k' 'hour ( 0-23)' \
    "$comp" 'l' 'hour ( 1-12)' \
    "$comp" 'm' 'month (01-12)' \
    "$comp" 'M' 'minute (00-59)' \
    "$comp" 'n' 'newline' \
    "$comp" 'p' 'locale dependent AM/PM' \
    "$comp" 'r' 'locale dependent a.m. or p.m. time (%I:%M:%S %p)' \
    "$comp" 'R' '24-hour notation time (%H:%M)' \
    "$comp" 's' 'seconds since the epoch' \
    "$comp" 'S' 'seconds (00-60)' \
    "$comp" 't' 'tab' \
    "$comp" 'T' '24-hour notation with seconds (%H:%M:%S)' \
    "$comp" 'u' 'day of week (1-7, 1=Monday)' \
    "$comp" 'U' 'week number of current year, Sunday based (00-53)' \
    "$comp" 'V' 'ISO 8601 week number of current year, week 1 has 4 days in current year (01-53)' \
    "$comp" 'w' 'day of week (0-6, 0=Sunday)' \
    "$comp" 'W' 'week number of current year, Monday based (00-53)' \
    "$comp" 'x' 'locale dependent date representation without time' \
    "$comp" 'X' 'locale dependent time representation without date' \
    "$comp" 'y' '2-digit year (00-99)' \
    "$comp" 'Y' 'full year' \
    "$comp" 'z' 'UTC offset' \
    "$comp" 'Z' 'timezone name' \
    "$comp" '%' 'literal %'
end
''', ['get_completing_arg'])

FishHelpers.add_function(_DATE_FORMAT_FISH)


def validate(_ctxt, arguments):
    '''Validate YAML for date_format completer'''
    arguments.require_no_more()


def bash(_completer, ctxt, _trace):
    '''Implement date_format for bash'''
    return BashCompletionCode(ctxt, '')


def fish(_completer, ctxt, _trace):
    '''Implement date_format for fish'''
    func = ctxt.helpers.use_function('date_format')
    return FishCompletionCommand(ctxt, [func])


def zsh(_completer, ctxt, _trace):
    '''Implement date_format for zsh'''
    return ZshComplFunc(ctxt, ['_date_formats'])
