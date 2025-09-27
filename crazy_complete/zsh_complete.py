'''This module contains code for completing arguments in Zsh.'''

from . import shell
from . import helpers
from .str_utils import join_with_wrap, indent
from .zsh_utils import escape_colon, escape_square_brackets

CHOICES_INLINE_THRESHOLD = 80
# The `choices` command can in Zsh be expressed inline in an optspec, like this:
#   (foo bar baz)
# or:
#   (foo\:"Foo value" bar\:"Bar value" baz\:"Baz value)
#
# This variable defines how big this string can get before a function
# is used instead.

class ZshCompleter(shell.ShellCompleter):
    '''Code generator for completing arguments in Zsh.'''

    # pylint: disable=too-many-public-methods
    # pylint: disable=missing-function-docstring

    def none(self, *_):
        return "' '"

    def integer(self, _ctxt):
        return '_numbers'

    def float(self, _ctxt):
        return "'_numbers -f'"

    def choices(self, ctxt, choices):
        if hasattr(choices, 'items'):
            return self._choices_dict(ctxt, choices)

        return self._choices_list(ctxt, choices)

    def _choices_list(self, ctxt, choices):
        # Inline choices
        items   = [str(item) for item in choices]
        escaped = [shell.escape(escape_colon(item)) for item in items]
        action  = shell.escape('(%s)' % ' '.join(escaped))
        if len(action) <= CHOICES_INLINE_THRESHOLD:
            return action

        # Make a function
        funcname = ctxt.helpers.get_unique_function_name(ctxt)
        metavar  = shell.escape(ctxt.option.metavar or '')
        escaped  = [shell.escape(escape_colon(c)) for c in choices]

        code  = 'local items=(\n'
        code += indent(join_with_wrap(' ', '\n', 78, escaped), 2)
        code += '\n)\n\n'
        code += f'_describe -- {metavar} items'

        ctxt.helpers.add_function(helpers.ShellFunction(funcname, code))
        funcname = ctxt.helpers.use_function(funcname)
        return funcname

    def _choices_dict(self, ctxt, choices):
        # Inline choices
        #   This does not work with `combine`; maybe we have to introduce
        #   a `combined` parameter to fix this
        #
        #   items   = [str(item) for item in choices.keys()]
        #   values  = [str(value) for value in choices.values()]
        #   colon   = any(':' in s for s in items + values)
        #   escaped = ['%s\\:%s' % (shell.escape(item), shell.escape(value)) for item, value in zip(items, values)]
        #   action  = shell.escape('((%s))' % ' '.join(escaped))
        #   if not colon and len(action) <= CHOICES_INLINE_THRESHOLD:
        #       return action

        # Make a function
        funcname = ctxt.helpers.get_unique_function_name(ctxt)
        metavar  = shell.escape(ctxt.option.metavar or '')

        code  = 'local items=(\n'
        for item, desc in choices.items():
            item = shell.escape(escape_colon(str(item)))
            desc = shell.escape(str(desc))
            code += f'  {item}:{desc}\n'
        code += ')\n\n'
        code += f'_describe -- {metavar} items'

        ctxt.helpers.add_function(helpers.ShellFunction(funcname, code))
        funcname = ctxt.helpers.use_function(funcname)
        return funcname

    def command(self, _ctxt):
        return '_command_names'

    def directory(self, _ctxt, opts=None):
        directory = None if opts is None else opts.get('directory', None)

        if directory:
            return shell.escape('_directories %s' % shell.escape(directory))

        return '_directories'

    def file(self, _ctxt, opts=None):
        directory = None if opts is None else opts.get('directory', None)

        if directory:
            return shell.escape('_files -W %s' % shell.escape(directory))

        return '_files'

    def group(self, _ctxt):
        return '_groups'

    def hostname(self, _ctxt):
        return '_hosts'

    def pid(self, _ctxt):
        return '_pids'

    def process(self, _ctxt):
        return "'_process_names -a'"

    def range(self, _ctxt, start, stop, step=1):
        if step == 1:
            return f"'({{{start}..{stop}}})'"

        return f"'({{{start}..{stop}..{step}}})'"

    def user(self, _ctxt):
        return '_users'

    def variable(self, _ctxt):
        return '_vars'

    def environment(self, _ctxt):
        return '"_parameters -g \'*export*\'"'

    def exec(self, ctxt, command):
        funcname = ctxt.helpers.use_function('exec')
        return shell.escape('{%s %s}' % (funcname, shell.escape(command)))

    def exec_fast(self, ctxt, command):
        funcname = ctxt.helpers.use_function('exec')
        return shell.escape('{%s %s}' % (funcname, shell.escape(command)))

    def exec_internal(self, _ctxt, command):
        return shell.escape(command)

    def value_list(self, ctxt, opts):
        desc   = ctxt.option.metavar or ''
        values = opts['values']

        if hasattr(values, 'items'):
            values_arg = ' '.join(
                shell.escape('%s[%s]' % (
                    escape_square_brackets(item),
                    escape_square_brackets(desc))
                ) for item, desc in values.items()
            )
        else:
            values_arg = ' '.join(shell.escape(escape_square_brackets(i)) for i in values)

        cmd = '_values -s %s %s %s' % (
            shell.escape(opts.get('separator', ',')),
            shell.escape(desc),
            values_arg
        )

        return shell.escape(cmd)

    def combine(self, ctxt, commands):
        completions = []
        for command_args in commands:
            command, *args = command_args
            c = getattr(self, command)(ctxt, *args)
            completions.append(c)

        funcname = ctxt.helpers.get_unique_function_name(ctxt)
        #metavar = shell.escape(ctxt.option.metavar or '')

        code  = '_alternative \\\n'
        for completion in completions:
            code += '  %s \\\n' % completion
        code = code.rstrip(' \\\n')

        ctxt.helpers.add_function(helpers.ShellFunction(funcname, code))
        funcname = ctxt.helpers.use_function(funcname)
        return funcname
