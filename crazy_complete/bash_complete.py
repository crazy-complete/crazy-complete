# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2025-2026 Benjamin Abendroth <braph93@gmx.de>

'''This module contains code for completing arguments in Bash.'''

from . import shell


class BashCompletionBase:
    '''Base class for Bash completions.'''

    def get_code(self, append=False):
        '''Returns the code used for completing an argument.

        If `append` is `True`, then the results will be appended to $COMPREPLY,
        otherwise $COMPREPLY will be truncated.

        Args:
            append (bool): If True, the results will be appended to $COMPREPLY.

        Returns:
            str: The command for Bash completion.
        '''
        raise NotImplementedError

    def get_function(self):
        '''Returns a function.'''
        raise NotImplementedError


class BashCompletionCode(BashCompletionBase):
    '''Used for completion code that internally modify $COMPREPLY.'''

    def __init__(self, ctxt, code):
        self.ctxt = ctxt
        self.code = code

    def get_code(self, append=False):
        if not self.code:
            return ''

        r = []

        if append:
            r.append('local COMPREPLY_OLD=("${COMPREPLY[@]}")')

        r.append(self.code)

        if append:
            r.append('COMPREPLY=("${COMPREPLY_OLD[@]}" "${COMPREPLY[@]}")')

        return '\n'.join(r)

    def get_function(self):
        if not self.code:
            return 'true'

        return self.ctxt.helpers.add_dynamic_func(self.ctxt, self.get_code())


class BashCompletionFunc(BashCompletionBase):
    '''Used for completion functions that internally modify $COMPREPLY.'''

    def __init__(self, ctxt, args):
        self.ctxt = ctxt
        self.args = args

    def get_code(self, append=False):
        r = []

        if append:
            r.append('local COMPREPLY_OLD=("${COMPREPLY[@]}")')

        r.append(shell.join_quoted(self.args))

        if append:
            r.append('COMPREPLY=("${COMPREPLY_OLD[@]}" "${COMPREPLY[@]}")')

        return '\n'.join(r)

    def get_function(self):
        if len(self.args) == 1:
            return self.args[0]

        return self.ctxt.helpers.add_dynamic_func(self.ctxt, self.get_code())


class BashCompletionCompgen(BashCompletionBase):
    '''Used for completion that uses Bash's `compgen` command.'''

    def __init__(self, ctxt, compgen_args, code=None):
        self.ctxt = ctxt
        self.compgen_args = compgen_args
        self.code = code

    def get_code(self, append=False):
        compgen_cmd = 'COMPREPLY%s=($(compgen %s -- "$cur"))' % (
            ('+' if append else ''), self.compgen_args)

        if not self.code:
            return compgen_cmd

        return f'{self.code}\n{compgen_cmd}'

    def get_function(self):
        return self.ctxt.helpers.add_dynamic_func(self.ctxt, self.get_code())


class BashCompleter(shell.ShellCompleter):
    '''Code generator for completing arguments in Bash.'''

    SHELL = 'bash'
