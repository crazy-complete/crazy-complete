# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2025-2026 Benjamin Abendroth <braph93@gmx.de>

'''This module contains code for completing arguments in Fish.'''

from . import shell


class FishCompletionBase:
    '''Base class for Fish completions.'''

    def __init__(self, ctxt):
        self.ctxt = ctxt

    def get_args(self):
        '''Return a list of arguments to be appended to the `complete`
        command in Fish.

        The returned arguments should be in raw form, without any escaping.
        Escaping will be handled at a later stage.
        '''
        raise NotImplementedError

    def get_code(self):
        '''Return the code that can be used for completing an argument.'''
        raise NotImplementedError

    def get_function(self):
        '''Return a function that runs the code.'''
        func = self.ctxt.helpers.add_dynamic_func(self.ctxt, self.get_code())
        return func


class FishCompleteNone(FishCompletionBase):
    '''Class for completing an argument without a completer.'''

    def get_args(self):
        return ['-f']

    def get_code(self):
        return ''

    def get_function(self):
        return 'true'


class FishCompletionCommand(FishCompletionBase):
    '''Class for executing a command.'''

    def __init__(self, ctxt, args):
        super().__init__(ctxt)
        self.args = args

    def get_code(self):
        return shell.join_quoted(self.args)

    def get_args(self):
        command = shell.join_quoted(self.args)
        return ['-f', '-a', '(%s)' % command]

    def get_function(self):
        if len(self.args) == 1:
            return self.args[0]

        func = self.ctxt.helpers.add_dynamic_func(self.ctxt, self.get_code())
        return func


class FishCompletionRawCommand(FishCompletionBase):
    '''Class for executing a command (without any escaping)'''

    def __init__(self, ctxt, command):
        super().__init__(ctxt)
        self.command = command

    def get_code(self):
        return self.command

    def get_args(self):
        return ['-f', '-a', '(%s)' % self.command]


class FishCompleteCommandArg(FishCompletionBase):
    '''Complete an argument of a command'''

    def __init__(self, ctxt):
        super().__init__(ctxt)

        ctxt.helpers.use_function('query_init', 'positional_position')
        pos_pos_func = ctxt.helpers.use_function('positional_position')
        command_pos = ctxt.option.get_positional_num() - 1

        r = 'set -l pos (%s %d)\n' % (pos_pos_func, command_pos)
        r += 'set -l cmdline (commandline -poc | string escape) (commandline -ct)\n'
        r += 'complete -C -- "$cmdline[$pos..]"'

        self.code = r

    def get_code(self):
        return self.code

    def get_args(self):
        func = self.ctxt.helpers.add_dynamic_func(self.ctxt, self.code)
        return ['-f', '-a', '(%s)' % func]

    def get_function(self):
        func = self.ctxt.helpers.add_dynamic_func(self.ctxt, self.code)
        return func


class FishCompleter(shell.ShellCompleter):
    '''Code generator for completing arguments in Fish.'''

    SHELL = 'fish'
