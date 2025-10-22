'''This module contains code for completing arguments in Fish.'''

from . import shell
from .type_utils import is_dict_type
from .str_utils import indent, join_with_wrap
from .utils import get_query_option_strings, get_defined_option_types


CHOICES_INLINE_THRESHOLD = 80
# The `choices` command can in Fish be expressed inline in a complete command
# like this:
#   complete -c program -a 'foo bar baz'
# or:
#   complete -c program -a 'foo\t"Foo value" bar\t"Bar value" baz\t"Baz value"'
#
# This variable defines how big this string can get before a function
# is used instead.


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
        return ' '.join(shell.escape(arg) for arg in self.args)

    def get_args(self):
        command = ' '.join(shell.escape(arg) for arg in self.args)
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


class FishCompleteChoices(FishCompletionBase):
    '''Class for completing choices.'''

    def __init__(self, ctxt, choices):
        super().__init__(ctxt)
        self.choices = choices

    @staticmethod
    def _get_inline_for_list(choices):
        return ' '.join(shell.escape(str(c)) for c in choices)

    @staticmethod
    def _get_inline_for_dict(choices):
        str0 = lambda o: str(o) if o is not None else ''
        stringified = {str(item): str0(desc) for item, desc in choices.items()}
        r = ['%s\\t%s' % (shell.escape(item), shell.escape(desc)) for item, desc in stringified.items()]
        return ' '.join(r)

    @staticmethod
    def _get_code_for_list(choices):
        code = "printf '%s\\n' \\\n"
        escaped = [shell.escape(str(item)) for item in choices]
        code += indent(join_with_wrap(' ', ' \\\n', 80, escaped), 2)
        return code.rstrip(' \\\n')

    @staticmethod
    def _get_code_for_dict(choices):
        code = "printf '%s\\t%s\\n' \\\n"
        for item, desc in choices.items():
            if desc is None:
                desc = ''
            code += '  %s %s \\\n' % (shell.escape(str(item)), shell.escape(str(desc)))
        return code.rstrip(' \\\n')

    def get_args(self):
        if is_dict_type(self.choices):
            arg = self._get_inline_for_dict(self.choices)
        else:
            arg = self._get_inline_for_list(self.choices)

        if len(arg) <= CHOICES_INLINE_THRESHOLD:
            return ['-f', '-a', arg]

        func = self.get_function()
        return ['-f', '-a', '(%s)' % func]

    def get_code(self):
        if is_dict_type(self.choices):
            return self._get_code_for_dict(self.choices)
        return self._get_code_for_list(self.choices)


def _get_extension_regex(extensions, fuzzy):
    patterns = []

    for extension in extensions:
        pattern = ''
        for c in extension:
            if c.isalpha():
                pattern += '[%s%s]' % (c.lower(), c.upper())
            elif c in ('.', '+'):
                pattern += f'\\{c}'
            else:
                pattern += c

        if fuzzy:
            pattern += '.*'

        patterns.append(pattern)

    return '|'.join(f'(.*\\.{pattern})' for pattern in patterns)


class FishCompleteFile(FishCompletionBase):
    '''Class for completing files.'''

    def __init__(self, ctxt, opts):
        super().__init__(ctxt)

        fuzzy = False
        directory = None
        extensions = None
        self.args = []

        if opts:
            fuzzy = opts.get('fuzzy', False)
            directory = opts.get('directory', None)
            extensions = opts.get('extensions', None)

        if directory:
            self.args.extend(['-C', directory])

        if extensions:
            ctxt.helpers.use_function('fish_complete_filedir', 'regex')
            self.args.extend(['-r', _get_extension_regex(extensions, fuzzy)])

    def get_args(self):
        if len(self.args) == 0:
            return ['-F']

        func = self.ctxt.helpers.use_function('fish_complete_filedir')
        return FishCompletionCommand(self.ctxt, [func] + self.args).get_args()

    def get_code(self):
        func = self.ctxt.helpers.use_function('fish_complete_filedir')
        return FishCompletionCommand(self.ctxt, [func] + self.args).get_code()

    def get_function(self):
        func = self.ctxt.helpers.use_function('fish_complete_filedir')
        return FishCompletionCommand(self.ctxt, [func] + self.args).get_function()


class FishCompleteDir(FishCompletionCommand):
    '''Class for completing directories.'''

    def __init__(self, ctxt, opts):
        directory = None if opts is None else opts.get('directory', None)

        if directory is not None:
            func = ctxt.helpers.use_function('fish_complete_filedir')
            super().__init__(ctxt, [func, '-D', '-C', directory])
        else:
            super().__init__(ctxt, ['__fish_complete_directories'])


