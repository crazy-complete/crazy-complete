'''This module contains code for completing arguments in Bash.'''

from . import shell
from . import bash_versions
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
        self.values = [str(value) for value in values]

    def get_code(self, append=False):
        needs_escape = any(filter(shell.needs_escape, self.values))

        if not needs_escape:
            return 'COMPREPLY%s=($(compgen -W %s -- "$cur"))' % (
                ('+' if append else ''),
                shell.escape(' '.join(self.values)))

        return ('%s %s-- "$cur" %s' % (
            self.ctxt.helpers.use_function('compgen_w_replacement'),
            ('-a ' if append else ''),
            ' '.join(shell.escape(s) for s in self.values)))


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

    def __init__(self, ctxt, trace, completer, commands):
        self.completion_objects = []

        for command_args in commands:
            command, *args = command_args
            obj = getattr(completer, command)(ctxt, trace, *args)
            self.completion_objects.append(obj)

    def get_code(self, append=False):
        code = [self.completion_objects[0].get_code(append=append)]
        for obj in self.completion_objects[1:]:
            code.append(obj.get_code(append=True))
        return '\n'.join(code)


class BashCompleteKeyValueList(BashCompletionCommand):
    '''Used for completing a list of key-value pairs.'''

    def __init__(self, ctxt, trace, completer, pair_separator, value_separator, values):
        funcs = {}

        for key, complete in values.items():
            if not complete:
                funcs[key] = 'false'
            elif complete[0] == 'none':
                funcs[key] = 'true'
            else:
                command, *args = complete
                obj = getattr(completer, command)(ctxt, trace, *args)
                code = obj.get_code()
                funcs[key] = ctxt.helpers.add_dynamic_func(ctxt, code)

        e = shell.escape
        args = ' \\\n'.join('%s %s' % (e(k), e(f)) for k, f in funcs.items())

        code = '%s %s %s \\\n%s' % (
            ctxt.helpers.use_function('key_value_list'),
            shell.escape(pair_separator),
            shell.escape(value_separator),
            indent(args, 2)
        )

        super().__init__(ctxt, code)


