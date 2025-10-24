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

_PARSE_LINE = helpers.ShellFunction('parse_line', r'''
local -n out="$1"
local in="$2" len=${#2} i=0 word='' active=0

if (( len == 0 )); then
  out+=('')
  return
fi

for ((i=0; i < len; ++i)); do
  case "${in:i:1}" in
    ' ')
      if (( active )); then
        out+=("$word")
        word=''
        active=0;
      fi;;
    '"')
      for ((; i < len; ++i)); do
        if [[ "${in:i:1}" == '\' ]]; then
          word+="${in:$((++i)):1}"
        else
          word+="${in:i:1}"
          [[ "${in:i:1}" == '"' ]] && break;
        fi
      done
      active=1;;
    "'")
      for ((; i < len; ++i)); do
        word+="${in:i:1}"
        [[ "${in:i:1}" == "'" ]] && break;
      done
      active=1;;
    '\')
      word+='\'
      word+="${in:$((++i)):1}"
      active=1;;
    *)
      word+="${in:i:1}"
      active=1;;
  esac
done

if (( active )); then
  out+=("$word")
elif [[ "${in:$((len - 1)):1}" == ' ' ]]; then
  out+=('')
fi
''')

_SUBSTRACT_PREFIX_SUFFIX = helpers.ShellFunction('subtract_prefix_suffix', r'''
local s1="$1"
local s2="$2"

local len1=${#s1}
local len2=${#s2}

local maxk=$len1
if (( len2 < maxk )); then
  maxk=$len2
fi

local k=$maxk
while (( k > 0 )); do
  local start=$((len1 - k))
  local suf="${s1:start:k}"
  local pre="${s2:0:k}"

  if [[ "$suf" == "$pre" ]]; then
    if (( len1 == k )); then
      echo ""
    else
      echo "${s1:0:len1-k}"
    fi

    return
  fi

  ((k--))
done

echo "$s1"
''')

_COMMANDLINE_STRING = helpers.ShellFunction('commandline_string', r'''
local quoted=0
[[ "${cur:0:1}" == '"' ]] && quoted=1
[[ "${cur:0:1}" == "'" ]] && quoted=1

local l line="$(my_dequote "$cur")"

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

if (( COMP_CWORD == 0 )); then
  local cur="${COMP_WORDS[0]}"
  if [[ "${cur:0:1}" == [./] ]]; then
#ifdef bash_completions_v_2_12
    _comp_compgen_filedir
#else
    _filedir
#endif
  else
    COMPREPLY=($(compgen -A command -- "$cur"))
  fi
else
#ifdef bash_completions_v_2_12
  _comp_command_offset 0
#else
  _command_offset 0
#endif

  local REPLY COMPREPLY_NEW=()

  for REPLY in "${COMPREPLY[@]}"; do
    l="$(subtract_prefix_suffix "$line" "$REPLY")"
    if (( quoted )); then
      COMPREPLY_NEW+=("$l$REPLY")
    else
      COMPREPLY_NEW+=("$(printf '%q' "$l$REPLY")")
    fi
  done

  COMPREPLY=("${COMPREPLY_NEW[@]}")
fi

COMP_LINE="$COMP_LINE_OLD"
COMP_POINT=$COMP_POINT_OLD
COMP_WORDS=("${COMP_WORDS_OLD[@]}")
COMP_CWORD=$COMP_CWORD_OLD
''', ['my_dequote', 'parse_line', 'subtract_prefix_suffix'])

_INVOKE_COMPLETE = helpers.ShellFunction('invoke_complete', r'''
local prog="${1##*/}"; shift

#ifdef bash_completions_v_2_12
_comp_complete_load "$prog"
#else
_completion_loader "$prog"
#endif

local i=0 args=($(complete -p -- "$prog"))

for ((; i < ${#args[@]}; ++i)); do
  if [[ "${args[i]}" == '-F' ]]; then
    "${args[i+1]}" "$@"
    return
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
local duplicates=0
[[ "$1" == '-d' ]] && { duplicates=1; shift; }

local separator="$1"; shift

cur="$(my_dequote "$cur")"

if [[ -z "$cur" ]]; then
  COMPREPLY=("$@")
  return
fi

local value having_value found_value
local -a having_values remaining_values

IFS="$separator" read -r -a having_values <<< "$cur"

if (( duplicates )); then
  remaining_values=("$@")
else
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
fi

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
''', ['my_dequote'])