class FishCompleteValueList(FishCompletionCommand):
    '''Class for completing a list of values.'''

    def __init__(self, ctxt, opts):
        separator = opts.get('separator', ',')
        duplicates = opts.get('duplicates', False)
        values = opts['values']

        if is_dict_type(values):
            code = "printf '%s\\t%s\\n' \\\n"
            for item, desc in values.items():
                code += '  %s %s \\\n' % (shell.escape(item), shell.escape(desc))
            code = code.rstrip(' \\\n')
        else:
            code = "printf '%s\\n' \\\n"
            for value in values:
                code += '  %s \\\n' % shell.escape(value)
            code = code.rstrip(' \\\n')

        func = ctxt.helpers.add_dynamic_func(ctxt, code)

        if duplicates:
            complete_list_func = '__fish_complete_list'
        else:
            complete_list_func = ctxt.helpers.use_function('complete_list_uniq')

        super().__init__(ctxt, [complete_list_func, separator, func])


class FishCompletKeyValueList(FishCompletionCommand):
    '''Used for completing a list of key-value pairs.'''

    def __init__(self, ctxt, completer, pair_separator, value_separator, values):
        funcs = {}

        for key, complete in values.items():
            if complete is None or complete[0] == 'none':
                funcs[key] = 'true'
            else:
                command, *args = complete
                obj = getattr(completer, command)(ctxt, *args)
                funcs[key] = obj.get_function()

        e = shell.escape
        args = ' \\\n'.join('%s %s' % (e(k), e(f)) for k, f in funcs.items())
        code = '%s %s %s \\\n%s' % (
            ctxt.helpers.use_function('key_value_list'),
            shell.escape(pair_separator),
            shell.escape(value_separator),
            indent(args, 2)
        )

        func = ctxt.helpers.add_dynamic_func(ctxt, code)

        super().__init__(ctxt, [func])


class FishCompleteCommand(FishCompletionBase):
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

        mkpath = lambda path: ' '.join(shell.escape(p) for p in path.split(':'))

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


class FishCompleteCombine(FishCompletionBase):
    '''Used for combining multiple complete commands.'''

    def __init__(self, ctxt, completer, commands):
        super().__init__(ctxt)

        self.code = []

        for command_args in commands:
            command, *args = command_args
            obj = getattr(completer, command)(ctxt, *args)
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


