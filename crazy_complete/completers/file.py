# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2025-2026 Benjamin Abendroth <braph93@gmx.de>

'''Completer for files.'''

from .. import shell
from .. import bash_versions
from ..bash_complete import BashCompletionCode, BashCompletionFunc
from ..bash_utils import make_file_extension_pattern as make_bash_ext_pattern
from ..fish_complete import FishCompletionBase, FishCompletionCommand
from ..pattern import bash_glob_to_regex, bash_glob_to_zsh_glob
from ..zsh_complete import ZshComplFunc
from ..zsh_utils import make_file_extension_pattern as make_zsh_ext_pattern
from . import _validate
from ..helpers import ShellFunction
from ..bash_helpers import BashHelpers

CATEGORY = 'basic'

SYNOPSIS = r'''
['file']

['file', <OPTIONS>]
'''

SHORT = 'Complete file names'

LONG = r'''
`OPTIONS`:
  A dictionary containing additional options for configuring the completion.

  - `directory`: Restrict completion to files inside the specified directory.

  - `extensions`: A list of file extensions to offer for completion.

  - `fuzzy`:
    Enable fuzzy extension matching.
    By default, files must end with one of the specified extensions.
    With fuzzy matching enabled, files with additional suffixes are also matched, for example `foo.txt.1`.
  
  - `ignore_globs`:
    A list of Bash globs for files that should not be offered for completion.

**NOTE:** Restricting completion to specific file extensions only makes sense
if the program being completed actually expects files of those types. On
Unix-like systems, file extensions generally have no inherent meaning and are
only conventions.
'''

ALSO = {
    'file_list': 'For completing comma-separated lists of files',
    'mime_file': 'For completing files by MIME type',
}

DEFINITION = r'''
prog: 'example'
options:
  - option_strings: ['--file']
    complete: ['file']

  - option_strings: ['--file-tmp']
    complete: ['file', {'directory': '/tmp'}]

  - option_strings: ['--file-ext']
    complete: ['file', {'extensions': ['c', 'cpp']}]

  - option_strings: ['--file-ignore']
    complete: ['file', {'ignore_globs': ['*.[tT][xX][tT]', '*.c++']}]
'''

OUTPUT = r'''
~ > example --file=<TAB>
dir1/  dir2/  file1  file2

~ > example --file-ext=<TAB>
dir1/  dir2/  file.c  file.cpp
'''

_FILE_FILTER_BASH = ShellFunction('file_filter', '''
local pattern REPLY COMPREPLY_OLD=("${COMPREPLY[@]}")

COMPREPLY=()

for REPLY in "${COMPREPLY_OLD[@]}"; do
  for pattern; do
    [[ "${REPLY##*/}" == $pattern ]] && continue 2
  done

  COMPREPLY+=("$REPLY")
done
''')

BashHelpers.add_function(_FILE_FILTER_BASH)


def validate(ctxt, arguments):
    '''Validate YAML for file completer'''
    _validate.check_filedir(ctxt, arguments, with_file_opts=True)


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
        ignore_globs = None
        self.args = []

        if opts:
            fuzzy = opts.get('fuzzy', False)
            directory = opts.get('directory', None)
            extensions = opts.get('extensions', None)
            ignore_globs = opts.get('ignore_globs', None)

        if directory:
            self.args.extend(['-C', directory])

        if extensions:
            ctxt.helpers.use_function('filedir', 'regex')
            self.args.extend(['-r', _get_extension_regex(extensions, fuzzy)])

        if ignore_globs:
            ctxt.helpers.use_function('filedir', 'regex_ignore')
            patterns = map(bash_glob_to_regex, ignore_globs)
            patterns = [f'({p})' for p in patterns]
            self.args.extend(['-i', '|'.join(patterns)])

    def get_args(self):
        if len(self.args) == 0:
            return ['-F']

        func = self.ctxt.helpers.use_function('filedir')
        return FishCompletionCommand(self.ctxt, [func] + self.args).get_args()

    def get_code(self):
        func = self.ctxt.helpers.use_function('filedir')
        return FishCompletionCommand(self.ctxt, [func] + self.args).get_code()

    def get_function(self):
        func = self.ctxt.helpers.use_function('filedir')
        return FishCompletionCommand(self.ctxt, [func] + self.args).get_function()


def bash(_completer, ctxt, _trace, opts=None):
    '''Implement file for bash'''
    fuzzy = False
    directory = None
    extensions = None
    ignore_globs = None

    if opts:
        fuzzy = opts.get('fuzzy', False)
        directory = opts.get('directory', None)
        extensions = opts.get('extensions', None)
        ignore_globs = opts.get('ignore_globs', None)

    args = [bash_versions.filedir(ctxt)]

    if extensions:
        args.append(make_bash_ext_pattern(extensions, fuzzy))

    if not directory and not ignore_globs:
        return BashCompletionFunc(ctxt, args)

    if directory:
        r = 'builtin pushd %s &>/dev/null && {\n' % shell.quote(directory)
        r += '  %s\n' % shell.join_quoted(args)
        r += '  builtin popd >/dev/null\n'
        r += '}'
    else:
        r = shell.join_quoted(args)

    if ignore_globs:
        func = ctxt.helpers.use_function('file_filter')
        r += '\n%s %s' % (func, shell.join_quoted(ignore_globs))

    return BashCompletionCode(ctxt, r)


def fish(_completer, ctxt, _trace, opts=None):
    '''Implement file for fish'''
    return FishCompleteFile(ctxt, opts)


def zsh(_completer, ctxt, _trace, opts=None):
    '''Implement file for zsh'''
    fuzzy = False
    directory = None
    extensions = None
    ignore_globs = None

    if opts:
        fuzzy = opts.get('fuzzy', False)
        directory = opts.get('directory', None)
        extensions = opts.get('extensions', None)
        ignore_globs = opts.get('ignore_globs', None)

    args = []

    if extensions:
        args.extend(['-g', make_zsh_ext_pattern(extensions, fuzzy)])

    if ignore_globs:
        patterns = map(bash_glob_to_zsh_glob, ignore_globs)
        args.extend(['-F', '(%s)' % ' '.join(patterns)])

    if not directory:
        return ZshComplFunc(ctxt, ['_files'] + args)

    if directory.startswith('/'):
        return ZshComplFunc(ctxt, ['_files', '-W', directory, *args])

    func = ctxt.helpers.use_function('path_files_relative')
    return ZshComplFunc(ctxt, [func, directory, *args], needs_braces=True)
