'''Shell utility functions.'''

import re
import shlex

from . import utils


def make_identifier(string):
    '''Make `string` a valid shell identifier.

    This function replaces any dashes '-' with underscores '_',
    removes any characters that are not letters, digits, or underscores,
    and ensures that consecutive underscores are replaced with a single underscore.

    Args:
        string (str): The input string to be converted into a valid shell identifier.

    Returns:
        str: The modified string that is a valid shell identifier.
    '''

    string = string.replace('-', '_')
    string = re.sub('[^a-zA-Z0-9_]', '', string)
    string = re.sub('_+', '_', string)
    if string and string[0] in '0123456789':
        return '_' + string
    return string


def needs_escape(string):
    '''Return if string needs escaping.'''

    return not re.fullmatch('[a-zA-Z0-9_@%+=:,./-]+', string)


def escape(string, escape_empty_string=True):
    '''Escapes special characters in a string for safe usage in shell commands or scripts.

    Args:
        string (str): The input string to be escaped.
        escape_empty_string (bool, optional): Determines whether to escape an empty string or not.
            Defaults to True.

    Returns:
        str: The escaped string.
    '''

    if not string and not escape_empty_string:
        return ''

    if not needs_escape(string):
        return string

    if "'" not in string:
        return "'%s'" % string

    if '"' not in string:
        return '"%s"' % string.replace('\\', '\\\\').replace('$', '\\$').replace('`', '\\`')

    return "'%s'" % string.replace("'", '\'"\'"\'')


def unescape(string):
    '''Unescapes a string.'''

    return ''.join(shlex.split(string, posix=True))


class ShellCompleter:
    '''Base class for argument completion.'''

    # pylint: disable=missing-function-docstring
    # pylint: disable=too-many-arguments
    # pylint: disable=too-many-positional-arguments

    def complete(self, ctxt, trace, command, *a):
        if not hasattr(self, command):
            utils.warn(f"ShellCompleter: Falling back from `{command}` to `none`")
            command = 'none'

        return getattr(self, command)(ctxt, trace, *a)

    def complete_from_def(self, ctxt, trace, definition):
        command, *args = definition
        return self.complete(ctxt, trace, command, *args)

    def fallback(self, ctxt, trace, from_, to, *a):
        utils.warn(f"ShellCompleter: Falling back from `{from_}` to `{to}`")
        return self.complete(ctxt, trace, to, *a)

    def signal(self, ctxt, trace):
        signals = {
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

        return self.complete(ctxt, trace, 'choices', signals)

    def range(self, ctxt, trace, start, stop, step=1):
        return self.fallback(ctxt, trace, 'range', 'choices', list(range(start, stop, step)))

    def directory(self, ctxt, trace, opts):
        return self.fallback(ctxt, trace, 'directory', 'file', opts)

    def command(self, ctxt, trace):
        return self.fallback(ctxt, trace, 'command', 'file')

    def exec(self, _ctxt, _trace, _command):
        raise NotImplementedError

    def list(self, _ctxt, _trace, _command, _opts=None):
        raise NotImplementedError

    # =========================================================================
    # Aliases
    # =========================================================================

    def file_list(self, ctxt, trace, opts=None):
        list_opts = {
            'separator': opts.pop('separator', ',') if opts else ',',
            'duplicates': opts.pop('duplicates', False) if opts else False
        }

        return self.list(ctxt, trace, ['file', opts], list_opts)

    def directory_list(self, ctxt, trace, opts=None):
        list_opts = {
            'separator': opts.pop('separator', ',') if opts else ',',
            'duplicates': opts.pop('duplicates', False) if opts else False
        }

        return self.list(ctxt, trace, ['directory', opts], list_opts)

    # =========================================================================
    # Bonus
    # =========================================================================

    def login_shell(self, ctxt, trace):
        return self.exec(ctxt, trace, "command grep -E '^[^#]' /etc/shells")

    def locale(self, ctxt, trace):
        return self.exec(ctxt, trace, "command locale -a")

    def charset(self, ctxt, trace):
        return self.exec(ctxt, trace, "command locale -m")

    def mountpoint(self, ctxt, trace):
        return self.exec(ctxt, trace, "command mount | command cut -d' ' -f3")
