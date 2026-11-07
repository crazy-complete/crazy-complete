# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2025-2026 Benjamin Abendroth <braph93@gmx.de>

'''Completer for ALSA sound devices.'''

from ..bash_complete import BashCompletionFunc
from ..fish_complete import FishCompletionCommand
from ..zsh_complete import ZshComplFunc
from ..helpers import ShellFunction
from ..helpers import FishFunction
from ..bash_helpers import BashHelpers
from ..fish_helpers import FishHelpers
from ..zsh_helpers import ZshHelpers

CATEGORY = 'basic'

SHORT = 'Complete ALSA devices'

ALSO = {
    'alsa_card': 'For completing ALSA cards',
}

DEFINITION = r'''
prog: 'example'
options:
  - option_strings: ['--alsa-device']
    complete: ['alsa_device']
'''

OUTPUT = r'''
~ > example --alsa-device=<TAB>
hw:0  hw:1
'''

_ALSA_LIST_DEVICES_BASH = ShellFunction('alsa_list_devices', r'''
local card id devices=()
while builtin read card; do
  card="${card#card }"
  id="${card%%: *}"
  devices+=("hw:$id")
done < <(command aplay -l | command grep -Eo '^card [0-9]+: [^,]+')

COMPREPLY=($(compgen -W "${devices[*]}" -- "$cur"))
''')

_ALSA_LIST_DEVICES_FISH = FishFunction('alsa_list_devices', r'''
set -l card

for card in (command aplay -l | string match -r '^card [0-9]+: [^,]+')
  set card (string replace 'card ' '' $card)
  set -l split (string split ': ' $card)

  if set -q split[2]
    printf "hw:%s\t%s\n" $split[1] $split[2]
  end
end
''')

_ALSA_COMPLETE_DEVICES_ZSH = ShellFunction('alsa_complete_devices', r'''
local card='' id='' name='' devices=()
command aplay -l \
  | command grep -Eo '^card [0-9]+: [^,]+' \
  | command uniq \
  | while builtin read card; do
  card="${card#card }"
  id="${card%%: *}"
  name="${card#*: }"
  devices+=("hw\\:$id:$name")
done

_describe 'ALSA device' devices
''')

BashHelpers.add_function(_ALSA_LIST_DEVICES_BASH)
FishHelpers.add_function(_ALSA_LIST_DEVICES_FISH)
ZshHelpers.add_function(_ALSA_COMPLETE_DEVICES_ZSH)


def validate(_ctxt, arguments):
    '''Validate YAML for alsa_device completer'''
    arguments.require_no_more()


def bash(_completer, ctxt, _trace):
    '''Implement alsa_device for bash'''
    func = ctxt.helpers.use_function('alsa_list_devices')
    return BashCompletionFunc(ctxt, [func])


def fish(_completer, ctxt, _trace):
    '''Implement alsa_device for fish'''
    func = ctxt.helpers.use_function('alsa_list_devices')
    return FishCompletionCommand(ctxt, [func])


def zsh(_completer, ctxt, _trace):
    '''Implement alsa_device for zsh'''
    func = ctxt.helpers.use_function('alsa_complete_devices')
    return ZshComplFunc(ctxt, [func], needs_braces=True)
