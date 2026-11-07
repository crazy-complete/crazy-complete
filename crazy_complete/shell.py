# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2025-2026 Benjamin Abendroth <braph93@gmx.de>

'''Shell utility functions.'''

import re

from . import completers
from . import utils


def make_identifier(string):
    '''Make `string` a valid shell identifier.

    This function replaces any dashes '-' with underscores '_',
    removes any characters that are not letters, digits, or underscores,
    and ensures that consecutive underscores are replaced with a single
    underscore.

    Args:
        string (str):
            The input string to be converted into a valid shell identifier.

    Returns:
        str: The modified string that is a valid shell identifier.
    '''

    string = string.replace('-', '_')
    string = re.sub('[^a-zA-Z0-9_]', '', string)
    string = re.sub('_+', '_', string)
    if string and string[0] in '0123456789':
        return '_' + string
    return string


def needs_quote(string):
    '''Return if string needs quoting.'''

    return not re.fullmatch('[a-zA-Z0-9_@%+=:,./-]+', string)


def quote(string, quote_empty_string=True):
    '''Quotes a string for safe usage in shell commands or scripts.

    Args:
        string (str):
            The input string to be quoted.

        quote_empty_string (bool, optional):
            Determines whether to quote an empty string or not.
            Defaults to True.

    Returns:
        str: The quoted string.
    '''

    if not string and not quote_empty_string:
        return ''

    if not needs_quote(string):
        return string

    if "'" not in string:
        return f"'{string}'"

    if '"' not in string:
        s = string
        s = s.replace('\\', '\\\\')
        s = s.replace('$', '\\$')
        s = s.replace('`', '\\`')
        return f'"{s}"'

    s = string.replace("'", '\'"\'"\'')
    return f"'{s}'"


def join_quoted(arguments, string=' '):
    '''Joins quoted `arguments` on `string`.'''

    return string.join(quote(arg) for arg in arguments)


def _load_plugin(completer, name):
    '''Try to load `name` from the `completers` package.

    Returns:
        The generation function for the shell of `completer`,
        or `None` if no such plugin exists.
    '''

    shell_name = getattr(completer, 'SHELL', None)

    if shell_name is None:
        return None

    try:
        module = completers.load(name)
    except ImportError:
        return None

    func = getattr(module, shell_name, None)

    if not callable(func):
        return None

    return func


class ShellCompleter:
    '''Base class for argument completion.'''

    # pylint: disable=missing-function-docstring
    # pylint: disable=too-many-arguments
    # pylint: disable=too-many-positional-arguments

    def complete(self, ctxt, trace, command, *a):
        if hasattr(self, command):
            return getattr(self, command)(ctxt, trace, *a)

        func = _load_plugin(self, command)

        if func is not None:
            return func(self, ctxt, trace, *a)

        utils.warn(f"complete: Falling back from `{command}` to `none`")
        return self.complete(ctxt, trace, 'none', *a)

    def complete_from_def(self, ctxt, trace, definition):
        command, *args = definition
        return self.complete(ctxt, trace, command, *args)

    def fallback(self, ctxt, trace, from_, to, *a):
        utils.warn(f"ShellCompleter: Falling back from `{from_}` to `{to}`")
        return self.complete(ctxt, trace, to, *a)
