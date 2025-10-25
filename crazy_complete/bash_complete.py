'''This module contains code for completing arguments in Bash.'''

from . import shell
from . import bash_versions
from .str_utils import indent
from .type_utils import is_dict_type
from .bash_utils import make_file_extension_pattern


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

        r.append(' '.join(shell.escape(arg) for arg in self.args))

        if append:
            r.append('COMPREPLY=("${COMPREPLY_OLD[@]}" "${COMPREPLY[@]}")')

        return '\n'.join(r)

    def get_function(self):
        if len(self.args) == 1:
            return self.args[0]

        return self.ctxt.helpers.add_dynamic_func(self.ctxt, self.get_code())


class CompgenW(BashCompletionCode):
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

    def get_function(self):
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


class BashCompleteCombine(BashCompletionBase):
    '''Used for combining multiple complete commands.'''

    def __init__(self, ctxt, trace, completer, commands):
        self.ctxt = ctxt
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

    def get_function(self):
        return self.ctxt.helpers.add_dynamic_func(self.ctxt, self.get_code())


class BashCompleteKeyValueList(BashCompletionCode):
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
                funcs[key] = obj.get_function()

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
        return BashCompletionCode(ctxt, '')

    def integer(self, ctxt, _trace, *_):
        return BashCompletionCode(ctxt, '')

    def float(self, ctxt, _trace, *_):
        return BashCompletionCode(ctxt, '')

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
            return BashCompletionCode(ctxt, cmd)

        return BashCompletionFunc(ctxt, [filedir, '-d'])

    def file(self, ctxt, _trace, opts=None):
        fuzzy = False
        directory = None
        extensions = None

        if opts:
            fuzzy = opts.get('fuzzy', False)
            directory = opts.get('directory', None)
            extensions = opts.get('extensions', None)

        args = [bash_versions.filedir(ctxt)]

        if extensions:
            args.append(make_file_extension_pattern(extensions, fuzzy))

        if directory:
            cmd =  'builtin pushd %s &>/dev/null && {\n' % shell.escape(directory)
            cmd += '  %s\n' % ' '.join(shell.escape(a) for a in args)
            cmd += '  builtin popd &>/dev/null\n'
            cmd += '}'
            return BashCompletionCode(ctxt, cmd)

        return BashCompletionFunc(ctxt, args)

    def mime_file(self, ctxt, _trace, pattern):
        func = ctxt.helpers.use_function('mime_file')
        return BashCompletionFunc(ctxt, [func, pattern])

    def group(self, ctxt, _trace):
        return BashCompletionCompgen(ctxt, '-A group')

    def hostname(self, ctxt, _trace):
        return BashCompletionCompgen(ctxt, '-A hostname')

    def pid(self, ctxt, _trace):
        return BashCompletionFunc(ctxt, [bash_versions.pids(ctxt)])

    def process(self, ctxt, _trace):
        return BashCompletionFunc(ctxt, [bash_versions.pnames(ctxt)])

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
        return BashCompletionFunc(ctxt, [func, command])

    def exec_fast(self, ctxt, _trace, command):
        func = ctxt.helpers.use_function('exec_fast')
        return BashCompletionFunc(ctxt, [func, command])

    def exec_internal(self, ctxt, _trace, command):
        return BashCompletionCode(ctxt, command)

    def value_list(self, ctxt, _trace, opts):
        separator = opts.get('separator', ',')
        duplicates = opts.get('duplicates', False)
        values = opts['values']

        if is_dict_type(values):
            values = list(values.keys())

        args = [ctxt.helpers.use_function('value_list')]
        if duplicates:
            args.append('-d')
        args.append(separator)

        return BashCompletionFunc(ctxt, args + values)

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

        func = ctxt.helpers.use_function('value_list')
        dup_arg = ' -d' if duplicates else ''

        r =  'local cur_old="$cur"\n'
        r += 'cur="${cur##*%s}"\n' % shell.escape(separator)
        r += '%s\n' % code
        r += 'cur="$cur_old"\n'
        r += '%s%s %s "${COMPREPLY[@]}"' % (func, dup_arg, shell.escape(separator))
        return BashCompletionCode(ctxt, r)

    def history(self, ctxt, _trace, pattern):
        func = ctxt.helpers.use_function('history')
        return BashCompletionFunc(ctxt, [func, pattern])

    def commandline_string(self, ctxt, _trace):
        func = ctxt.helpers.use_function('commandline_string')
        return BashCompletionFunc(ctxt, [func])

    def command_arg(self, ctxt, _trace):
        return BashCompletionCode(ctxt, '')

    def date(self, ctxt, _trace, _format):
        return BashCompletionCode(ctxt, '')

    def date_format(self, ctxt, _trace):
        return BashCompletionCode(ctxt, '')

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
        return BashCompletionFunc(ctxt, [bash_versions.uids(ctxt)])

    def gid(self, ctxt, _trace):
        return BashCompletionFunc(ctxt, [bash_versions.gids(ctxt)])

    def signal(self, ctxt, _trace):
        return BashCompletionFunc(ctxt, [bash_versions.signals(ctxt)])

    def filesystem_type(self, ctxt, _trace):
        return BashCompletionFunc(ctxt, [bash_versions.fstypes(ctxt)])

    # =========================================================================
    # Bonus
    # =========================================================================

    def login_shell(self, ctxt, _trace):
        return BashCompletionFunc(ctxt, [bash_versions.shells(ctxt)])

    def net_interface(self, ctxt, _trace):
        func = bash_versions.available_interfaces(ctxt)
        return BashCompletionFunc(ctxt, [func])

    def timezone(self, ctxt, _trace):
        exec_func = ctxt.helpers.use_function('exec')
        list_func = ctxt.helpers.use_function('timezone_list')
        return BashCompletionFunc(ctxt, [exec_func, list_func])

    def alsa_card(self, ctxt, _trace):
        func = ctxt.helpers.use_function('alsa_list_cards')
        return BashCompletionFunc(ctxt, [func])

    def alsa_device(self, ctxt, _trace):
        func = ctxt.helpers.use_function('alsa_list_devices')
        return BashCompletionFunc(ctxt, [func])
