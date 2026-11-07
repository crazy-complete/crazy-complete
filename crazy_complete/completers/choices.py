# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2025-2026 Benjamin Abendroth <braph93@gmx.de>

'''Completer for presenting a static set of choices.'''

from .. import shell
from ..bash_complete import BashCompletionBase
from ..fish_complete import FishCompletionBase
from ..zsh_complete import ZshCompletionBase
from ..zsh_utils import escape_colon
from ..type_utils import is_dict_type
from ..str_utils import indent, join_with_wrap
from ..scheme_validator import check_type

CATEGORY = 'basic'

SYNOPSIS = r'''
['choices', <ITEMS>]
'''

SHORT = 'Complete from a predefined set of values'

LONG = r'''
`ITEMS`:
  A list or dictionary containing the values to offer for completion.

  If a list is supplied, all items are offered without descriptions.

  If a dictionary is supplied, the keys are used as completion values and the
  values are used as descriptions.
'''

NOTES = [
    'If the completion suggestions should appear in their original order, set `nosort` to `true`',
]

DEFINITION = r'''
prog: 'example'
options:
  - option_strings: ['--choices-1']
    complete: ['choices', ['Item 1', 'Item 2']]

  - option_strings: ['--choices-2']
    complete: ['choices', {'Item 1': 'Description 1', 'Item 2': 'Description 2'}]

  - option_strings: ['--choices-keep-order']
    complete: ['choices', ['zebra', 'cat', 'monkey']]
    nosort: true
'''

OUTPUT = r'''
~ > example --choices-2=<TAB>
Item 1  (Description 1)  Item 2  (Description 2)

~ > example --choices-keep-order=<TAB>
zebra    cat    monkey
'''

CHOICES_INLINE_THRESHOLD = 80
# The `choices` command can in Fish be expressed inline in a complete command
# like this:
#   complete -c program -a 'foo bar baz'
# or:
#   complete -c program -a 'foo\t"Foo value" bar\t"Bar value" baz\t"Baz value"'
#
# The `choices` command can in Zsh be expressed inline in an optspec, like:
#   (foo bar baz)
# or:
#   (foo:"Foo value" bar:"Bar value" baz:"Baz value")
#
# This variable defines how big this string can get before a function
# is used instead.


def validate(_ctxt, arguments):
    '''Validate YAML for choices completer'''
    choices = arguments.get_required_arg('values')
    check_type(choices, (list, dict), 'values')
    arguments.require_no_more()

    if isinstance(choices.value, dict):
        for i, (value, desc) in enumerate(choices.value.items()):
            check_type(value, (str, int), f'values[{i}]: item')
            check_type(desc,  (str, int), f'values[{i}]: description')

    elif isinstance(choices.value, list):
        for i, value in enumerate(choices.value):
            check_type(value, (str, int), f'values[{i}]')


class FishCompleteChoices(FishCompletionBase):
    '''Class for completing choices.'''

    def __init__(self, ctxt, choices):
        super().__init__(ctxt)
        self.choices = choices

    def _get_inline_for_list(self):
        return ' '.join(shell.quote(str(c)) for c in self.choices)

    def _get_inline_for_dict(self):
        def str0(s):
            return str(s) if s is not None else ''

        stringified = {str(item): str0(desc) for item, desc in self.choices.items()}
        q = shell.quote
        r = ['%s\\t%s' % (q(item), q(desc)) for item, desc in stringified.items()]
        return ' '.join(r)

    def _get_code_for_list(self):
        code = "printf '%s\\n' \\\n"
        quoted = [shell.quote(str(item)) for item in self.choices]
        line_length = self.ctxt.config.line_length - 2
        code += indent(join_with_wrap(' ', ' \\\n', line_length, quoted), 2)
        return code.rstrip(' \\\n')

    def _get_code_for_dict(self):
        code = "printf '%s\\t%s\\n' \\\n"
        for item, desc in self.choices.items():
            if desc is None:
                desc = ''
            code += '  %s %s \\\n' % (shell.quote(str(item)), shell.quote(str(desc)))
        return code.rstrip(' \\\n')

    def get_args(self):
        if is_dict_type(self.choices):
            arg = self._get_inline_for_dict()
        else:
            arg = self._get_inline_for_list()

        if len(arg) <= CHOICES_INLINE_THRESHOLD:
            return ['-f', '-a', arg]

        func = self.get_function()
        return ['-f', '-a', '(%s)' % func]

    def get_code(self):
        if is_dict_type(self.choices):
            return self._get_code_for_dict()
        return self._get_code_for_list()


class ZshCompleteChoices(ZshCompletionBase):
    '''Complete from a set of words.'''

    def __init__(self, ctxt, trace, choices):
        self.ctxt = ctxt
        self.trace = trace
        self.choices = choices

    def _list_action_string(self):
        items = [str(item) for item in self.choices]
        quoted = [shell.quote(item) for item in items]
        action = shell.quote('(%s)' % ' '.join(quoted))
        if len(action) <= CHOICES_INLINE_THRESHOLD:
            return action

        return self._list_function()

    def _list_function(self):
        metavar = shell.quote(self.ctxt.option.metavar or '')
        quoted = [shell.quote(escape_colon(c)) for c in self.choices]
        line_length = self.ctxt.config.line_length - 2

        code = 'local items=(\n'
        code += indent(join_with_wrap(' ', '\n', line_length, quoted), 2)
        code += '\n)\n\n'
        code += f'_describe -- {metavar} items'

        funcname = self.ctxt.helpers.add_dynamic_func(self.ctxt, code)
        return funcname

    def _dict_action_string(self):
        def str0(s):
            return str(s) if s is not None else ''

        items = [str0(item) for item in self.choices.keys()]
        descriptions = [str0(value) for value in self.choices.values()]
        colon = any(':' in s for s in items + descriptions)
        quoted = []

        for item, desc in zip(items, descriptions):
            val = shell.quote(item)
            if desc:
                val += ':%s' % shell.quote(desc)
            quoted.append(val)

        action = shell.quote('((%s))' % ' '.join(quoted))
        if not colon and len(action) <= CHOICES_INLINE_THRESHOLD:
            return action

        return self._dict_function()

    def _dict_function(self):
        metavar = shell.quote(self.ctxt.option.metavar or '')

        code = 'local items=(\n'
        for item, desc in self.choices.items():
            item = shell.quote(escape_colon(str(item)))
            if desc:
                desc = shell.quote(str(desc))
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


def bash(_completer, ctxt, _trace, choices):
    '''Implement choices for bash'''
    return CompgenW(ctxt, choices)


def fish(_completer, ctxt, _trace, choices):
    '''Implement choices for fish'''
    return FishCompleteChoices(ctxt, choices)


def zsh(_completer, ctxt, trace, choices):
    '''Implement choices for zsh'''
    return ZshCompleteChoices(ctxt, trace, choices)
