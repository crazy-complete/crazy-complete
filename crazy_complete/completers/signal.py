# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2025-2026 Benjamin Abendroth <braph93@gmx.de>

'''Completer for signals.'''

from .. import bash_versions
from ..bash_complete import BashCompletionFunc
from ..zsh_complete import ZshComplFunc

CATEGORY = 'basic'

SHORT = 'Complete signal names'

DEFINITION = r'''
prog: 'example'
options:
  - option_strings: ['--signal']
    complete: ['signal']
'''

OUTPUT = r'''
~ > example --signal=<TAB>
ABRT    -- Process abort signal
ALRM    -- Alarm clock
BUS     -- Access to an undefined portion of a memory object
CHLD    -- Child process terminated, stopped, or continued
CONT    -- Continue executing, if stopped
FPE     -- Erroneous arithmetic operation
HUP     -- Hangup
ILL     -- Illegal instruction
INT     -- Terminal interrupt signal
[...]
'''

_SIGNALS = {
    'ABRT':   'Process abort signal',
    'ALRM':   'Alarm clock',
    'BUS':    'Access to an undefined portion of a memory object',
    'CHLD':   'Child process terminated: stopped: or continued',
    'CONT':   'Continue executing: if stopped',
    'FPE':    'Erroneous arithmetic operation',
    'HUP':    'Hangup',
    'ILL':    'Illegal instruction',
    'INT':    'Terminal interrupt signal',
    'KILL':   'Kill (cannot be caught or ignored)',
    'PIPE':   'Write on a pipe with no one to read it',
    'QUIT':   'Terminal quit signal',
    'SEGV':   'Invalid memory reference',
    'STOP':   'Stop executing (cannot be caught or ignored)',
    'TERM':   'Termination signal',
    'TSTP':   'Terminal stop signal',
    'TTIN':   'Background process attempting read',
    'TTOU':   'Background process attempting write',
    'USR1':   'User-defined signal 1',
    'USR2':   'User-defined signal 2',
    'POLL':   'Pollable event',
    'PROF':   'Profiling timer expired',
    'SYS':    'Bad system call',
    'TRAP':   'Trace/breakpoint trap',
    'XFSZ':   'File size limit exceeded',
    'VTALRM': 'Virtual timer expired',
    'XCPU':   'CPU time limit exceeded',
}


def validate(_ctxt, arguments):
    '''Validate YAML for signal completer'''
    arguments.require_no_more()


def bash(_completer, ctxt, _trace):
    '''Implement signal for bash'''
    return BashCompletionFunc(ctxt, [bash_versions.signals(ctxt)])


def fish(completer, ctxt, trace):
    '''Implement signal for fish'''
    return completer.complete(ctxt, trace, 'choices', _SIGNALS)


def zsh(_completer, ctxt, _trace):
    '''Implement signal for zsh'''
    return ZshComplFunc(ctxt, ['_signals'])
