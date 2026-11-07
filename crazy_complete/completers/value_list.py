# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2025-2026 Benjamin Abendroth <braph93@gmx.de>

'''Completer for a list of values.'''

from .. import shell
from ..bash_complete import BashCompletionFunc
from ..fish_complete import FishCompletionCommand
from ..zsh_complete import ZshComplFunc
from ..zsh_utils import escape_square_brackets
from ..type_utils import is_dict_type
from ..scheme_validator import (
    check_type, check_dictionary,
    check_char,
    check_non_empty_dict, check_non_empty_list)

CATEGORY = 'basic'

SYNOPSIS = r'''
['value_list', <OPTIONS>]
'''

SHORT = 'Complete comma-separated lists of values'

LONG = r'''
`OPTIONS`:
  A dictionary containing additional options for configuring the completion.

  - `values`:
    A list or dictionary containing the values to offer for completion.

    If a list is supplied, all values are offered without descriptions.

    If a dictionary is supplied, the keys are used as completion values and
    the values are used as descriptions.

  - `separator`:
    The separator used between list elements. Defaults to `,`.

  - `duplicates`:
    Allow duplicate values to be offered for completion. Defaults to `false`.
'''

ALSO = {
    'list': 'For completing comma-separated lists using a completer',
    'key_value_list': 'For completing comma-separated lists of key=value pairs',
}

DEFINITION = r'''
prog: 'example'
options:
  - option_strings: ['--value-list-1']
    complete: ['value_list', {'values': ['exec', 'noexec']}]

  - option_strings: ['--value-list-2']
    complete: ['value_list', {'values': {'one': 'Description 1', 'two': 'Description 2'}}]
'''

OUTPUT = r'''
~ > example --value-list-1=<TAB>
exec    noexec

~ > example --value-list-1=exec,<TAB>
noexec

~ > example --value-list-2=<TAB>
one  -- Description 1
two  -- Description 2
'''

def validate(_ctxt, arguments):
    '''Validate YAML for value_list completer'''
    options = arguments.get_required_arg('options')
    check_type(options, (dict,), 'options')
    arguments.require_no_more()

    check_dictionary(options, {
        'values':    (True,  (list, dict), None),
        'separator': (False, (str,), check_char),
        'duplicates': (False, (bool,), None),
    })

    values = options.value['values']

    if isinstance(values.value, dict):
        check_non_empty_dict(values, 'values')

        for i, (item, desc) in enumerate(values.value.items()):
            check_type(item, (str,), f'values[{i}]: item')
            check_type(desc, (str,), f'values[{i}]: description')
    else:
        check_non_empty_list(values, 'values')

        for i, value in enumerate(values.value):
            check_type(value, (str,), f'values[{i}]: item')


class FishCompleteValueList(FishCompletionCommand):
    '''Class for completing a list of values.'''

    def __init__(self, ctxt, opts):
        separator = opts.get('separator', ',')
        duplicates = opts.get('duplicates', False)
        values = opts['values']

        if is_dict_type(values):
            code = "printf '%s\\t%s\\n' \\\n"
            for item, desc in values.items():
                code += '  %s %s \\\n' % (shell.quote(item), shell.quote(desc))
            code = code.rstrip(' \\\n')
        else:
            code = "printf '%s\\n' \\\n"
            for value in values:
                code += '  %s \\\n' % shell.quote(value)
            code = code.rstrip(' \\\n')

        func = ctxt.helpers.add_dynamic_func(ctxt, code)

        if duplicates:
            super().__init__(ctxt, ['__fish_complete_list', separator, func])
        else:
            complete_list_func = ctxt.helpers.use_function('list')
            super().__init__(ctxt, [complete_list_func, separator, func])


def bash(_completer, ctxt, _trace, opts):
    '''Implement value_list for bash'''
    separator = opts.get('separator', ',')
    duplicates = opts.get('duplicates', False)
    values = opts['values']

    if is_dict_type(values):
        values = list(values.keys())

    args = [ctxt.helpers.use_function('value_list')]
    if duplicates:
        ctxt.helpers.use_function('value_list', 'duplicates')
        args.append('-d')
    args.append(separator)

    return BashCompletionFunc(ctxt, args + values)


def fish(_completer, ctxt, _trace, opts):
    '''Implement value_list for fish'''
    return FishCompleteValueList(ctxt, opts)


def zsh(_completer, ctxt, _trace, opts):
    '''Implement value_list for zsh'''
    desc = ctxt.option.metavar or ''
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
