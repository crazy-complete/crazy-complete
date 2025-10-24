'''This module contains code for completing arguments in Zsh.'''

from . import shell
from .str_utils import join_with_wrap, indent
from .zsh_utils import escape_colon, escape_square_brackets, make_file_extension_pattern
from .type_utils import is_dict_type


CHOICES_INLINE_THRESHOLD = 80
# The `choices` command can in Zsh be expressed inline in an optspec, like this:
#   (foo bar baz)
# or:
#   (foo\:"Foo value" bar\:"Bar value" baz\:"Baz value)
#
# This variable defines how big this string can get before a function
# is used instead.


class ZshCompletionBase:
    '''Base class for Zsh completions.'''

    def get_action_string(self):
        '''Return an action string that can be used in an option spec.'''
        raise NotImplementedError

    def get_function(self):
        '''Return a function that can be used in e.g. `_sequence`.'''


class ZshComplFunc(ZshCompletionBase):
    def __init__(self, ctxt, args, needs_braces=False):
        self.ctxt = ctxt
        self.args = args
        self.needs_braces = needs_braces

    def get_action_string(self):
        if len(self.args) == 1:
            cmd = self.args[0]
        else:
            cmd = ' '.join(shell.escape(arg) for arg in self.args)

        if self.needs_braces:
            cmd = shell.escape('{%s}' % cmd)
        else:
            cmd = shell.escape(cmd)

        return escape_colon(cmd)

    def get_function(self):
        if len(self.args) == 1:
            return self.args[0]

        code = ' '.join(shell.escape(arg) for arg in self.args)
        funcname = self.ctxt.helpers.add_dynamic_func(self.ctxt, code)
        return funcname


class ZshCompleteChoices(ZshCompletionBase):
    def __init__(self, ctxt, trace, choices):
        self.ctxt = ctxt
        self.trace = trace
        self.choices = choices

    def _list_action_string(self):
        items   = [str(item) for item in self.choices]
        escaped = [shell.escape(escape_colon(item)) for item in items]
        action  = shell.escape('(%s)' % ' '.join(escaped))
        if len(action) <= CHOICES_INLINE_THRESHOLD:
            return action

        return self._list_function()

    def _list_function(self):
        metavar = shell.escape(self.ctxt.option.metavar or '')
        escaped = [shell.escape(escape_colon(c)) for c in self.choices]

        code  = 'local items=(\n'
        code += indent(join_with_wrap(' ', '\n', 78, escaped), 2)
        code += '\n)\n\n'
        code += f'_describe -- {metavar} items'

        funcname = self.ctxt.helpers.add_dynamic_func(self.ctxt, code)
        return funcname

    def _dict_action_string(self):
        # _alternative (used in `combine`) does not allow inlined version
        if self.trace and self.trace[-1] == 'combine':
            return self._dict_function()

        items   = [str(item) for item in self.choices.keys()]
        values  = [str(value) for value in self.choices.values()]
        colon   = any(':' in s for s in items + values)
        escaped = ['%s\\:%s' % (shell.escape(item), shell.escape(value)) for item, value in zip(items, values)]
        action  = shell.escape('((%s))' % ' '.join(escaped))
        if not colon and len(action) <= CHOICES_INLINE_THRESHOLD:
            return action

        return self._dict_function()

    def _dict_function(self):
        metavar  = shell.escape(self.ctxt.option.metavar or '')

        code  = 'local items=(\n'
        for item, desc in self.choices.items():
            item = shell.escape(escape_colon(str(item)))
            if desc:
                desc = shell.escape(str(desc))
                code += f'  {item}:{desc}\n'
            else:
                code += f'  {item}\n'
        code += ')\n\n'
        code += f'_describe -- {metavar} items'

        funcname = self.ctxt.helpers.add_dynamic_func(self.ctxt, code)
        return funcname

    def get_action_string(self):
        if is_dict_type(self.choices):
            return self._dict_action_string()

        return self._list_action_string()

    def get_function(self):
        if is_dict_type(self.choices):
            return self._dict_function()

        return self._list_function()


class ZshCompleteCommand(ZshCompletionBase):
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
            self.code = 'local -x PATH=%s' % shell.escape(path)
        elif append and prepend:
            append = shell.escape(append)
            prepend = shell.escape(prepend)
            self.code = 'local -x PATH=%s:"$PATH":%s' % (prepend, append)
        elif append:
            self.code = 'local -x PATH="$PATH":%s' % shell.escape(append)
        elif prepend:
            self.code = 'local -x PATH=%s:"$PATH"' % shell.escape(prepend)

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


