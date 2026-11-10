# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2025-2026 Benjamin Abendroth <braph93@gmx.de>

'''Completer for filesystem labels.'''

from ..bash_complete import BashCompletionFunc
from ..fish_complete import FishCompletionCommand
from ..zsh_complete import ZshComplFunc
from ..helpers import ShellFunction
from ..helpers import FishFunction
from ..bash_helpers import BashHelpers
from ..fish_helpers import FishHelpers
from ..zsh_helpers import ZshHelpers

CATEGORY = 'basic'

SHORT = 'Complete labels of block device filesystems'

ALSO = {
    'filesystem_uuid': 'For completing filesystem UUIDs',
    'partition_label': 'For completing partition labels',
    'partition_uuid': 'For completing partition UUIDs',
}

DEFINITION = r'''
prog: 'example'
options:
  - option_strings: ['--filesystem-label']
    complete: ['filesystem_label']
'''

OUTPUT = r'''
~ > example --filesystem-label=<TAB>
MyData    (nvme0n1p2)
Recovery  (nvme0n1p4)
root      (nvme0n1p1)
'''

_FILESYSTEM_LABEL_LIST_BASH = ShellFunction('filesystem_label_list', r'''
local item items=()

while IFS= read -r item; do
  items+=("$item")
done < <(command lsblk -rno LABEL,FSTYPE | command awk 'NF>=2 {print $1}' | command sort -u)

values -- "${items[@]}"
''', ['values'])

_FILESYSTEM_LABEL_LIST_FISH = FishFunction('filesystem_label_list', r'''
set -l line
set -l cols

for line in (command lsblk -rno LABEL,NAME,FSTYPE | command sort -u)
  set cols (string split -- ' ' $line)

  if test (count $cols) -eq 3; and test -n "$cols[1]"; and test -n "$cols[3]"
    printf "%s\t%s\n" "$cols[1]" "$cols[2]"
  end
end
''')

_FILESYSTEM_LABEL_COMPLETE_ZSH = ShellFunction('filesystem_label_complete', r'''
local item='' desc='' describe=()

command lsblk -rno LABEL,NAME,FSTYPE \
  | command awk 'NF>=3 && $3!="" && $1!="" {printf "%s\t%s\n",$1,$2}' \
  | command sort -u \
  | while IFS=$'\t' builtin read -r item desc; do
  item="${item//\\/\\\\}"
  item="${item//:/\\:}"
  desc="${desc//\\/\\\\}"
  [[ -n "$desc" ]] && describe+=("$item:$desc") || describe+=("$item")
done

_describe 'Filesystem label' describe
''')

BashHelpers.add_function(_FILESYSTEM_LABEL_LIST_BASH)
FishHelpers.add_function(_FILESYSTEM_LABEL_LIST_FISH)
ZshHelpers.add_function(_FILESYSTEM_LABEL_COMPLETE_ZSH)


def validate(_ctxt, arguments):
    '''Validate YAML for filesystem_label completer'''
    arguments.require_no_more()


def bash(_completer, ctxt, _trace):
    '''Implement filesystem_label for bash'''
    func = ctxt.helpers.use_function('filesystem_label_list')
    return BashCompletionFunc(ctxt, [func])


def fish(_completer, ctxt, _trace):
    '''Implement filesystem_label for fish'''
    func = ctxt.helpers.use_function('filesystem_label_list')
    return FishCompletionCommand(ctxt, [func])


def zsh(_completer, ctxt, _trace):
    '''Implement filesystem_label for zsh'''
    func = ctxt.helpers.use_function('filesystem_label_complete')
    return ZshComplFunc(ctxt, [func], needs_braces=True)
