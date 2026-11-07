# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2025-2026 Benjamin Abendroth <braph93@gmx.de>

'''Completer for ALSA sound cards.'''

from ..bash_complete import BashCompletionFunc
from ..fish_complete import FishCompletionCommand
from ..zsh_complete import ZshComplFunc
from ..helpers import ShellFunction
from ..helpers import FishFunction
from ..bash_helpers import BashHelpers
from ..fish_helpers import FishHelpers
from ..zsh_helpers import ZshHelpers

CATEGORY = 'basic'

SHORT = 'Complete ALSA cards'

ALSO = {
    'alsa_device': 'For completing ALSA devices',
}

DEFINITION = r'''
prog: 'example'
options:
  - option_strings: ['--alsa-card']
    complete: ['alsa_card']
'''

OUTPUT = r'''
~ > example --alsa-card=<TAB>
0  1
'''

_ALSA_LIST_CARDS_BASH = ShellFunction('alsa_list_cards', r'''
local card id cards=()
while builtin read card; do
  card="${card#card }"
  id="${card%%: *}"
  cards+=("$id")
done < <(command aplay -l | command grep -Eo '^card [0-9]+: [^,]+')

COMPREPLY=($(compgen -W "${cards[*]}" -- "$cur"))
''')

_ALSA_LIST_CARDS_FISH = FishFunction('alsa_list_cards', r'''
set -l card

for card in (command aplay -l | string match -r '^card [0-9]+: [^,]+')
  set card (string replace 'card ' '' $card)
  set -l split (string split ': ' $card)

  if set -q split[2]
    printf "%s\t%s\n" $split[1] $split[2]
  end
end
''')

_ALSA_COMPLETE_CARDS_ZSH = ShellFunction('alsa_complete_cards', r'''
local card='' cards=()
command aplay -l \
  | command grep -Eo '^card [0-9]+: [^,]+' \
  | command uniq \
  | while builtin read card; do
  card="${card#card }"
  local id="${card%%: *}"
  local name="${card#*: }"
  cards+=("$id:$name")
done

_describe 'ALSA card' cards
''')

BashHelpers.add_function(_ALSA_LIST_CARDS_BASH)
FishHelpers.add_function(_ALSA_LIST_CARDS_FISH)
ZshHelpers.add_function(_ALSA_COMPLETE_CARDS_ZSH)


def validate(_ctxt, arguments):
    '''Validate YAML for alsa_card completer'''
    arguments.require_no_more()


def bash(_completer, ctxt, _trace):
    '''Implement alsa_card for bash'''
    func = ctxt.helpers.use_function('alsa_list_cards')
    return BashCompletionFunc(ctxt, [func])


def fish(_completer, ctxt, _trace):
    '''Implement alsa_card for fish'''
    func = ctxt.helpers.use_function('alsa_list_cards')
    return FishCompletionCommand(ctxt, [func])


def zsh(_completer, ctxt, _trace):
    '''Implement alsa_card for zsh'''
    func = ctxt.helpers.use_function('alsa_complete_cards')
    return ZshComplFunc(ctxt, [func], needs_braces=True)
