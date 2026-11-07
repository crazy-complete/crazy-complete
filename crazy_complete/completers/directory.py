# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2025-2026 Benjamin Abendroth <braph93@gmx.de>

'''Completer for directories.'''

from .. import shell
from .. import bash_versions
from ..bash_complete import BashCompletionCode, BashCompletionFunc
from ..fish_complete import FishCompletionCommand
from ..zsh_complete import ZshComplFunc
from . import _validate

CATEGORY = 'basic'

SYNOPSIS = r'''
['directory']

['directory', <OPTIONS>]
'''

SHORT = 'Complete directory names'

LONG = r'''
`OPTIONS`:
  A dictionary containing additional options for configuring the completion.

  - `directory`: Restrict completion to directories inside the specified directory.
'''

ALSO = {
    'directory_list': 'For completing comma-separated lists of directories',
}

DEFINITION = r'''
prog: 'example'
options:
  - option_strings: ['--directory']
    complete: ['directory']

  - option_strings: ['--directory-tmp']
    complete: ['directory', {'directory': '/tmp'}]
'''

OUTPUT = r'''
~ > example --directory=<TAB>
dir1/  dir2/
'''

def validate(ctxt, arguments):
    '''Validate YAML for directory completer'''
    _validate.check_filedir(ctxt, arguments)


class FishCompleteDirectory(FishCompletionCommand):
    '''Class for completing directories.'''

    def __init__(self, ctxt, trace, opts):
        directory = None if opts is None else opts.get('directory', None)

        # __fish_complete_directories does not respect __fish_stripprefix
        # which is used inside list/key_value_list/key_value_pair/prefix
        use_filedir = (
            'list' in trace or
            'key_value_list' in trace or
            'key_value_pair' in trace or
            'prefix' in trace or
            'suffix' in trace
        )

        if directory is not None:
            func = ctxt.helpers.use_function('filedir')
            super().__init__(ctxt, [func, '-D', '-C', directory])
        elif use_filedir:
            func = ctxt.helpers.use_function('filedir')
            super().__init__(ctxt, [func, '-D'])
        else:
            super().__init__(ctxt, ['__fish_complete_directories'])


def bash(_completer, ctxt, _trace, opts=None):
    '''Implement directory for bash'''
    directory = None if opts is None else opts.get('directory', None)
    filedir = bash_versions.filedir(ctxt)

    if directory:
        r = 'builtin pushd %s &>/dev/null && {\n' % shell.quote(directory)
        r += '  %s -d\n' % filedir
        r += '  builtin popd >/dev/null\n'
        r += '}'
        return BashCompletionCode(ctxt, r)

    return BashCompletionFunc(ctxt, [filedir, '-d'])


def fish(_completer, ctxt, trace, opts=None):
    '''Implement directory for fish'''
    return FishCompleteDirectory(ctxt, trace, opts)


def zsh(_completer, ctxt, _trace, opts=None):
    '''Implement directory for zsh'''
    directory = None if opts is None else opts.get('directory', None)

    if not directory:
        return ZshComplFunc(ctxt, ['_directories'])

    if directory.startswith('/'):
        return ZshComplFunc(ctxt, ['_directories', '-W', directory])

    func = ctxt.helpers.use_function('path_files_relative')
    return ZshComplFunc(ctxt, [func, directory, '-/'], needs_braces=True)