class ZshCompleteRange(ZshCompletionBase):
    def __init__(self, ctxt, start, stop, step):
        self.ctxt = ctxt
        self.start = start
        self.stop = stop
        self.step = step

    def get_action_string(self):
        if self.step == 1:
            return f"'({{{self.start}..{self.stop}}})'"

        return f"'({{{self.start}..{self.stop}..{self.step}}})'"

    def get_function(self):
        if self.step == 1:
            code = f"command seq {self.start} {self.step} {self.stop}"
        else:
            code = f"command seq {self.start}  {self.stop}"

        code = f'compadd -- $({code})'

        funcname = self.ctxt.helpers.add_dynamic_func(self.ctxt, code)
        return funcname


class ZshKeyValueList(ZshComplFunc):
    '''Used for completing a list of key-value pairs.'''

    def __init__(self, ctxt, trace, completer, pair_separator, value_separator, values):
        spec = []
        trace.append('key_value_list')

        for key, complete in values.items():
            if not complete:
                spec.append('%s' % escape_colon(key))
            elif complete[0] == 'none':
                spec.append('%s:::' % escape_colon(key))
            else:
                command, *args = complete
                compl_obj = getattr(completer, command)(ctxt, trace, *args)
                action = compl_obj.get_action_string()
                spec.append('%s:::%s' % (escape_colon(key), action))

        code = '_values -s %s -S %s %s \\\n' % (
            shell.escape(pair_separator),
            shell.escape(value_separator),
            shell.escape(ctxt.option.metavar or ''))

        code += indent(' \\\n'.join(spec), 2)

        func = ctxt.helpers.add_dynamic_func(ctxt, code)

        super().__init__(ctxt, [func], needs_braces=True)


class ZshCompleteCombine(ZshCompletionBase):
    def __init__(self, ctxt, trace, completer, commands):
        # metavar = shell.escape(ctxt.option.metavar or '')
        trace.append('combine')

        completions = []
        for command_args in commands:
            command, *args = command_args
            compl_obj = getattr(completer, command)(ctxt, trace, *args)
            completions.append(compl_obj.get_action_string())

        code  = '_alternative \\\n'
        for completion in completions:
            code += '  %s \\\n' % completion
        code = code.rstrip(' \\\n')

        self.func = ctxt.helpers.add_dynamic_func(ctxt, code)

    def get_function(self):
        return self.func

    def get_action_string(self):
        return shell.escape('{%s}' % self.func)


