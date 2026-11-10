# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2025-2026 Benjamin Abendroth <braph93@gmx.de>

'''Completer for shell job specifications.'''

from ..bash_complete import BashCompletionCompgen
from ..fish_complete import FishCompletionCommand
from ..zsh_complete import ZshComplFunc

CATEGORY = 'basic'

SHORT = "Complete the current shell's jobs"

DEFINITION = r'''
prog: 'example'
options:
  - option_strings: ['--job']
    complete: ['jobs']
'''

OUTPUT = r'''
~ > example --job=<TAB>
%1  %2  %3
'''


def validate(_ctxt, arguments):
    '''Validate YAML for jobs completer'''
    arguments.require_no_more()


def bash(_completer, ctxt, _trace):
    '''Implement jobs for bash'''
    # `jobs` must run in the interactive shell (it only knows that shell's own
    # jobs), so we feed its table into `compgen -W` instead of delegating to a
    # subprocess. The space separator suits `compgen -W`, while `-- "$cur"`
    # filters the candidates by prefix.
    awk = r'{n=$1; gsub(/[^0-9]/,"",n); if(n!="") printf "%%%s ",n}'
    args = "-W \"$(jobs | awk '%s')\"" % awk
    return BashCompletionCompgen(ctxt, args)


def fish(completer, ctxt, trace):
    '''Implement jobs for fish'''
    return FishCompletionCommand(ctxt, ["__fish_complete_job_pids"])


def zsh(completer, ctxt, trace):
    '''Implement jobs for zsh'''
    return ZshComplFunc(ctxt, ['_jobs'])
