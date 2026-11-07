# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2025-2026 Benjamin Abendroth <braph93@gmx.de>

'''Completer that combines several completers.'''

from .. import messages as m
from .. import shell
from ..bash_complete import BashCompletionBase
from ..errors import CrazySchemaValidationError
from ..fish_complete import FishCompletionBase
from ..scheme_validator import (
    check_type, check_non_empty_list, check_complete)
from ..str_utils import indent
from ..zsh_complete import ZshCompletionBase

SYNOPSIS = r'''
['combine', <COMPLETERS>]
'''

CATEGORY = 'meta'

SHORT = 'Combine multiple completers'

LONG = r'''
Combines multiple completers into a single completer.

`COMPLETERS`:
  A list of completers to combine.
'''

DEFINITION = r'''
prog: 'example'
options:
  - option_strings: ['--combine']
    complete: ['combine', [['user'], ['pid']]]
'''

OUTPUT = r'''
~ > example --combine=avahi,daemon,<TAB>
1439404  3488332  3571716           3607235                 4134206
alpm     avahi    bin               braph                   daemon
root     rtkit    systemd-coredump  systemd-journal-remote  systemd-network
[...]
'''

_error = CrazySchemaValidationError


def validate(ctxt, arguments):
    '''Validate YAML for combine completer'''
    commands = arguments.get_required_arg('commands')
    arguments.require_no_more()

    check_type(commands, (list,), 'commands')
    check_non_empty_list(commands, 'commands')

    if len(commands.value) == 1:
        msg = '%s: %s' % ('commands', m.list_must_contain_at_least_n_items('2'))
        raise _error(msg, commands)

    ctxt.trace.append('combine')

    for i, completer in enumerate(commands.value):
        check_type(completer, (list,), f'command[{i}]')
        check_complete(ctxt, completer)


class BashCompleteCombine(BashCompletionBase):
    '''Used for combining multiple completion commands.'''

    def __init__(self, ctxt, trace, completer, commands):
        self.ctxt = ctxt
        self.completion_objects = []

        for command_args in commands:
            obj = completer.complete_from_def(ctxt, trace, command_args)
            self.completion_objects.append(obj)

    def get_code(self, append=False):
        code = [self.completion_objects[0].get_code(append=append)]
        for obj in self.completion_objects[1:]:
            code.append(obj.get_code(append=True))
        return '\n'.join(code)

    def get_function(self):
        return self.ctxt.helpers.add_dynamic_func(self.ctxt, self.get_code())


class FishCompleteCombine(FishCompletionBase):
    '''Used for combining multiple complete commands.'''

    def __init__(self, ctxt, trace, completer, commands):
        super().__init__(ctxt)

        self.code = []
        trace.append('combine')

        for command in commands:
            obj = completer.complete_from_def(ctxt, trace, command)
            self.code.append(obj.get_code())

    def get_code(self):
        return '\n'.join(self.code)

    def get_args(self):
        code_is_singleline = not any('\n' in code for code in self.code)

        if code_is_singleline:
            return ['-f', '-a', '(%s)' % '; '.join(self.code)]

        code = '\n'.join(self.code)
        func = self.ctxt.helpers.add_dynamic_func(self.ctxt, code)
        return ['-f', '-a', '(%s)' % func]


class ZshCompleteCombine(ZshCompletionBase):
    '''Combine multiple completers into one.'''

    def __init__(self, ctxt, trace, completer, commands):
        trace.append('combine')

        completions = []
        for command_args in commands:
            compl_obj = completer.complete_from_def(ctxt, trace, command_args)
            action_string = compl_obj.get_action_string()
            completions.append(f'::{action_string}')

        code = '_alternative \\\n'
        code += indent(' \\\n'.join(completions), 2)

        self.func = ctxt.helpers.add_dynamic_func(ctxt, code)

    def get_function(self):
        return self.func

    def get_action_string(self):
        return shell.quote('{%s}' % self.func)


def bash(completer, ctxt, trace, commands):
    '''Implement combine for bash'''
    return BashCompleteCombine(ctxt, trace, completer, commands)


def fish(completer, ctxt, trace, commands):
    '''Implement combine for fish'''
    return FishCompleteCombine(ctxt, trace, completer, commands)


def zsh(completer, ctxt, trace, commands):
    '''Implement combine for zsh'''
    return ZshCompleteCombine(ctxt, trace, completer, commands)
