# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2025-2026 Benjamin Abendroth <braph93@gmx.de>

'''Completer for a list of directories.'''

from . import _validate

CATEGORY = 'basic'

SYNOPSIS = r'''
['directory_list']

['directory_list', <OPTIONS>]
'''

SHORT = 'Complete comma-separated lists of directories'

LONG = r'''
This is an alias for `['list', ['directory']]`.

`OPTIONS`:
  A dictionary containing additional options for configuring the completion.

  - `directory`:
    Restrict completion to directories inside the specified directory.

  - `duplicates`:
    Allow duplicate values to be offered for completion. Defaults to `false`.

  - `separator`:
    The separator used between list elements. Defaults to `,`.
'''

ALSO = {
    'list': 'For completion comma-separated lists using a completer',
    'directory': 'For completing directory names',
    'file_list': 'For completing comma-separated lists of files',
}

DEFINITION = r'''
prog: 'example'
options:
  - option_strings: ['--directory-list']
    complete: ['directory_list']
'''

OUTPUT = r'''
~ > example --directory-list=directory1,directory2,<TAB>
directory3  directory4
'''

def validate(ctxt, arguments):
    '''Validate YAML for directory_list completer'''
    _validate.check_filedir(ctxt, arguments, with_list_opts=True)


def bash(completer, ctxt, trace, opts=None):
    '''Implement directory_list for bash'''
    list_opts = {
        'separator': opts.pop('separator', ',') if opts else ',',
        'duplicates': opts.pop('duplicates', False) if opts else False
    }
    return completer.complete(
        ctxt, trace, 'list', ['directory', opts], list_opts)


def fish(completer, ctxt, trace, opts=None):
    '''Implement directory_list for fish'''
    list_opts = {
        'separator': opts.pop('separator', ',') if opts else ',',
        'duplicates': opts.pop('duplicates', False) if opts else False
    }
    return completer.complete(
        ctxt, trace, 'list', ['directory', opts], list_opts)


def zsh(completer, ctxt, trace, opts=None):
    '''Implement directory_list for zsh'''
    list_opts = {
        'separator': opts.pop('separator', ',') if opts else ',',
        'duplicates': opts.pop('duplicates', False) if opts else False
    }
    return completer.complete(
        ctxt, trace, 'list', ['directory', opts], list_opts)
