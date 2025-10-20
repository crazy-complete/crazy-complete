'''This module contains code for completing arguments in Bash.'''

from . import shell
from .str_utils import indent
from .type_utils import is_dict_type
from .bash_utils import make_file_extension_pattern


# pylint: disable=too-few-public-methods


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


class BashCompletionCommand(BashCompletionBase):
    '''Used for completion functions that internally modify $COMPREPLY.'''

    def __init__(self, ctxt, cmd):
        self.ctxt = ctxt
        self.cmd = cmd

    def get_code(self, append=False):
        if not self.cmd:
            return ''

        r = []

        if append:
            r.append('local COMPREPLY_OLD=("${COMPREPLY[@]}")')

        r.append(self.cmd)

        if append:
            r.append('COMPREPLY=("${COMPREPLY_OLD[@]}" "${COMPREPLY[@]}")')

        return '\n'.join(r)


class CompgenW(BashCompletionBase):
    '''Used for completing a list of words.'''

    def __init__(self, ctxt, values):
        self.ctxt = ctxt
        self.values = values

    def get_code(self, append=False):
        needs_escape = any(shell.needs_escape(str(value)) for value in self.values)

        if needs_escape:
            compgen_funcname = self.ctxt.helpers.use_function('compgen_w_replacement')
            return ('%s %s-- "$cur" %s' % (
                compgen_funcname,
                ('-a ' if append else ''),
                ' '.join(shell.escape(str(s)) for s in self.values)))

        return 'COMPREPLY%s=($(compgen -W %s -- "$cur"))' % (
            ('+' if append else ''),
            shell.escape(' '.join(str(v) for v in self.values)))


class BashCompletionCompgen(BashCompletionBase):
    '''Used for completion that uses Bash's `compgen` command.'''

    def __init__(self, _ctxt, compgen_args, code=None):
        self.compgen_args = compgen_args
        self.code = code

    def get_code(self, append=False):
        compgen_cmd = 'COMPREPLY%s=($(compgen %s -- "$cur"))' % (
            ('+' if append else ''), self.compgen_args)

        if not self.code:
            return compgen_cmd

        return '%s\n%s' % (self.code, compgen_cmd)


class BashCompleteCombine(BashCompletionBase):
    '''Used for combining multiple complete commands.'''

    def __init__(self, ctxt, completer, commands):
        self.completion_objects = []

        for command_args in commands:
            command, *args = command_args
            obj = getattr(completer, command)(ctxt, *args)
            self.completion_objects.append(obj)

    def get_code(self, append=False):
        code = [self.completion_objects[0].get_code(append=append)]
        for obj in self.completion_objects[1:]:
            code.append(obj.get_code(append=True))
        return '\n'.join(code)


