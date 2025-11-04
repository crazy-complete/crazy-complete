'''This module contains code for completing arguments in Bash.'''

from . import shell
from . import bash_versions
from .str_utils import indent
from .type_utils import is_dict_type
from .bash_utils import make_file_extension_pattern
from .utils import key_value_list_normalize_values


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


class CompgenW(BashCompletionBase):
    '''Used for completing a list of words.'''

    def __init__(self, ctxt, values):
        self.ctxt = ctxt
        self.values = [str(value) for value in values]

    def get_code(self, append=False):
        needs_quote = any(filter(shell.needs_quote, self.values))

        if not needs_quote:
            return 'COMPREPLY%s=($(compgen -W %s -- "$cur"))' % (
                ('+' if append else ''),
                shell.quote(' '.join(self.values)))

        return ('%s %s-- %s' % (
            self.ctxt.helpers.use_function('values'),
            ('-a ' if append else ''),
            shell.join_quoted(self.values)))

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


class BashCompleteKeyValueList(BashCompletionCode):
    '''Used for completing a list of key-value pairs.'''

    # pylint: disable=too-many-arguments
    # pylint: disable=too-many-positional-arguments

    def __init__(self, ctxt, trace, completer,
                 pair_separator, value_separator, values):
        funcs = {}

        for key, _desc, complete in key_value_list_normalize_values(values):
            if not complete:
                funcs[key] = 'false'
            elif complete[0] == 'none':
                funcs[key] = 'true'
            else:
                obj = completer.complete_from_def(ctxt, trace, complete)
                funcs[key] = obj.get_function()

        q = shell.quote
        args = ' \\\n'.join('%s %s' % (q(k), q(f)) for k, f in funcs.items())

        code = '%s %s %s \\\n%s' % (
            ctxt.helpers.use_function('key_value_list'),
            shell.quote(pair_separator),
            shell.quote(value_separator),
            indent(args, 2)
        )

        super().__init__(ctxt, code)


class BashCompleter(shell.ShellCompleter):
    '''Code generator for completing arguments in Bash.'''

    # pylint: disable=missing-function-docstring
    # pylint: disable=too-many-public-methods
    # pylint: disable=too-many-arguments
    # pylint: disable=too-many-positional-arguments

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

    def directory(self, ctxt, _trace, opts=None):
        directory = None if opts is None else opts.get('directory', None)
        filedir = bash_versions.filedir(ctxt)

        if directory:
            r = 'builtin pushd %s &>/dev/null && {\n' % shell.quote(directory)
            r += '  %s -d\n' % filedir
            r += '  builtin popd >/dev/null\n'
            r += '}'
            return BashCompletionCode(ctxt, r)

        return BashCompletionFunc(ctxt, [filedir, '-d'])

    def file(self, ctxt, _trace, opts=None):
        fuzzy = False
        directory = None
        extensions = None
        ignore_globs = None

        if opts:
            fuzzy = opts.get('fuzzy', False)
            directory = opts.get('directory', None)
            extensions = opts.get('extensions', None)
            ignore_globs = opts.get('ignore_globs', None)

        args = [bash_versions.filedir(ctxt)]

        if extensions:
            args.append(make_file_extension_pattern(extensions, fuzzy))

        if not directory and not ignore_globs:
            return BashCompletionFunc(ctxt, args)

        if directory:
            r = 'builtin pushd %s &>/dev/null && {\n' % shell.quote(directory)
            r += '  %s\n' % shell.join_quoted(args)
            r += '  builtin popd >/dev/null\n'
            r += '}'
        else:
            r = shell.join_quoted(args)

        if ignore_globs:
            func = ctxt.helpers.use_function('file_filter')
            r += '\n%s %s' % (func, shell.join_quoted(ignore_globs))

        return BashCompletionCode(ctxt, r)

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

        obj = self.complete_from_def(ctxt, trace, command)
        code = obj.get_code()

        func = ctxt.helpers.use_function('value_list')
        dup_arg = ' -d' if duplicates else ''

        r = 'local cur_old="$cur"\n'
        r += 'cur="${cur##*%s}"\n' % shell.quote(separator)
        r += '%s\n' % code
        r += 'cur="$cur_old"\n'
        r += '%s%s %s "${COMPREPLY[@]}"' % (func, dup_arg, shell.quote(separator))
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

    def uid(self, ctxt, _trace):
        return BashCompletionFunc(ctxt, [bash_versions.uids(ctxt)])

    def gid(self, ctxt, _trace):
        return BashCompletionFunc(ctxt, [bash_versions.gids(ctxt)])

    def signal(self, ctxt, _trace):
        return BashCompletionFunc(ctxt, [bash_versions.signals(ctxt)])

    def filesystem_type(self, ctxt, _trace):
        return BashCompletionFunc(ctxt, [bash_versions.fstypes(ctxt)])

    def prefix(self, ctxt, trace, prefix, command):
        obj = self.complete_from_def(ctxt, trace, command)
        func = obj.get_function()
        prefix_func = ctxt.helpers.use_function('prefix')
        return BashCompletionFunc(ctxt, [prefix_func, prefix, func])

    def ip_address(self, ctxt, _trace, type_='all'):
        func = bash_versions.ip_addresses(ctxt)

        if type_ == 'ipv6':
            return BashCompletionFunc(ctxt, [func, '-6'])

        if type_ == 'ipv4':
            return BashCompletionFunc(ctxt, [func])

        return BashCompletionFunc(ctxt, [func, '-a'])

    # =========================================================================
    # Bonus
    # =========================================================================

    def locale(self, ctxt, trace):
        func = ctxt.helpers.use_function('locales')
        return BashCompletionFunc(ctxt, [func])

    def charset(self, ctxt, trace):
        func = ctxt.helpers.use_function('charsets')
        return BashCompletionFunc(ctxt, [func])

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
