'''Shell utility functions.'''

import re
import shlex
import collections

from . import cli
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


def make_completion_funcname(cmdline, prefix='_', suffix=''):
    '''Generates a function name for auto-completing a program or subcommand.

    Args:
        cmdline (CommandLine): The CommandLine instance representing the program or subcommand.
        prefix (str): The prefix that shall be prepended to the result.
        suffix (str): The suffix that shall be appended to the result.

    Returns:
        str: The generated function name for auto-completion.

    This function is used to generate a unique function name for auto-completing
    a program or subcommand in the specified shell. It concatenates the names of
    all parent commandlines, including the current commandline, and converts them
    into a valid function name format.

    Example:
        For a program with the name 'my_program' and a subcommand with the name 'subcommand',
        the generated function name is '_my_program_subcommand'.
    '''
    assert isinstance(cmdline, cli.CommandLine), \
        "make_completion_funcname: cmdline: expected CommandLine, got %r" % cmdline

    commandlines = cmdline.get_parents(include_self=True)
    identifier = make_identifier('_'.join(p.prog for p in commandlines))

    return f'{prefix}{identifier}{suffix}'


class ShellCompleter:
    '''Base class for argument completion.'''

    # pylint: disable=missing-function-docstring

    def complete(self, ctxt, completion, *a):
        if not hasattr(self, completion):
            utils.warn(f"ShellCompleter: Falling back from `{completion}` to `none`")
            completion = 'none'

        return getattr(self, completion)(ctxt, *a)

    def fallback(self, ctxt, from_, to, *a):
        utils.warn(f"ShellCompleter: Falling back from `{from_}` to `{to}`")
        return self.complete(ctxt, to, *a)

    def signal(self, ctxt, prefix=''):
        sig = prefix
        signals = collections.OrderedDict([
            (sig+'ABRT',   'Process abort signal'),
            (sig+'ALRM',   'Alarm clock'),
            (sig+'BUS',    'Access to an undefined portion of a memory object'),
            (sig+'CHLD',   'Child process terminated, stopped, or continued'),
            (sig+'CONT',   'Continue executing, if stopped'),
            (sig+'FPE',    'Erroneous arithmetic operation'),
            (sig+'HUP',    'Hangup'),
            (sig+'ILL',    'Illegal instruction'),
            (sig+'INT',    'Terminal interrupt signal'),
            (sig+'KILL',   'Kill (cannot be caught or ignored)'),
            (sig+'PIPE',   'Write on a pipe with no one to read it'),
            (sig+'QUIT',   'Terminal quit signal'),
            (sig+'SEGV',   'Invalid memory reference'),
            (sig+'STOP',   'Stop executing (cannot be caught or ignored)'),
            (sig+'TERM',   'Termination signal'),
            (sig+'TSTP',   'Terminal stop signal'),
            (sig+'TTIN',   'Background process attempting read'),
            (sig+'TTOU',   'Background process attempting write'),
            (sig+'USR1',   'User-defined signal 1'),
            (sig+'USR2',   'User-defined signal 2'),
            (sig+'POLL',   'Pollable event'),
            (sig+'PROF',   'Profiling timer expired'),
            (sig+'SYS',    'Bad system call'),
            (sig+'TRAP',   'Trace/breakpoint trap'),
            (sig+'XFSZ',   'File size limit exceeded'),
            (sig+'VTALRM', 'Virtual timer expired'),
            (sig+'XCPU',   'CPU time limit exceeded'),
        ])

        return self.complete(ctxt, 'choices', signals)

    def range(self, ctxt, start, stop, step=1):
        return self.fallback(ctxt, 'range', 'choices', list(range(start, stop, step)))

    def directory(self, ctxt, opts):
        return self.fallback(ctxt, 'directory', 'file', opts)

    def command(self, ctxt):
        return self.fallback(ctxt, 'command', 'file')

    # =========================================================================
    # Bonus
    # =========================================================================

    def login_shell(self, ctxt):
        return self.exec(ctxt, "command grep -E '^[^#]' /etc/shells")

    def locale(self, ctxt):
        return self.exec(ctxt, "command locale -a")

    def charset(self, ctxt):
        return self.exec(ctxt, "command locale -m")

    def mountpoint(self, ctxt):
        return self.exec(ctxt, "command mount | command cut -d' ' -f3")
