'''This module contains helper functions for Bash.'''

from . import helpers

_COMPGEN_W_REPLACEMENT = helpers.ShellFunction('compgen_w_replacement', r'''
local cur word append=0

[[ "$1" == "-a" ]] && { shift; append=1; }
[[ "$1" == "--" ]] && { shift; }
cur="$1"; shift

(( append )) || COMPREPLY=()

for word; do
  if [[ "$word" == "$cur"* ]]; then
    COMPREPLY+=("$(printf '%q' "$word")")
  fi
done
''')

_MY_DEQUOTE = helpers.ShellFunction('my_dequote', r'''
local input="$1" result=''
local i=0 len=${#input}

for ((; i < len; ++i)); do
  case "${input:i:1}" in
    "'")
      for ((++i; i < len; ++i)); do
        [[ "${input:i:1}" == "'" ]] && break
        result+="${input:i:1}"
      done;;
    '"')
      for ((++i; i < len; ++i)); do
        [[ "${input:i:1}" == '"' ]] && break

        if [[ "${input:i:1}" == '\' ]]; then
          result+="${input:$((++i)):1}"
        else
          result+="${input:i:1}"
        fi
      done;;
    '\')
      result+="${input:$((++i)):1}";;
    *)
      result+="${input:i:1}";;
  esac
done

printf '%s\n' "$result"
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
local i prefix="$1"
for ((i=0; i < ${#COMPREPLY[@]}; ++i)); do
  COMPREPLY[i]="$prefix${COMPREPLY[i]}"
done
''')

_HISTORY = helpers.ShellFunction('history', r'''
[[ -f "$HISTFILE" ]] || return

local match

while read -r match; do
  if [[ "$match" == "$cur"* ]]; then
    COMPREPLY+=("$(printf '%q' "$match")")
  fi
done < <(command grep -E -o -- "$1" "$HISTFILE")
''')

_MIME_FILE = helpers.ShellFunction('mime_file', r'''
local line file mime i_opt cur_dequoted

if command file -i /dev/null &>/dev/null; then
  i_opt="-i"
elif command file -I /dev/null &>/dev/null; then
  i_opt="-I"
else
  _filedir
  return
fi

cur_dequoted="$(my_dequote "$cur")"

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
''', ['my_dequote'])

# =============================================================================
# Bonus
# =============================================================================

_NET_INTERFACES_LIST = helpers.ShellFunction('net_interfaces_list', r'''
if [[ -d /sys/class/net ]]; then
  command ls /sys/class/net
elif command ifconfig -l &>/dev/null; then
  command ifconfig -l # BSD / macOS
else
  command ifconfig 2>/dev/null | command awk '/^[a-z0-9]/ {print $1}' | command sed 's/://'
fi''')

_TIMEZONE_LIST = helpers.ShellFunction('timezone_list', r'''
if ! command timedatectl list-timezones 2>/dev/null; then
  command find /usr/share/zoneinfo -type f |\
  command sed 's|/usr/share/zoneinfo/||g'  |\
  command grep -E -v '^(posix|right)'
fi''')

_ALSA_LIST_CARDS = helpers.ShellFunction('alsa_list_cards', r'''
local card
command aplay -l \
  | command grep -Eo '^card [0-9]+: [^,]+' \
  | command uniq \
  | while builtin read card; do
  card="${card#card }"
  local id="${card%%: *}"
  builtin echo "$id"
done''')

_ALSA_LIST_DEVICES = helpers.ShellFunction('alsa_list_devices', r'''
local card
command aplay -l \
  | command grep -Eo '^card [0-9]+: [^,]+' \
  | command uniq \
  | while builtin read card; do
  card="${card#card }"
  local id="${card%%: *}"
  builtin echo "hw:$id"
done''')


class BashHelpers(helpers.GeneralHelpers):
    '''Class holding helper functions for Bash.'''

    def __init__(self, function_prefix):
        super().__init__(function_prefix, helpers.ShellFunction)
        self.add_function(_COMPGEN_W_REPLACEMENT)
        self.add_function(_MY_DEQUOTE)
        self.add_function(_EXEC)
        self.add_function(_EXEC_FAST)
        self.add_function(_VALUE_LIST)
        self.add_function(_PREFIX_COMPREPLY)
        self.add_function(_HISTORY)
        self.add_function(_MIME_FILE)
        self.add_function(_NET_INTERFACES_LIST)
        self.add_function(_TIMEZONE_LIST)
        self.add_function(_ALSA_LIST_CARDS)
        self.add_function(_ALSA_LIST_DEVICES)
