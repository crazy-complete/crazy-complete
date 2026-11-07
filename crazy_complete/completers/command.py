# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2025-2026 Benjamin Abendroth <braph93@gmx.de>

'''Completer for executable commands.'''

from .. import shell
from .. import messages as m
from ..bash_complete import BashCompletionCompgen
from ..fish_complete import FishCompletionBase
from ..zsh_complete import ZshCompletionBase
from ..errors import CrazySchemaValidationError
from ..scheme_validator import (
    check_type, check_dictionary, check_non_empty_string)

CATEGORY = 'basic'

SYNOPSIS = r'''
['command']

['command', <OPTIONS>]
'''

SHORT = 'Complete command names'

LONG = r'''
This completer provides completion suggestions for executable commands available in the system's `$PATH`.
 
`OPTIONS`:
  A dictionary containing additional options for configuring the completion.

  - `path`:
    Override the default `$PATH` used for searching executables.

  - `path_append`:
    Append directories to the default `$PATH`.

  - `path_prepend`:
    Prepend directories to the default `$PATH`.
'''

NOTES = [
    '`path_append` and `path_prepend` can be used together, but both are mutually exclusive with `path`.',
]

ALSO = {
    'command_arg': 'For completing arguments of a command',
    'commandline_string': 'For completing command lines as strings',
}

DEFINITION = r'''
prog: 'example'
options:
  - option_strings: ['--command']
    complete: ['command']

  - option_strings: ['--command-sbin']
    complete: ['command', {'path_append': '/sbin:/usr/sbin'}]
'''

OUTPUT = r'''
~ > example --command=bas<TAB>
base32    base64    basename  basenc    bash      bashbug
'''

_error = CrazySchemaValidationError


def validate(_ctxt, arguments):
    '''Validate YAML for command completer'''
    opts = arguments.get_optional_arg({})
    check_type(opts, (dict,), 'options')
    arguments.require_no_more()

    check_dictionary(opts, {
        'path':         (False, (str,), check_non_empty_string),
        'path_append':  (False, (str,), check_non_empty_string),
        'path_prepend': (False, (str,), check_non_empty_string),
    })

    path = opts.value.get('path', None)
    append = opts.value.get('path_append', None)
    prepend = opts.value.get('path_prepend', None)

    if path and append:
        msg = m.mutually_exclusive_parameters('path, path_append')
        raise _error(msg, opts)

    if path and prepend:
        msg = m.mutually_exclusive_parameters('path, path_prepend')
        raise _error(msg, opts)


class ZshCompleteCommand(ZshCompletionBase):
    '''Complete a command from $PATH.'''

    def __init__(self, ctxt, opts):
        self.ctxt = ctxt
        self.code = None
        path = None
        append = None
        prepend = None

        if opts:
            path = opts.get('path', None)
            append = opts.get('path_append', None)
            prepend = opts.get('path_prepend', None)

        if path:
            self.code = 'local -x PATH=%s' % shell.quote(path)
        elif append and prepend:
            append = shell.quote(append)
            prepend = shell.quote(prepend)
            self.code = 'local -x PATH=%s:"$PATH":%s' % (prepend, append)
        elif append:
            self.code = 'local -x PATH="$PATH":%s' % shell.quote(append)
        elif prepend:
            self.code = 'local -x PATH=%s:"$PATH"' % shell.quote(prepend)

    def get_action_string(self):
        if not self.code:
            return '_command_names'

        code = f'{self.code}\n_command_names'
        funcname = self.ctxt.helpers.add_dynamic_func(self.ctxt, code)
        return funcname

    def get_function(self):
        if not self.code:
            return '_command_names'

        code = f'{self.code}\n_command_names'
        funcname = self.ctxt.helpers.add_dynamic_func(self.ctxt, code)
        return funcname


class FishCompleteCommand(FishCompletionBase):
    '''Complete a command from $PATH.'''

    def __init__(self, ctxt, opts):
        super().__init__(ctxt)

        code = None
        path = None
        append = None
        prepend = None

        if opts:
            path = opts.get('path', None)
            append = opts.get('path_append', None)
            prepend = opts.get('path_prepend', None)

        def mkpath(path):
            return shell.join_quoted(path.split(':'))

        if path:
            code = 'set -lx PATH %s' % mkpath(path)
        elif append and prepend:
            code = 'set -lx PATH %s $PATH %s' % (mkpath(prepend), mkpath(append))
        elif append:
            code = 'set -lx -a PATH %s' % mkpath(append)
        elif prepend:
            code = 'set -lx PATH %s $PATH' % mkpath(prepend)

        if not code:
            self.code = "__fish_complete_command"
        else:
            self.code = f'{code}\n__fish_complete_command'

    def get_args(self):
        if '\n' in self.code:
            func = self.ctxt.helpers.add_dynamic_func(self.ctxt, self.code)
            return ['-f', '-a', '(%s)' % func]

        return ['-f', '-a', '(%s)' % self.code]

    def get_code(self):
        return self.code


def bash(_completer, ctxt, _trace, opts=None):
    '''Implement command for bash'''
    code = None
    path = None
    append = None
    prepend = None

    if opts:
        path = opts.get('path', None)
        append = opts.get('path_append', None)
        prepend = opts.get('path_prepend', None)

    if path:
        code = 'local -x PATH=%s' % shell.quote(path)
    elif append and prepend:
        append = shell.quote(append)
        prepend = shell.quote(prepend)
        code = 'local -x PATH=%s:"$PATH":%s' % (prepend, append)
    elif append:
        code = 'local -x PATH="$PATH":%s' % shell.quote(append)
    elif prepend:
        code = 'local -x PATH=%s:"$PATH"' % shell.quote(prepend)

    return BashCompletionCompgen(ctxt, '-A command', code=code)


def fish(_completer, ctxt, _trace, opts=None):
    '''Implement command for fish'''
    return FishCompleteCommand(ctxt, opts)


def zsh(_completer, ctxt, _trace, opts=None):
    '''Implement command for zsh'''
    return ZshCompleteCommand(ctxt, opts)