class BashCompleter(shell.ShellCompleter):
    '''Code generator for completing arguments in Bash.'''

    # pylint: disable=missing-function-docstring
    # pylint: disable=too-many-public-methods

    def none(self, ctxt, _trace, *_):
        return BashCompletionCommand(ctxt, '')

    def integer(self, ctxt, _trace, *_):
        return BashCompletionCommand(ctxt, '')

    def float(self, ctxt, _trace, *_):
        return BashCompletionCommand(ctxt, '')

    def choices(self, ctxt, _trace, choices):
        return CompgenW(ctxt, choices)

    def command(self, ctxt, _trace, opts=None):
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

    def directory(self, ctxt, _trace, opts=None):
        directory = None if opts is None else opts.get('directory', None)
        filedir = bash_versions.filedir(ctxt)

        if directory:
            cmd =  'builtin pushd %s &>/dev/null && {\n' % shell.escape(directory)
            cmd += '  %s -d\n' % filedir
            cmd += '  builtin popd &>/dev/null\n'
            cmd += '}'
            return BashCompletionCommand(ctxt, cmd)

        return BashCompletionCommand(ctxt, '%s -d' % filedir)

    def file(self, ctxt, _trace, opts=None):
        fuzzy = False
        directory = None
        extensions = None

        if opts:
            fuzzy = opts.get('fuzzy', False)
            directory = opts.get('directory', None)
            extensions = opts.get('extensions', None)

        if extensions:
            filedir_cmd = '%s %s' % (
                bash_versions.filedir(ctxt),
                make_file_extension_pattern(extensions, fuzzy))
        else:
            filedir_cmd = bash_versions.filedir(ctxt)

        if directory:
            cmd =  'builtin pushd %s &>/dev/null && {\n' % shell.escape(directory)
            cmd += '  %s\n' % filedir_cmd
            cmd += '  builtin popd &>/dev/null\n'
            cmd += '}'
            return BashCompletionCommand(ctxt, cmd)

        return BashCompletionCommand(ctxt, filedir_cmd)

    def mime_file(self, ctxt, _trace, pattern):
        funcname = ctxt.helpers.use_function('mime_file')
        return BashCompletionCommand(ctxt, '%s %s' % (funcname, shell.escape(pattern)))

    def group(self, ctxt, _trace):
        return BashCompletionCompgen(ctxt, '-A group')

    def hostname(self, ctxt, _trace):
        return BashCompletionCompgen(ctxt, '-A hostname')

    def pid(self, ctxt, _trace):
        return BashCompletionCommand(ctxt, bash_versions.pids(ctxt))

    def process(self, ctxt, _trace):
        return BashCompletionCommand(ctxt, bash_versions.pnames(ctxt))

    def range(self, ctxt, _trace, start, stop, step=1):
        if step == 1:
            return BashCompletionCompgen(ctxt, f"-W '{{{start}..{stop}}}'")

        return BashCompletionCompgen(ctxt, f"-W '{{{start}..{stop}..{step}}}'")

    def service(self, ctxt, _trace):
        return BashCompletionCompgen(ctxt, '-A service')

    def user(self, ctxt, _trace):
        return BashCompletionCompgen(ctxt, '-A user')

    def variable(self, ctxt, _trace):
        return BashCompletionCompgen(ctxt, '-A variable')

    def environment(self, ctxt, _trace):
        return BashCompletionCompgen(ctxt, '-A export')

    def exec(self, ctxt, _trace, command):
        func = ctxt.helpers.use_function('exec')
        return BashCompletionCommand(ctxt, '%s %s' % (func, shell.escape(command)))

    def exec_fast(self, ctxt, _trace, command):
        func = ctxt.helpers.use_function('exec_fast')
        return BashCompletionCommand(ctxt, '%s %s' % (func, shell.escape(command)))

    def exec_internal(self, ctxt, _trace, command):
        return BashCompletionCommand(ctxt, command)

    def value_list(self, ctxt, _trace, opts):
        funcname = ctxt.helpers.use_function('value_list')
        separator = opts.get('separator', ',')
        duplicates = opts.get('duplicates', False)
        values = opts['values']

        if is_dict_type(values):
            values = list(values.keys())

        return BashCompletionCommand(ctxt, '%s%s %s %s' % (
            funcname,
            ' -d' if duplicates else '',
            shell.escape(separator),
            ' '.join(shell.escape(v) for v in values)))

    def key_value_list(self, ctxt, trace, pair_separator, value_separator, values):
        return BashCompleteKeyValueList(ctxt, trace, self, pair_separator, value_separator, values)

    def combine(self, ctxt, trace, commands):
        return BashCompleteCombine(ctxt, trace, self, commands)

    def list(self, ctxt, trace, command, opts=None):
        separator = opts.get('separator', ',') if opts else ','
        duplicates = opts.get('duplicates', False) if opts else False

        cmd, *args = command
        obj = getattr(self, cmd)(ctxt, trace, *args)
        code = obj.get_code()

        funcname = ctxt.helpers.use_function('value_list')
        dup_arg = ' -d' if duplicates else ''

        r =  'local cur_old="$cur"\n'
        r += 'cur="${cur##*%s}"\n' % shell.escape(separator)
        r += '%s\n' % code
        r += 'cur="$cur_old"\n'
        r += '%s%s %s "${COMPREPLY[@]}"' % (funcname, dup_arg, shell.escape(separator))
        return BashCompletionCommand(ctxt, r)

    def history(self, ctxt, _trace, pattern):
        funcname = ctxt.helpers.use_function('history')
        return BashCompletionCommand(ctxt, '%s %s' % (funcname, shell.escape(pattern)))

    def commandline_string(self, ctxt, _trace):
        funcname = ctxt.helpers.use_function('commandline_string')
        return BashCompletionCommand(ctxt, '%s' % funcname)

    def command_arg(self, ctxt, _trace):
        return BashCompletionCommand(ctxt, '')

    def date(self, ctxt, _trace, _format):
        return BashCompletionCommand(ctxt, '')

    def date_format(self, ctxt, _trace):
        return BashCompletionCommand(ctxt, '')

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

    def uid(self, ctxt, _trace):
        return BashCompletionCommand(ctxt, bash_versions.uids(ctxt))

    def gid(self, ctxt, _trace):
        return BashCompletionCommand(ctxt, bash_versions.gids(ctxt))

    def signal(self, ctxt, _trace):
        return BashCompletionCommand(ctxt, bash_versions.signals(ctxt))

    def filesystem_type(self, ctxt, _trace):
        return BashCompletionCommand(ctxt, bash_versions.fstypes(ctxt))

    # =========================================================================
    # Bonus
    # =========================================================================

    def login_shell(self, ctxt, _trace):
        return BashCompletionCommand(ctxt, bash_versions.shells(ctxt))

    def net_interface(self, ctxt, _trace):
        func = bash_versions.available_interfaces(ctxt)
        return BashCompletionCommand(ctxt, '%s' % func)

    def timezone(self, ctxt, _trace):
        exec_func = ctxt.helpers.use_function('exec')
        list_func = ctxt.helpers.use_function('timezone_list')
        return BashCompletionCommand(ctxt, '%s %s' % (exec_func, list_func))

    def alsa_card(self, ctxt, _trace):
        exec_func = ctxt.helpers.use_function('exec')
        list_func = ctxt.helpers.use_function('alsa_list_cards')
        return BashCompletionCommand(ctxt, '%s %s' % (exec_func, list_func))

    def alsa_device(self, ctxt, _trace):
        exec_func = ctxt.helpers.use_function('exec')
        list_func = ctxt.helpers.use_function('alsa_list_devices')
        return BashCompletionCommand(ctxt, '%s %s' % (exec_func, list_func))
