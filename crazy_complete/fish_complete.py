'''This module contains code for completing arguments in Fish.'''

from . import shell
from .type_utils import is_dict_type
from .str_utils import indent, join_with_wrap

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


class FishCompleteNone(FishCompletionBase):
    '''Class for completing an argument without a completer.'''

    def get_args(self):
        return ['-f']

    def get_code(self):
        return ''


class FishCompletionCommand(FishCompletionBase):
    '''Class for executing a command and parsing its output.'''

    def __init__(self, command):
        self.command = command

    def get_code(self):
        return self.command

    def get_args(self):
        return ['-f', '-a', '(%s)' % self.command]


class FishCompleteChoices(FishCompletionBase):
    '''Class for completing choices.'''

    def __init__(self, ctxt, choices):
        self.ctxt = ctxt
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

        code = self.get_code()

        funcname = self.ctxt.helpers.add_dynamic_func(self.ctxt, code)
        return ['-f', '-a', '(%s)' % funcname]

    def get_code(self):
        if is_dict_type(self.choices):
            return self._get_code_for_dict(self.choices)
        return self._get_code_for_list(self.choices)


class FishCompleteFile(FishCompletionBase):
    '''Class for completing files.'''

    def __init__(self, ctxt, opts):
        self.ctxt = ctxt
        self.directory = None
        self.extensions = None

        if opts:
            self.directory = opts.get('directory', None)
            self.extensions = opts.get('extensions', None)

    def _get_extension_regex(self):
        patterns = []

        for extension in self.extensions:
            pattern = ''
            for c in extension:
                if c.isalpha():
                    pattern += '[%s%s]' % (c.lower(), c.upper())
                elif c in ('.', '+'):
                    pattern += f'\\{c}'
                else:
                    pattern += c
            patterns.append(pattern)

        return '|'.join(f'(.*\\.{pattern})' for pattern in patterns)

    def get_args(self):
        args = []

        if self.directory:
            args.extend(['-C', shell.escape(self.directory)])

        if self.extensions:
            self.ctxt.helpers.use_function('fish_complete_filedir', 'regex')
            args.extend(['-r', shell.escape(self._get_extension_regex())])

        if not args:
            return ['-F']

        funcname = self.ctxt.helpers.use_function('fish_complete_filedir')
        return ['-f', '-a', '(%s %s)' % (funcname, ' '.join(args))]

    def get_code(self):
        args = []

        if self.directory:
            args.extend(['-C', shell.escape(self.directory)])

        if self.extensions:
            self.ctxt.helpers.use_function('fish_complete_filedir', 'regex')
            args.extend(['-r', shell.escape(self._get_extension_regex())])

        funcname = self.ctxt.helpers.use_function('fish_complete_filedir')

        if not args:
            return funcname

        return '%s %s' % (funcname, ' '.join(args))


class FishCompleteDir(FishCompletionBase):
    '''Class for completing directories.'''

    def __init__(self, ctxt, opts):
        self.ctxt = ctxt
        self.directory = None if opts is None else opts.get('directory', None)

    def get_args(self):
        if self.directory is not None:
            funcname = self.ctxt.helpers.use_function('fish_complete_filedir')
            return ['-f', '-a', '(%s -D -C %s)' % (funcname, shell.escape(self.directory))]

        return ['-f', '-a', '(__fish_complete_directories)']

    def get_code(self):
        if self.directory is not None:
            funcname = self.ctxt.helpers.use_function('fish_complete_filedir')
            return '%s -D -C %s' % (funcname, shell.escape(self.directory))

        return '__fish_complete_directories'


class FishCompleteValueList(FishCompletionBase):
    '''Class for completing a list of values.'''

    def __init__(self, ctxt, opts):
        separator = opts.get('separator', ',')
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

        funcname = ctxt.helpers.add_dynamic_func(ctxt, code)
        self.cmd = '__fish_complete_list %s %s' % (shell.escape(separator), funcname)

    def get_args(self):
        return ['-f', '-a', '(%s)' % self.cmd]

    def get_code(self):
        return self.cmd


class FishCompleteCombine(FishCompletionBase):
    '''Used for combining multiple complete commands.'''

    def __init__(self, ctxt, completer, commands):
        self.ctxt = ctxt
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
        funcname = self.ctxt.helpers.add_dynamic_func(self.ctxt, code)
        return ['-f', '-a', '(%s)' % funcname]


class FishCompleter(shell.ShellCompleter):
    '''Code generator for completing arguments in Fish.'''

    # pylint: disable=missing-function-docstring
    # pylint: disable=too-many-public-methods

    def none(self, _ctxt, *_):
        return FishCompleteNone()

    def integer(self, _ctxt, *_):
        return FishCompleteNone()

    def float(self, _ctxt, *_):
        return FishCompleteNone()

    def choices(self, ctxt, choices):
        return FishCompleteChoices(ctxt, choices)

    def command(self, __ctxt):
        return FishCompletionCommand("__fish_complete_command")

    def directory(self, ctxt, opts=None):
        return FishCompleteDir(ctxt, opts)

    def file(self, ctxt, opts=None):
        return FishCompleteFile(ctxt, opts)

    def group(self, _ctxt):
        return FishCompletionCommand("__fish_complete_groups")

    def hostname(self, _ctxt):
        return FishCompletionCommand("__fish_print_hostnames")

    def pid(self, _ctxt):
        return FishCompletionCommand("__fish_complete_pids")

    def process(self, _ctxt):
        return FishCompletionCommand("__fish_complete_proc")

    def range(self, _ctxt, start, stop, step=1):
        if step == 1:
            return FishCompletionCommand(f"command seq {start} {stop}")

        return FishCompletionCommand(f"command seq {start} {step} {stop}")

    def service(self, _ctxt):
        return FishCompletionCommand("__fish_systemctl_services")

    def user(self, _ctxt):
        return FishCompletionCommand("__fish_complete_users")

    def variable(self, _ctxt):
        return FishCompletionCommand("set -n")

    def environment(self, _ctxt):
        return FishCompletionCommand("set -n -x")

    def exec(self, _ctxt, command):
        return FishCompletionCommand(command)

    def exec_fast(self, _ctxt, command):
        return FishCompletionCommand(command)

    def exec_internal(self, _ctxt, command):
        return FishCompletionCommand(command)

    def value_list(self, ctxt, opts):
        return FishCompleteValueList(ctxt, opts)

    def combine(self, ctxt, commands):
        return FishCompleteCombine(ctxt, self, commands)

    def history(self, ctxt, pattern):
        func = ctxt.helpers.use_function('history')
        return FishCompletionCommand('%s %s' % (func, shell.escape(pattern)))

    def commandline_string(self, ctxt):
        func = ctxt.helpers.use_function('commandline_string')
        return FishCompletionCommand(func)

    def command_arg(self, _ctxt):
        return FishCompleteNone()

    # =========================================================================
    # Bonus
    # =========================================================================

    def net_interface(self, ctxt):
        func = ctxt.helpers.use_function('net_interfaces_list')
        return FishCompletionCommand(func)

    def timezone(self, ctxt):
        func = ctxt.helpers.use_function('timezone_list')
        return FishCompletionCommand(func)

    def alsa_card(self, ctxt):
        func = ctxt.helpers.use_function('alsa_list_cards')
        return FishCompletionCommand(func)

    def alsa_device(self, ctxt):
        func = ctxt.helpers.use_function('alsa_list_devices')
        return FishCompletionCommand(func)
