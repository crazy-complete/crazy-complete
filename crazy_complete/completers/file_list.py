# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2025-2026 Benjamin Abendroth <braph93@gmx.de>

'''Completer for a list of files.'''

from . import _validate

CATEGORY = 'basic'

SYNOPSIS = r'''
['file_list']

['file_list', <OPTIONS>]
'''

SHORT = 'Complete comma-separated lists of files'

LONG = r'''
This is an alias for `['list', ['file']]`.

`OPTIONS`:
  A dictionary containing additional options for configuring the completion.

  - `directory`:
    Restrict completion to files inside the specified directory.

  - `extensions`:
    A list of file extensions to offer for completion.

  - `fuzzy`:
    Enable fuzzy extension matching. By default, files must end with one of
    the specified extensions. With fuzzy matching enabled, files with
    additional suffixes are also matched, for example `foo.txt.1`.

  - `ignore_globs`:
    A list of Bash globs for files that should not be offered for completion.

  - `duplicates`:
    Allow duplicate values to be offered for completion. Defaults to `false`.

  - `separator`:
    The separator used between list elements. Defaults to `,`.
'''

ALSO = {
    'list': 'For completing comma-separted lists using a completer',
    'file': 'For completing file names',
    'directory_list': 'For completing comma-separated lists of directories',
}

DEFINITION = r'''
prog: 'example'
options:
  - option_strings: ['--file-list']
    complete: ['file_list']
'''

OUTPUT = r'''
~ > example --file-list=file1,file2,<TAB>
file3  file4
'''

def validate(ctxt, arguments):
    '''Validate YAML for file_list completer'''
    _validate.check_filedir(
        ctxt, arguments, with_file_opts=True, with_list_opts=True)


def bash(completer, ctxt, trace, opts=None):
    '''Implement file_list for bash'''
    list_opts = {
        'separator': opts.pop('separator', ',') if opts else ',',
        'duplicates': opts.pop('duplicates', False) if opts else False
    }
    return completer.complete(ctxt, trace, 'list', ['file', opts], list_opts)


def fish(completer, ctxt, trace, opts=None):
    '''Implement file_list for fish'''
    list_opts = {
        'separator': opts.pop('separator', ',') if opts else ',',
        'duplicates': opts.pop('duplicates', False) if opts else False
    }
    return completer.complete(ctxt, trace, 'list', ['file', opts], list_opts)


def zsh(completer, ctxt, trace, opts=None):
    '''Implement file_list for zsh'''
    list_opts = {
        'separator': opts.pop('separator', ',') if opts else ',',
        'duplicates': opts.pop('duplicates', False) if opts else False
    }
    return completer.complete(ctxt, trace, 'list', ['file', opts], list_opts)
