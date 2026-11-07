# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2025-2026 Benjamin Abendroth <braph93@gmx.de>

'''Completer that executes a shell command internally.'''

from ..bash_complete import BashCompletionCode
from ..fish_complete import FishCompletionRawCommand
from ..zsh_complete import ZshComplFunc
from ..completers import _validate

CATEGORY = 'custom'

SYNOPSIS = r'''
['exec_internal', <COMMAND>]
'''

SHORT = "Use the shell's internal completion mechanisms"

LONG = r'''
Execute a function that internally modifies the completion state.

This is useful if a more advanced completion is needed.

For **Bash**, it might look like:

```sh
my_completion_func() {
    COMPREPLY=( $(compgen -W 'read write append' -- '$cur') )
}
```

For **Zsh**, it might look like:

```sh
my_completion_func() {
    local items=(
        read:'Read data from a file'
        write:'Write data from a file'
        append:'Append data to a file'
    )

    _describe 'my items' items
}
```

For **Fish**, it might look like:

```sh
function my_completion_func
    printf '%s\t%s\n' \
        read 'Read data from a file'  \
        write 'Write data from a file' \
        append 'Append data to a file'
end
```
'''

NOTES = [
    'Functions can be put inside a file and included with `--include-file`',
]

DEFINITION = r'''
prog: 'example'
options:
  - option_strings: ['--exec-internal']
    complete: ['exec_internal', 'my_completion_func']
'''

OUTPUT = r'''
~ > example --exec-internal=<TAB>
append  -- Append data to a file
read    -- Read data from a file
write   -- Write data from a file
'''

def validate(ctxt, arguments):
    '''Validate YAML for exec_internal completer'''
    _validate.check_exec(ctxt, arguments)


def bash(_completer, ctxt, _trace, command):
    '''Implement exec_internal for bash'''
    return BashCompletionCode(ctxt, command)


def fish(_completer, ctxt, _trace, command):
    '''Implement exec_internal for fish'''
    return FishCompletionRawCommand(ctxt, command)


def zsh(_completer, ctxt, _trace, command):
    '''Implement exec_internal for zsh'''
    return ZshComplFunc(ctxt, [command], needs_braces=True)
