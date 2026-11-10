# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2025-2026 Benjamin Abendroth <braph93@gmx.de>

'''Completer for filesystem UUIDs.'''

from ..bash_complete import BashCompletionFunc
from ..fish_complete import FishCompletionCommand
from ..zsh_complete import ZshComplFunc
from ..helpers import ShellFunction
from ..helpers import FishFunction
from ..bash_helpers import BashHelpers
from ..fish_helpers import FishHelpers
from ..zsh_helpers import ZshHelpers

CATEGORY = 'basic'

SHORT = 'Complete UUIDs of block device filesystems'

ALSO = {
    'filesystem_label': 'For completing filesystem labels',
    'partition_label': 'For completing partition labels',
    'partition_uuid': 'For completing partition UUIDs',
}

DEFINITION = r'''
prog: 'example'
options:
  - option_strings: ['--filesystem-uuid']
    complete: ['filesystem_uuid']
'''

OUTPUT = r'''
~ > example --filesystem-uuid=<TAB>
3C14-D029         (nvme0n1p1)
E4B21F0A          (nvme0n1p2)
a1b2c3d4e5f60718  (nvme0n1p4)
'''

_FILESYSTEM_UUID_LIST_BASH = ShellFunction('filesystem_uuid_list', r'''
local item items=()

while IFS= read -r item; do
  items+=("$item")
done < <(command lsblk -rno UUID,FSTYPE | command awk 'NF>=2 {print $1}' | command sort -u)

values -- "${items[@]}"
''', ['values'])

_FILESYSTEM_UUID_LIST_FISH = FishFunction('filesystem_uuid_list', r'''
set -l line
set -l cols

for line in (command lsblk -rno UUID,NAME,FSTYPE | command sort -u)
  set cols (string split -- ' ' $line)

  if test (count $cols) -eq 3; and test -n "$cols[1]"; and test -n "$cols[3]"
    printf "%s\t%s\n" "$cols[1]" "$cols[2]"
  end
end
''')

_FILESYSTEM_UUID_COMPLETE_ZSH = ShellFunction('filesystem_uuid_complete', r'''
local item='' desc='' describe=()

command lsblk -rno UUID,NAME,FSTYPE \
  | command awk 'NF>=3 && $3!="" && $1!="" {printf "%s\t%s\n",$1,$2}' \
  | command sort -u \
  | while IFS=$'\t' builtin read -r item desc; do
  item="${item//\\/\\\\}"
  item="${item//:/\\:}"
  desc="${desc//\\/\\\\}"
  [[ -n "$desc" ]] && describe+=("$item:$desc") || describe+=("$item")
done

_describe 'Filesystem uuid' describe
''')

BashHelpers.add_function(_FILESYSTEM_UUID_LIST_BASH)
FishHelpers.add_function(_FILESYSTEM_UUID_LIST_FISH)
ZshHelpers.add_function(_FILESYSTEM_UUID_COMPLETE_ZSH)


def validate(_ctxt, arguments):
    '''Validate YAML for filesystem_uuid completer'''
    arguments.require_no_more()


def bash(_completer, ctxt, _trace):
    '''Implement filesystem_uuid for bash'''
    func = ctxt.helpers.use_function('filesystem_uuid_list')
    return BashCompletionFunc(ctxt, [func])


def fish(_completer, ctxt, _trace):
    '''Implement filesystem_uuid for fish'''
    func = ctxt.helpers.use_function('filesystem_uuid_list')
    return FishCompletionCommand(ctxt, [func])


def zsh(_completer, ctxt, _trace):
    '''Implement filesystem_uuid for zsh'''
    func = ctxt.helpers.use_function('filesystem_uuid_complete')
    return ZshComplFunc(ctxt, [func], needs_braces=True)
