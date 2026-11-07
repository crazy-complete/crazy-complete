# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2025-2026 Benjamin Abendroth <braph93@gmx.de>

'''This module contains code for completing arguments in Zsh.'''

from . import shell


class ZshCompletionBase:
    '''Base class for Zsh completions.'''

    def get_action_string(self):
        '''Return an action string that can be used in an option spec.'''
        raise NotImplementedError

    def get_function(self):
        '''Return a function that can be used in e.g. `_sequence`.'''
        raise NotImplementedError


class ZshComplFunc(ZshCompletionBase):
    '''Complete using a function.'''

    def __init__(self, ctxt, args, needs_braces=False):
        self.ctxt = ctxt
        self.args = args
        self.needs_braces = needs_braces

    def get_action_string(self):
        if len(self.args) == 1:
            cmd = self.args[0]
        else:
            cmd = shell.join_quoted(self.args)

        if self.needs_braces:
            return shell.quote(f'{{{cmd}}}')

        return shell.quote(cmd)

    def get_function(self):
        if len(self.args) == 1:
            return self.args[0]

        code = shell.join_quoted(self.args)
        funcname = self.ctxt.helpers.add_dynamic_func(self.ctxt, code)
        return funcname


class ZshCompleter(shell.ShellCompleter):
    '''Code generator for completing arguments in Zsh.'''

    SHELL = 'zsh'
