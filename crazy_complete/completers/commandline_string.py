# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2025-2026 Benjamin Abendroth <braph93@gmx.de>

'''Completer for the string of the current command line.'''

from ..bash_complete import BashCompletionFunc
from ..fish_complete import FishCompletionCommand
from ..zsh_complete import ZshComplFunc
from ..helpers import ShellFunction
from ..helpers import FishFunction
from ..bash_helpers import BashHelpers
from ..fish_helpers import FishHelpers

CATEGORY = 'basic'

SHORT = 'Complete command lines as strings'

ALSO = {
    'command': 'For completing command names',
    'command_arg': 'For completing command arguments',
}

DEFINITION = r'''
prog: 'example'
options:
  - option_strings: ['--commandline']
    complete: ['commandline_string']
'''

OUTPUT = r'''
~ > example --commandline='sudo ba<TAB>
base32    base64    basename  basenc    bash      bashbug
'''

_COMMANDLINE_STRING_BASH = ShellFunction('commandline_string', r'''
local l line break_pos in_quotes
dequote "$cur" line break_pos in_quotes

local COMP_LINE_OLD="$COMP_LINE"
local COMP_POINT_OLD=$COMP_POINT
local COMP_WORDS_OLD=("${COMP_WORDS[@]}")
local COMP_CWORD_OLD=$COMP_CWORD

COMP_LINE="$line"
COMP_POINT=${#line}
COMP_WORDS=()
parse_line COMP_WORDS "$line"
COMP_CWORD=$(( ${#COMP_WORDS[@]} - 1 ))
COMPREPLY=()

#ifdef bash_completions_v_2_12
_comp_command_offset 0
#else
_command_offset 0
#endif
compopt -o nospace
compopt -o noquote

if (( break_pos >= 0 )); then
  line="${line:break_pos}"
fi

if (( ${#COMPREPLY[@]} )); then
  local len=$(get_prefix_suffix_len "$line" "${COMPREPLY[0]}")
  line="${line:0:len}"

  for i in "${!COMPREPLY[@]}"; do
    local REPLY="${COMPREPLY[i]}"
    if (( in_quotes )); then
      COMPREPLY[i]="$line$REPLY"
    else
      COMPREPLY[i]="$(printf '%q' "$line$REPLY")"
    fi
  done
fi

COMP_LINE="$COMP_LINE_OLD"
COMP_POINT=$COMP_POINT_OLD
COMP_WORDS=("${COMP_WORDS_OLD[@]}")
COMP_CWORD=$COMP_CWORD_OLD
''', ['dequote', 'parse_line', 'get_prefix_suffix_len'])

_COMMANDLINE_STRING_FISH = FishFunction('commandline_string', r'''
set -l line
set -l comp (get_completing_arg)

complete -C "$comp" | while read line
  set -l split (string split -m 1 -- \t $line)
  set -l comp2 (subtract_prefix_suffix "$comp" "$split[1]")
  printf '%s\t%s\n' "$comp2$split[1]" "$split[2]"
end''', ['subtract_prefix_suffix', 'get_completing_arg'])

BashHelpers.add_function(_COMMANDLINE_STRING_BASH)
FishHelpers.add_function(_COMMANDLINE_STRING_FISH)


def validate(_ctxt, arguments):
    '''Validate YAML for commandline_string completer'''
    arguments.require_no_more()


def bash(_completer, ctxt, _trace):
    '''Implement commandline_string for bash'''
    func = ctxt.helpers.use_function('commandline_string')
    return BashCompletionFunc(ctxt, [func])


def fish(_completer, ctxt, _trace):
    '''Implement commandline_string for fish'''
    func = ctxt.helpers.use_function('commandline_string')
    return FishCompletionCommand(ctxt, [func])


def zsh(_completer, ctxt, _trace):
    '''Implement commandline_string for zsh'''
    return ZshComplFunc(ctxt, ['_cmdstring'])
