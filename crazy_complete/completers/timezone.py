# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2025-2026 Benjamin Abendroth <braph93@gmx.de>

'''Completer for time zones.'''

from ..bash_complete import BashCompletionFunc
from ..fish_complete import FishCompletionCommand
from ..zsh_complete import ZshComplFunc
from ..helpers import ShellFunction
from ..helpers import FishFunction
from ..bash_helpers import BashHelpers
from ..fish_helpers import FishHelpers

CATEGORY = 'basic'

SHORT = 'Complete timezones'

DEFINITION = r'''
prog: 'example'
options:
  - option_strings: ['--timezone']
    complete: ['timezone']
'''

OUTPUT = r'''
~ > example --timezone=Europe/B<TAB>
Belfast     Belgrade    Berlin      Bratislava
Brussels    Bucharest   Budapest    Busingen
'''

_TIMEZONE_LIST_BASH = ShellFunction('timezone_list', r'''
if ! command timedatectl list-timezones 2>/dev/null; then
  command find /usr/share/zoneinfo -type f |\
  command sed 's|/usr/share/zoneinfo/||g'  |\
  command grep -E -v '^(posix|right)'
fi''')

_TIMEZONE_LIST_FISH = FishFunction('timezone_list', r'''
if ! command timedatectl list-timezones 2>/dev/null
  command find /usr/share/zoneinfo -type f |\
  command sed 's|/usr/share/zoneinfo/||g'  |\
  command grep -E -v '^(posix|right)'
end
''')

BashHelpers.add_function(_TIMEZONE_LIST_BASH)
FishHelpers.add_function(_TIMEZONE_LIST_FISH)


def validate(_ctxt, arguments):
    '''Validate YAML for timezone completer'''
    arguments.require_no_more()


def bash(_completer, ctxt, _trace):
    '''Implement timezone for bash'''
    exec_func = ctxt.helpers.use_function('exec')
    list_func = ctxt.helpers.use_function('timezone_list')
    return BashCompletionFunc(ctxt, [exec_func, list_func])


def fish(_completer, ctxt, _trace):
    '''Implement timezone for fish'''
    func = ctxt.helpers.use_function('timezone_list')
    return FishCompletionCommand(ctxt, [func])


def zsh(_completer, ctxt, _trace):
    '''Implement timezone for zsh'''
    return ZshComplFunc(ctxt, ['_time_zone'])