class ZshCompleter(shell.ShellCompleter):
    '''Code generator for completing arguments in Zsh.'''

    # pylint: disable=too-many-public-methods
    # pylint: disable=missing-function-docstring

    def none(self, ctxt, _trace, *_):
        return ZshComplFunc(ctxt, [' '])

    def integer(self, ctxt, _trace):
        return ZshComplFunc(ctxt, ['_numbers'])

    def float(self, ctxt, _trace):
        return ZshComplFunc(ctxt, ['_numbers', '-f'])

    def choices(self, ctxt, trace, choices):
        return ZshCompleteChoices(ctxt, trace, choices)

    def command(self, ctxt, _trace, opts=None):
        return ZshCompleteCommand(ctxt, opts)

    def directory(self, ctxt, _trace, opts=None):
        directory = None if opts is None else opts.get('directory', None)

        if not directory:
            return ZshComplFunc(ctxt, ['_directories'])

        return ZshComplFunc(ctxt, ['_directories', '-W', directory])

    def file(self, ctxt, _trace, opts=None):
        fuzzy = False
        directory = None
        extensions = None

        if opts:
            fuzzy = opts.get('fuzzy', False)
            directory = opts.get('directory', None)
            extensions = opts.get('extensions', None)

        args = []

        if directory:
            args.extend(['-W', directory])

        if extensions:
            args.extend(['-g', make_file_extension_pattern(extensions, fuzzy)])

        return ZshComplFunc(ctxt, ['_files'] + args)

    def mime_file(self, ctxt, _trace, pattern):
        func = ctxt.helpers.use_function('mime_file')
        return ZshComplFunc(ctxt, [func, pattern], needs_braces=True)

    def group(self, ctxt, _trace):
        return ZshComplFunc(ctxt, ['_groups'])

    def hostname(self, ctxt, _trace):
        return ZshComplFunc(ctxt, ['_hosts'])

    def pid(self, ctxt, _trace):
        return ZshComplFunc(ctxt, ['_pids'])

    def process(self, ctxt, _trace):
        return ZshComplFunc(ctxt, ['_process_names', '-a'])

    def range(self, ctxt, _trace, start, stop, step=1):
        return ZshCompleteRange(ctxt, start, stop, step)

    def user(self, ctxt, _trace):
        return ZshComplFunc(ctxt, ['_users'])

    def variable(self, ctxt, _trace):
        return ZshComplFunc(ctxt, ['_vars'])

    def environment(self, ctxt, _trace):
        return ZshComplFunc(ctxt, ['_parameters', '-g', '*export*'])

    def exec(self, ctxt, _trace, command):
        funcname = ctxt.helpers.use_function('exec')
        return ZshComplFunc(ctxt, [funcname, command], needs_braces=True)

    def exec_fast(self, ctxt, _trace, command):
        funcname = ctxt.helpers.use_function('exec')
        return ZshComplFunc(ctxt, [funcname, command], needs_braces=True)

    def exec_internal(self, ctxt, _trace, command):
        return ZshComplFunc(ctxt, [command], needs_braces=True)

    def value_list(self, ctxt, trace, opts):
        desc   = ctxt.option.metavar or ''
        values = opts['values']
        separator = opts.get('separator', ',')
        duplicates = opts.get('duplicates', False)

        if is_dict_type(values):
            esc = escape_square_brackets
            values = ['%s[%s]' % (esc(item), esc(desc)) for item, desc in values.items()]
        else:
            values = [escape_square_brackets(i) for i in values]

        if not duplicates:
            return ZshComplFunc(ctxt, ['_values', '-s', separator, desc] + values)

        values_func = ZshComplFunc(ctxt, ['_values', desc] + values).get_function()

        if separator == ',':
            return ZshComplFunc(ctxt, ['_sequence', '-d', values_func])

        return ZshComplFunc(ctxt, ['_sequence', '-s', separator, '-d', values_func])

    def key_value_list(self, ctxt, trace, pair_separator, value_separator, values):
        return ZshKeyValueList(ctxt, trace, self, pair_separator, value_separator, values)

    def combine(self, ctxt, trace, commands):
        return ZshCompleteCombine(ctxt, trace, self, commands)

    def list(self, ctxt, trace, command, opts=None):
        separator = opts.get('separator', ',') if opts else ','
        duplicates = opts.get('duplicates', False) if opts else False
        trace.append('list')

        cmd, *args = command
        obj = getattr(self, cmd)(ctxt, trace, *args)
        func = obj.get_function()

        args = []

        if separator != ',':
            args.extend(['-s', separator])

        if duplicates:
            args.append('-d')

        return ZshComplFunc(ctxt, ['_sequence', *args, func])

    def history(self, ctxt, _trace, pattern):
        func = ctxt.helpers.use_function('history')
        return ZshComplFunc(ctxt, [func, pattern], needs_braces=True)

    def commandline_string(self, ctxt, _trace):
        return ZshComplFunc(ctxt, ['_cmdstring'])

    def command_arg(self, ctxt, _trace):
        return ZshComplFunc(ctxt, ['_normal'])

    def date(self, ctxt, _trace, format_):
        return ZshComplFunc(ctxt, ['_dates', '-f', format_])

    def date_format(self, ctxt, _trace):
        return ZshComplFunc(ctxt, ['_date_formats'])

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
        func = ctxt.helpers.use_function('uid_list')
        return ZshComplFunc(ctxt, [func], needs_braces=True)

    def gid(self, ctxt, _trace):
        func = ctxt.helpers.use_function('gid_list')
        return ZshComplFunc(ctxt, [func], needs_braces=True)

    def filesystem_type(self, ctxt, _trace):
        return ZshComplFunc(ctxt, ['_file_systems'])

    def signal(self, ctxt, _trace):
        return ZshComplFunc(ctxt, ['_signals'])

    # =========================================================================
    # Bonus
    # =========================================================================

    def net_interface(self, ctxt, _trace):
        return ZshComplFunc(ctxt, ['_net_interfaces'])

    def timezone(self, ctxt, _trace):
        return ZshComplFunc(ctxt, ['_time_zone'])

    def locale(self, ctxt, _trace):
        return ZshComplFunc(ctxt, ['_locales'])

    def alsa_card(self, ctxt, _trace):
        func = ctxt.helpers.use_function('alsa_complete_cards')
        return ZshComplFunc(ctxt, [func], needs_braces=True)

    def alsa_device(self, ctxt, _trace):
        func = ctxt.helpers.use_function('alsa_complete_devices')
        return ZshComplFunc(ctxt, [func], needs_braces=True)
