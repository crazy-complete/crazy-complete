# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2025-2026 Benjamin Abendroth <braph93@gmx.de>

'''Completer for files matching a MIME type pattern.'''

from ..bash_complete import BashCompletionFunc
from ..fish_complete import FishCompletionCommand
from ..zsh_complete import ZshComplFunc
from ..scheme_validator import check_type, check_regex
from ..helpers import ShellFunction
from ..helpers import FishFunction
from ..bash_helpers import BashHelpers
from ..fish_helpers import FishHelpers
from ..zsh_helpers import ZshHelpers

CATEGORY = 'basic'

SYNOPSIS = r'''
['mime_file', <MIME_REGEX>]
'''

SHORT = 'Complete files by MIME type'

LONG = r'''
`MIME_REGEX`:
  An extended regular expression used to match MIME types.
  The expression is passed to `grep -E` to filter the results.
'''

DEFINITION = r'''
prog: 'example'
options:
  - option_strings: ['--image']
    complete: ['mime_file', 'image/']
'''

OUTPUT = r'''
~ > example --image=<TAB>
dir1/  dir2/  img.png  img.jpg
'''

_MIME_FILE_BASH = ShellFunction('mime_file', r'''
local line file mime i_opt cur_dequoted

if command file -i /dev/null &>/dev/null; then
  i_opt="-i"
elif command file -I /dev/null &>/dev/null; then
  i_opt="-I"
else
#ifdef bash_completions_v_2_12
  _comp_compgen_filedir
#else
  _filedir
#endif
  return
fi

local cur_dequoted break_pos in_quotes
dequote "$cur" cur_dequoted break_pos in_quotes

while read -r line; do
  mime="${line##*:}"

  if [[ "$mime" == *inode/directory* ]] || command grep -q -E -- "$1" <<< "$mime"; then
    file="${line%:*}"

    if [[ "$file" == *\\* ]]; then
      file="$(command perl -pe 's/\\([0-7]{3})/chr(oct($1))/ge' <<< "$file")"
    fi

    if [[ "$mime" == *inode/directory* ]]; then
      file="$file/"
    fi

    if [[ "$file" == "$cur_dequoted"* ]]; then
      COMPREPLY+=("$(printf '%q' "$file")")
    fi
  fi
done < <(command file -L $i_opt -- "$cur_dequoted"* 2>/dev/null)
''', ['dequote'])

_MIME_FILE_FISH = FishFunction('mime_file', r'''
set -l i_opt

set -l comp (get_completing_arg)

if command file -i /dev/null &>/dev/null
  set i_opt '-i'
else if command file -I /dev/null &>/dev/null
  set i_opt '-I'
else
  complete -C"'' $comp"
  return
end

set -l line
command file -L $i_opt -- "$comp"* 2>/dev/null | while read line
  set -l split (string split -m 1 -r ':' "$line")

  if string match -q -- '*inode/directory*' $split[2]
    printf '%s/\n' "$split[1]"
  else if begin; echo "$split[2]" | command grep -q -E -- $argv[1]; end
    printf '%s\n' "$split[1]"
  end
end
''', ['get_completing_arg'])

_MIME_FILE_ZSH = ShellFunction('mime_file', r'''
local line='' file='' mime='' i_opt=''

if command file -i /dev/null &>/dev/null; then
  i_opt="-i"
elif command file -I /dev/null &>/dev/null; then
  i_opt="-I"
else
  compadd -- "$PREFIX"*
  return
fi

command file -L $i_opt -- "$PREFIX"* 2>/dev/null | while read -r line; do
  mime="${line##*:}"

  if [[ "$mime" == *inode/directory* ]] || command grep -q -E -- "$1" <<< "$mime"; then
    file="${line%:*}"

    if [[ "$file" == *\\* ]]; then
      file="$(command perl -pe 's/\\([0-7]{3})/chr(oct($1))/ge' <<< "$file")"
    fi

    if [[ "$mime" == *inode/directory* ]]; then
      compadd -- "$file/"
    else
      compadd -- "$file"
    fi
  fi
done
''')

BashHelpers.add_function(_MIME_FILE_BASH)
FishHelpers.add_function(_MIME_FILE_FISH)
ZshHelpers.add_function(_MIME_FILE_ZSH)


def validate(_ctxt, arguments):
    '''Validate YAML for mime_file completer'''
    pattern = arguments.get_required_arg("pattern")
    check_type(pattern, (str,), "pattern")
    arguments.require_no_more()
    check_regex(pattern, 'pattern')


def bash(_completer, ctxt, _trace, pattern):
    '''Implement mime_file for bash'''
    func = ctxt.helpers.use_function('mime_file')
    return BashCompletionFunc(ctxt, [func, pattern])


def fish(_completer, ctxt, _trace, pattern):
    '''Implement mime_file for fish'''
    func = ctxt.helpers.use_function('mime_file')
    return FishCompletionCommand(ctxt, [func, pattern])


def zsh(_completer, ctxt, _trace, pattern):
    '''Implement mime_file for zsh'''
    func = ctxt.helpers.use_function('mime_file')
    return ZshComplFunc(ctxt, [func, pattern], needs_braces=True)
