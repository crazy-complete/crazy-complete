# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2025-2026 Benjamin Abendroth <braph93@gmx.de>

'''Completer for a list of values provided by another completer.'''

from .. import shell
from ..bash_complete import BashCompletionCode
from ..fish_complete import FishCompletionCommand
from ..zsh_complete import ZshComplFunc
from ..scheme_validator import (
    check_type, check_dictionary, check_char, check_complete)

SHORT = 'Complete comma-separated lists using a completer'

SYNOPSIS = r'''
['list', <COMPLETER>]

['list', <COMPLETER>, <OPTIONS>]
'''

CATEGORY = 'meta'

LONG = r'''
`COMPLETER`:
  The completer used to generate the list elements.

`OPTIONS`:
  A dictionary containing additional options for configuring the list completion.

  - `separator`: The separator used between list elements. Defaults to `,`

  - `duplicates`: Allow duplicate values to be offered for completion. Defaults to `false`
'''

ALSO = {
    'value_list': 'For completing comma-separated lists of values',
    'file_list': 'For completing comma-separated lists of files',
    'directory_list': 'For completing comma-separated lists of directories',
    'key_value_list': 'For completing comma-separated lists of key=value pairs',
}

DEFINITION = r'''
prog: 'example'
options:
  - option_strings: ['--user-list']
    complete: ['list', ['user']]

  - option_strings: ['--option-list']
    complete: ['list', ['choices', ['setuid', 'async', 'block']], {'separator': ':', 'duplicates': true}]
'''

OUTPUT = r'''
~ > example --user-list=avahi,daemon,<TAB>
bin       braph
colord    dbus
dhcpcd    git
[...]

~ > example --option-list=setuid:<TAB>
setuid     async    block
'''

def validate(ctxt, arguments):
    '''Validate YAML for list completer'''
    command = arguments.get_required_arg('command')
    options = arguments.get_optional_arg({})
    arguments.require_no_more()

    check_type(command, (list,), 'command')
    check_type(options, (dict,), 'options')

    check_dictionary(options, {
        'separator': (False, (str,), check_char),
        'duplicates': (False, (bool,), None),
    })

    ctxt.trace.append('list')
    check_complete(ctxt, command)


def bash(completer, ctxt, trace, command, opts=None):
    '''Implement list for bash'''
    separator = opts.get('separator', ',') if opts else ','
    duplicates = opts.get('duplicates', False) if opts else False

    obj = completer.complete_from_def(ctxt, trace, command)
    code = obj.get_code()

    func = ctxt.helpers.use_function('value_list')

    dup_arg = ''
    if duplicates:
        ctxt.helpers.use_function('value_list', 'duplicates')
        dup_arg = ' -d'

    r = 'local cur_old="$cur"\n'
    r += 'cur="${cur##*%s}"\n' % shell.quote(separator)
    r += '%s\n' % code
    r += 'cur="$cur_old"\n'
    r += '%s%s %s "${COMPREPLY[@]}"' % (func, dup_arg, shell.quote(separator))
    return BashCompletionCode(ctxt, r)


def fish(completer, ctxt, trace, command, opts=None):
    '''Implement list for fish'''
    separator = opts.get('separator', ',') if opts else ','
    duplicates = opts.get('duplicates', False) if opts else False
    trace.append('list')

    obj = completer.complete_from_def(ctxt, trace, command)
    func = obj.get_function()

    list_func = ctxt.helpers.use_function('list')
    if not duplicates:
        return FishCompletionCommand(ctxt, [list_func, separator, func])

    return FishCompletionCommand(ctxt, [list_func, '-d', separator, func])


def zsh(completer, ctxt, trace, command, opts=None):
    '''Implement list for zsh'''
    separator = opts.get('separator', ',') if opts else ','
    duplicates = opts.get('duplicates', False) if opts else False
    trace.append('list')

    obj = completer.complete_from_def(ctxt, trace, command)
    func = obj.get_function()

    args = []

    if separator != ',':
        args.extend(['-s', separator])

    if duplicates:
        args.append('-d')

    return ZshComplFunc(ctxt, ['_sequence', *args, func])
