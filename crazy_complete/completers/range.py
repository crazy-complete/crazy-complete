# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2025-2026 Benjamin Abendroth <braph93@gmx.de>

'''Completer for a range of numbers.'''

from .. import messages as m
from ..bash_complete import BashCompletionCompgen
from ..fish_complete import FishCompletionCommand
from ..zsh_complete import ZshCompletionBase
from ..errors import CrazySchemaValidationError
from ..scheme_validator import check_type

CATEGORY = 'basic'

SYNOPSIS = r'''
['range', <START>, <STOP>]

['range', <START>, <STOP>, <STEP>]
'''

SHORT = 'Complete sequences of integers'

LONG = r'''
`START`:
  The first value of the range.

`STOP`:
  The last value of the range.

`STEP`:
  The increment between values. Defaults to `1`.
'''

DEFINITION = r'''
prog: 'example'
options:
  - option_strings: ['--range-1']
    complete: ['range', 1, 9]

  - option_strings: ['--range-2']
    complete: ['range', 1, 9, 2]
'''

OUTPUT = r'''
~ > example --range-1=<TAB>
1  2  3  4  5  6  7  8  9

~ > example --range-2=<TAB>
1  3  5  7  9
'''

_error = CrazySchemaValidationError


def validate(_ctxt, arguments):
    '''Validate YAML for range completer'''
    start = arguments.get_required_arg("start")
    stop = arguments.get_required_arg("stop")
    step = arguments.get_optional_arg(1)
    arguments.require_no_more()

    check_type(start, (int,), "start")
    check_type(stop, (int,), "stop")
    check_type(step, (int,), "step")

    if step.value == 0:
        msg = '%s: %s' % ('step', m.integer_cannot_be_zero())
        raise _error(msg, step)

    if step.value > 0 and start.value > stop.value:
        msg = f"start > stop: {start.value} > {stop.value} (step={step.value})"
        raise _error(msg, step)

    if step.value < 0 and stop.value > start.value:
        msg = f"stop > start: {stop.value} > {start.value} (step={step.value})"
        raise _error(msg, step)


class ZshCompleteRange(ZshCompletionBase):
    '''Complete a range of integers.'''

    def __init__(self, ctxt, start, stop, step):
        self.ctxt = ctxt
        self.start = start
        self.stop = stop
        self.step = step

    def get_action_string(self):
        if self.step == 1:
            return f"'({{{self.start}..{self.stop}}})'"

        return f"'({{{self.start}..{self.stop}..{self.step}}})'"

    def get_function(self):
        if self.step == 1:
            code = f"command seq {self.start} {self.stop}"
        else:
            code = f"command seq {self.start} {self.step} {self.stop}"

        code = f'compadd -- $({code})'

        funcname = self.ctxt.helpers.add_dynamic_func(self.ctxt, code)
        return funcname


def bash(_completer, ctxt, _trace, start, stop, step=1):
    '''Implement range for bash'''
    if step == 1:
        return BashCompletionCompgen(ctxt, f"-W '{{{start}..{stop}}}'")

    return BashCompletionCompgen(ctxt, f"-W '{{{start}..{stop}..{step}}}'")


def fish(_completer, ctxt, _trace, start, stop, step=1):
    '''Implement range for fish'''
    if step == 1:
        return FishCompletionCommand(ctxt, ['seq', str(start), str(stop)])

    return FishCompletionCommand(ctxt, ['seq', str(start), str(step), str(stop)])


def zsh(_completer, ctxt, _trace, start, stop, step=1):
    '''Implement range for zsh'''
    return ZshCompleteRange(ctxt, start, stop, step)
