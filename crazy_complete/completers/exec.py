# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2025-2026 Benjamin Abendroth <braph93@gmx.de>

'''Completer that executes a shell command.'''

from ..bash_complete import BashCompletionFunc
from ..fish_complete import FishCompletionRawCommand
from ..zsh_complete import ZshComplFunc
from ..completers import _validate

CATEGORY = 'custom'

SYNOPSIS = r'''
['exec', <COMMAND>]
'''

SHORT = 'Complete values from the output of a command or function'

LONG = r'''
`COMMAND`:
  The command or function to execute. Its output must be formatted as tab-separated values:

```
<ITEM_1>\t<DESCRIPTION_1>
<ITEM_2>\t<DESCRIPTION_2>
[...]
```

Each line represents one completion candidate. The item and its description are separated by a tab character.
'''

ALSO = {
    'exec_fast': 'Faster implementation of exec',
    'exec_internal': "Use the shell's internal completion mechanisms",
}

NOTES = [
    'Functions can be put inside a file and included with `--include-file`',
]

DEFINITION = r'''
prog: 'example'
options:
  - option_strings: ['--exec']
    complete: ['exec', "printf '%s\\t%s\\n' 'Item 1' 'Description 1' 'Item 2' 'Description 2'"]
'''

OUTPUT = r'''
~ > example --exec=<TAB>
Item 1  (Description 1)  Item 2  (Description 2)
'''

def validate(ctxt, arguments):
    '''Validate YAML for exec completer'''
    _validate.check_exec(ctxt, arguments)


def bash(_completer, ctxt, _trace, command):
    '''Implement exec for bash'''
    func = ctxt.helpers.use_function('exec')
    return BashCompletionFunc(ctxt, [func, command])


def fish(_completer, ctxt, _trace, command):
    '''Implement exec for fish'''
    return FishCompletionRawCommand(ctxt, command)


def zsh(_completer, ctxt, _trace, command):
    '''Implement exec for zsh'''
    funcname = ctxt.helpers.use_function('exec')
    return ZshComplFunc(ctxt, [funcname, command], needs_braces=True)