class FishCompleteCommandArg(FishCompletionBase):
    '''Complete an argument of a command'''

    def __init__(self, ctxt):
        super().__init__(ctxt)

        query = ctxt.helpers.use_function('query', 'positionals_positions')
        types = get_defined_option_types(ctxt.option.parent.get_root_commandline())
        if types.short:
            ctxt.helpers.use_function('query', 'short_options')
        if types.long:
            ctxt.helpers.use_function('query', 'long_options')
        if types.old:
            ctxt.helpers.use_function('query', 'old_options')

        opts = get_query_option_strings(ctxt.option.parent, with_parent_options=True)
        opts = shell.escape(opts)
        command_pos = ctxt.option.get_positional_num() - 1

        r =  'set -l opts %s\n' % shell.escape(opts)
        r += 'set -l pos (%s "$opts" positional_pos %d)\n' % (query, command_pos)
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

    # pylint: disable=missing-function-docstring
    # pylint: disable=too-many-public-methods

    def none(self, ctxt, *_):
        return FishCompleteNone(ctxt)

    def integer(self, ctxt, *_):
        return FishCompleteNone(ctxt)

    def float(self, ctxt, *_):
        return FishCompleteNone(ctxt)

    def choices(self, ctxt, choices):
        return FishCompleteChoices(ctxt, choices)

    def command(self, ctxt, opts=None):
        return FishCompleteCommand(ctxt, opts)

    def directory(self, ctxt, opts=None):
        return FishCompleteDir(ctxt, opts)

    def file(self, ctxt, opts=None):
        return FishCompleteFile(ctxt, opts)

    def mime_file(self, ctxt, pattern):
        func = ctxt.helpers.use_function('mime_file')
        return FishCompletionCommand(ctxt, [func, pattern])

    def group(self, ctxt):
        return FishCompletionCommand(ctxt, ["__fish_complete_groups"])

    def hostname(self, ctxt):
        return FishCompletionCommand(ctxt, ["__fish_print_hostnames"])

    def pid(self, ctxt):
        return FishCompletionCommand(ctxt, ["__fish_complete_pids"])

    def process(self, ctxt):
        return FishCompletionCommand(ctxt, ["__fish_complete_proc"])

    def range(self, ctxt, start, stop, step=1):
        if step == 1:
            return FishCompletionCommand(ctxt, ['command', 'seq', str(start), str(stop)])

        return FishCompletionCommand(ctxt, ['command', 'seq', str(start), str(step), str(stop)])

    def service(self, ctxt):
        return FishCompletionCommand(ctxt, ["__fish_systemctl_services"])

    def user(self, ctxt):
        return FishCompletionCommand(ctxt, ["__fish_complete_users"])

    def variable(self, ctxt):
        return FishCompletionCommand(ctxt, ["set", "-n"])

    def environment(self, ctxt):
        return FishCompletionCommand(ctxt, ["set", "-n", "-x"])

    def exec(self, ctxt, command):
        return FishCompletionRawCommand(ctxt, command)

    def exec_fast(self, ctxt, command):
        return FishCompletionRawCommand(ctxt, command)

    def exec_internal(self, ctxt, command):
        return FishCompletionRawCommand(ctxt, command)

    def value_list(self, ctxt, opts):
        return FishCompleteValueList(ctxt, opts)

    def key_value_list(self, ctxt, pair_separator, value_separator, values):
        return FishCompletKeyValueList(ctxt, self, pair_separator, value_separator, values)

    def combine(self, ctxt, commands):
        return FishCompleteCombine(ctxt, self, commands)

    def list(self, ctxt, command, opts=None):
        separator = opts.get('separator', ',') if opts else ','
        duplicates = opts.get('duplicates', False) if opts else False

        cmd, *args = command
        obj = getattr(self, cmd)(ctxt, *args)
        func = obj.get_function()

        if duplicates:
            complete_list_func = '__fish_complete_list'
        else:
            complete_list_func = ctxt.helpers.use_function('complete_list_uniq')

        return FishCompletionCommand(ctxt, [complete_list_func, separator, func])

    def history(self, ctxt, pattern):
        func = ctxt.helpers.use_function('history')
        return FishCompletionCommand(ctxt, [func, pattern])

    def commandline_string(self, ctxt):
        func = ctxt.helpers.use_function('commandline_string')
        return FishCompletionCommand(ctxt, [func])

    def command_arg(self, ctxt):
        return FishCompleteCommandArg(ctxt)

    def date(self, ctxt, _format):
        return FishCompleteNone(ctxt)

    def date_format(self, ctxt):
        func = ctxt.helpers.use_function('date_format')
        return FishCompletionCommand(ctxt, [func])

    def file_list(self, ctxt, opts=None):
        separator = ','
        duplicates = False
        fuzzy = False
        directory = None
        extensions = None

        if opts:
            separator = opts.get('separator', ',')
            duplicates = opts.get('duplicates', False)
            fuzzy = opts.get('fuzzy', False)
            directory = opts.get('directory', None)
            extensions = opts.get('extensions', None)

        args = []

        if directory:
            args.extend(['-C', shell.escape(directory)])

        if extensions:
            ctxt.helpers.use_function('list_files', 'regex')
            args.extend(['-r', shell.escape(_get_extension_regex(extensions, fuzzy))])

        file_list_func = ctxt.helpers.use_function('list_files')
        func = FishCompletionCommand(ctxt, [file_list_func] + args).get_function()

        if duplicates:
            complete_list_func = '__fish_complete_list'
        else:
            complete_list_func = ctxt.helpers.use_function('complete_list_uniq')

        return FishCompletionCommand(ctxt, [complete_list_func, separator, func])

    def directory_list(self, ctxt, opts=None):
        separator = ','
        duplicates = False
        directory = None

        if opts:
            separator = opts.get('separator', ',')
            directory = opts.get('directory', None)
            duplicates = opts.get('duplicates', False)

        args = ['-D']

        if directory:
            args.extend(['-C', shell.escape(directory)])

        file_list_func = ctxt.helpers.use_function('list_files')
        func = FishCompletionCommand(ctxt, [file_list_func] + args).get_function()

        if duplicates:
            complete_list_func = '__fish_complete_list'
        else:
            complete_list_func = ctxt.helpers.use_function('complete_list_uniq')

        return FishCompletionCommand(ctxt, [complete_list_func, separator, func])

    def uid(self, ctxt):
        func = ctxt.helpers.use_function('uid_list')
        return FishCompletionCommand(ctxt, [func])

    def gid(self, ctxt):
        func = ctxt.helpers.use_function('gid_list')
        return FishCompletionCommand(ctxt, [func])

    # =========================================================================
    # Bonus
    # =========================================================================

    def net_interface(self, ctxt):
        func = ctxt.helpers.use_function('net_interfaces_list')
        return FishCompletionCommand(ctxt, [func])

    def timezone(self, ctxt):
        func = ctxt.helpers.use_function('timezone_list')
        return FishCompletionCommand(ctxt, [func])

    def alsa_card(self, ctxt):
        func = ctxt.helpers.use_function('alsa_list_cards')
        return FishCompletionCommand(ctxt, [func])

    def alsa_device(self, ctxt):
        func = ctxt.helpers.use_function('alsa_list_devices')
        return FishCompletionCommand(ctxt, [func])