_KEY_VALUE_LIST = helpers.ShellFunction('key_value_list', r'''
local sep1="$1"; shift
local sep2="$1"; shift
local -A keys=()
local i

for ((i=1; i <= $#; i += 2)); do
  keys["${@:i:1}"]="${@:i + 1:1}"
done

local strip_chars=''
[[ "$COMP_WORDBREAKS" == *"$sep1"* ]] && strip_chars+="$sep1"
[[ "$COMP_WORDBREAKS" == *"$sep2"* ]] && strip_chars+="$sep2"
[[ "${cur:0:1}" == '"' ]] && strip_chars=''
[[ "${cur:0:1}" == "'" ]] && strip_chars=''
cur="$(my_dequote "$cur")"

if [[ -z "$cur" ]]; then
  COMPREPLY=("${!keys[@]}")
  return
fi

local pair key value found_key cur_stripped="$cur"
local -a having_pairs having_keys remaining_keys

IFS="$sep1" read -r -a having_pairs <<< "$cur"

for pair in "${having_pairs[@]}"; do
  having_keys+=("${pair%%"$sep2"*}")
done

for key in "${!keys[@]}"; do
  found_key=0

  for having_key in "${having_keys[@]}"; do
    if [[ "$key" == "$having_key" ]]; then
      found_key=1
      break
    fi
  done

  if (( ! found_key )); then
    remaining_keys+=("$key")
  fi
done

COMPREPLY=()

if [[ "${cur: -1}" == "$sep1" ]]; then
  [[ -n "$strip_chars" ]] && cur_stripped="${cur_stripped##*[$strip_chars]}"

  for key in "${remaining_keys[@]}"; do
    COMPREPLY+=("$cur_stripped$key")
  done
else
  pair="${cur##*"$sep1"}"
  if [[ "$pair" == *"$sep2"* ]]; then
    key="${pair%%"$sep2"*}"
    value="${pair##*"$sep2"}"
    cur="$value"
    ${keys[$key]}

    cur_stripped="${cur_stripped:0:$(( ${#cur_stripped} - ${#value} ))}"
    if [[ -n "$strip_chars" ]]; then
        cur_stripped="${cur_stripped##*[$strip_chars]}"
    fi

    for i in "${!COMPREPLY[@]}"; do
      COMPREPLY[i]="$cur_stripped${COMPREPLY[i]}"
    done
  else
    [[ -n "$strip_chars" ]] && cur_stripped="${cur_stripped##*[$strip_chars]}"
    cur_stripped="${cur_stripped%"$pair"}"

    for key in "${remaining_keys[@]}"; do
      if [[ "$key" == "$pair"* ]]; then
        COMPREPLY+=("$cur_stripped$key")
      fi
    done
  fi
fi
''', ['my_dequote'])

_PREFIX_COMPREPLY = helpers.ShellFunction('prefix_compreply', r'''
[[ "$cur" == *[$COMP_WORDBREAKS]* ]] && return

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
#ifdef bash_completions_v_2_12
  _comp_compgen_filedir
#else
  _filedir
#endif
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
        self.add_function(_PARSE_LINE)
        self.add_function(_SUBSTRACT_PREFIX_SUFFIX)
        self.add_function(_COMMANDLINE_STRING)
        self.add_function(_INVOKE_COMPLETE)
        self.add_function(_EXEC)
        self.add_function(_EXEC_FAST)
        self.add_function(_VALUE_LIST)
        self.add_function(_KEY_VALUE_LIST)
        self.add_function(_PREFIX_COMPREPLY)
        self.add_function(_HISTORY)
        self.add_function(_MIME_FILE)
        self.add_function(_NET_INTERFACES_LIST)
        self.add_function(_TIMEZONE_LIST)
        self.add_function(_ALSA_LIST_CARDS)
        self.add_function(_ALSA_LIST_DEVICES)
