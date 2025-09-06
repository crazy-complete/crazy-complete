'''This module contains helper functions for Bash.'''

from . import helpers

_COMPGEN_W_REPLACEMENT = helpers.ShellFunction('compgen_w_replacement', r'''
local cur word append=0

[[ "$1" == "-a" ]] && { shift; append=1; }
[[ "$1" == "--" ]] && { shift; }

cur="$1"
shift

(( append )) || COMPREPLY=()

for word; do
  if [[ "$word" == "$cur"* ]]; then
    COMPREPLY+=("$(printf '%q' "$word")")
  fi
done
''')

_EXEC = helpers.ShellFunction('exec', r'''
local item desc

while IFS=$'\t' read -r item desc; do
  if [[ "$item" == "$cur"* ]]; then
    COMPREPLY+=("$(printf '%q' "$item")")
  fi
done < <(eval "$1")
''')

_EXEC_FAST = helpers.ShellFunction('exec_fast', r'''
local item desc

while IFS=$'\t' read -r item desc; do
  if [[ "$item" == "$cur"* ]]; then
    COMPREPLY+=("$item")
  fi
done < <(eval "$1")
''')

_VALUE_LIST = helpers.ShellFunction('value_list', r'''
local separator="$1"; shift

if [[ -z "$cur" ]]; then
  COMPREPLY=("$@")
  return
fi

local value having_value found_value
local -a having_values remaining_values

IFS="$separator" read -r -a having_values <<< "$cur"

for value; do
  found_value=0

  for having_value in "${having_values[@]}"; do
    if [[ "$value" == "$having_value" ]]; then
      found_value=1
      break
    fi
  done

  if (( ! found_value )); then
    remaining_values+=("$value")
  fi
done

COMPREPLY=()

if [[ "${cur: -1}" == "$separator" ]]; then
  for value in "${remaining_values[@]}"; do
    COMPREPLY+=("$cur$value")
  done
elif (( ${#having_values[@]} )); then
  local cur_last_value=${having_values[-1]}

  for value in "${remaining_values[@]}"; do
    if [[ "$value" == "$cur_last_value"* ]]; then
      COMPREPLY+=("${cur%"$cur_last_value"}$value")
    fi
  done
fi
''')

_PREFIX_COMPREPLY = helpers.ShellFunction('prefix_compreply', r'''
local i=0 prefix="$1"
for ((i=0; i < ${#COMPREPLY[@]}; ++i)); do
  COMPREPLY[i]="$prefix${COMPREPLY[i]}"
done
''')

class BashHelpers(helpers.GeneralHelpers):
    def __init__(self, function_prefix):
        super().__init__(function_prefix)
        self.add_function(_COMPGEN_W_REPLACEMENT)
        self.add_function(_EXEC)
        self.add_function(_EXEC_FAST)
        self.add_function(_VALUE_LIST)
        self.add_function(_PREFIX_COMPREPLY)