class BashCompleter(shell.ShellCompleter):
    '''Code generator for completing arguments in Bash.'''

    # pylint: disable=missing-function-docstring
    # pylint: disable=too-many-public-methods

    def none(self, ctxt, *_):
        return BashCompletionCommand(ctxt, '')

    def integer(self, ctxt, *_):
        return BashCompletionCommand(ctxt, '')

    def float(self, ctxt, *_):
        return BashCompletionCommand(ctxt, '')

    def choices(self, ctxt, choices):
        return CompgenW(ctxt, choices)

    def command(self, ctxt, opts=None):
        code = None
        path = None
        append = None
        prepend = None

        if opts:
            path = opts.get('path', None)
            append = opts.get('path_append', None)
            prepend = opts.get('path_prepend', None)

        if path:
            code = 'local -x PATH=%s' % shell.escape(path)
        elif append and prepend:
            append = shell.escape(append)
            prepend = shell.escape(prepend)
            code = 'local -x PATH=%s:"$PATH":%s' % (prepend, append)
        elif append:
            code = 'local -x PATH="$PATH":%s' % shell.escape(append)
        elif prepend:
            code = 'local -x PATH=%s:"$PATH"' % shell.escape(prepend)

        return BashCompletionCompgen(ctxt, '-A command', code=code)

    def directory(self, ctxt, opts=None):
        directory = None if opts is None else opts.get('directory', None)

        if directory:
            cmd =  'builtin pushd %s &>/dev/null && {\n' % shell.escape(directory)
            cmd += '  _filedir -d\n'
            cmd += '  builtin popd &>/dev/null\n'
            cmd += '}'
            return BashCompletionCommand(ctxt, cmd)

        return BashCompletionCommand(ctxt, '_filedir -d')

    def file(self, ctxt, opts=None):
        directory = None
        extensions = None

        if opts:
            directory = opts.get('directory', None)
            extensions = opts.get('extensions', None)

        if extensions:
            filedir_cmd = '_filedir %s' % make_file_extension_pattern(extensions)
        else:
            filedir_cmd = '_filedir'

        if directory:
            cmd =  'builtin pushd %s &>/dev/null && {\n' % shell.escape(directory)
            cmd += '  %s\n' % filedir_cmd
            cmd += '  builtin popd &>/dev/null\n'
            cmd += '}'
            return BashCompletionCommand(ctxt, cmd)

        return BashCompletionCommand(ctxt, filedir_cmd)

    def mime_file(self, ctxt, pattern):
        funcname = ctxt.helpers.use_function('mime_file')
        return BashCompletionCommand(ctxt, '%s %s' % (funcname, shell.escape(pattern)))

    def group(self, ctxt):
        return BashCompletionCompgen(ctxt, '-A group')

    def hostname(self, ctxt):
        return BashCompletionCompgen(ctxt, '-A hostname')

    def pid(self, ctxt):
        return BashCompletionCommand(ctxt, '_pids')

    def process(self, ctxt):
        return BashCompletionCommand(ctxt, '_pnames')

    def range(self, ctxt, start, stop, step=1):
        if step == 1:
            return BashCompletionCompgen(ctxt, f"-W '{{{start}..{stop}}}'")

        return BashCompletionCompgen(ctxt, f"-W '{{{start}..{stop}..{step}}}'")

    def service(self, ctxt):
        return BashCompletionCompgen(ctxt, '-A service')

    def user(self, ctxt):
        return BashCompletionCompgen(ctxt, '-A user')

    def variable(self, ctxt):
        return BashCompletionCompgen(ctxt, '-A variable')

    def environment(self, ctxt):
        return BashCompletionCompgen(ctxt, '-A export')

    def exec(self, ctxt, command):
        funcname = ctxt.helpers.use_function('exec')
        return BashCompletionCommand(ctxt, '%s %s' % (funcname, shell.escape(command)))

    def exec_fast(self, ctxt, command):
        funcname = ctxt.helpers.use_function('exec_fast')
        return BashCompletionCommand(ctxt, '%s %s' % (funcname, shell.escape(command)))

    def exec_internal(self, ctxt, command):
        return BashCompletionCommand(ctxt, command)

    def value_list(self, ctxt, opts):
        funcname = ctxt.helpers.use_function('value_list')
        separator = opts.get('separator', ',')
        values = opts['values']

        if is_dict_type(values):
            values = list(values.keys())

        return BashCompletionCommand(ctxt, '%s %s %s' % (
            funcname,
            shell.escape(separator),
            ' '.join(shell.escape(v) for v in values)))

    def combine(self, ctxt, commands):
        return BashCompleteCombine(ctxt, self, commands)

    def history(self, ctxt, pattern):
        funcname = ctxt.helpers.use_function('history')
        return BashCompletionCommand(ctxt, '%s %s' % (funcname, shell.escape(pattern)))

    def commandline_string(self, ctxt):
        funcname = ctxt.helpers.use_function('commandline_string')
        return BashCompletionCommand(ctxt, '%s' % funcname)

    def command_arg(self, ctxt):
        return BashCompletionCommand(ctxt, '')

    def date(self, ctxt, _format):
        return BashCompletionCommand(ctxt, '')

    def date_format(self, ctxt):
        return BashCompletionCommand(ctxt, '')

    # =========================================================================
    # Bonus
    # =========================================================================

    def net_interface(self, ctxt):
        exec_func = ctxt.helpers.use_function('exec')
        list_func = ctxt.helpers.use_function('net_interfaces_list')
        return BashCompletionCommand(ctxt, '%s %s' % (exec_func, list_func))

    def timezone(self, ctxt):
        exec_func = ctxt.helpers.use_function('exec')
        list_func = ctxt.helpers.use_function('timezone_list')
        return BashCompletionCommand(ctxt, '%s %s' % (exec_func, list_func))

    def alsa_card(self, ctxt):
        exec_func = ctxt.helpers.use_function('exec')
        list_func = ctxt.helpers.use_function('alsa_list_cards')
        return BashCompletionCommand(ctxt, '%s %s' % (exec_func, list_func))

    def alsa_device(self, ctxt):
        exec_func = ctxt.helpers.use_function('exec')
        list_func = ctxt.helpers.use_function('alsa_list_devices')
        return BashCompletionCommand(ctxt, '%s %s' % (exec_func, list_func))
