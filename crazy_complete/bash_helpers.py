'''This module contains helper functions for Bash.'''

from . import helpers

_VALUES = helpers.ShellFunction('values', r'''
local word append=0

[[ "$1" == "-a" ]] && { shift; append=1; }
[[ "$1" == "--" ]] && { shift; }

(( append )) || COMPREPLY=()

for word; do
  if [[ "$word" == "$cur"* ]]; then
    COMPREPLY+=("$(printf '%q' "$word")")
  fi
done
''')

_DEQUOTE = helpers.ShellFunction('dequote', r'''
local in="$1" len=${#1} i=0 result='' ___break_pos=-1 ___in_quotes=0

for ((; i < len; ++i)); do
  case "${in:i:1}" in
    "'")
      ___in_quotes=1
      for ((++i; i < len; ++i)); do
        [[ "${in:i:1}" == "'" ]] && { ___in_quotes=0; break; }
        result+="${in:i:1}"
      done;;
    '"')
      ___in_quotes=1
      for ((++i; i < len; ++i)); do
        [[ "${in:i:1}" == '"' ]] && { ___in_quotes=0; break; }

        if [[ "${in:i:1}" == '\' ]]; then
          result+="${in:$((++i)):1}"
        else
          result+="${in:i:1}"
        fi
      done;;
    '\')
      result+="${in:$((++i)):1}";;
    [$COMP_WORDBREAKS])
      result+="${in:i:1}"
      ___break_pos=${#result};;
    *)
      result+="${in:i:1}";;
  esac
done

local -n ___RESULT=$2
local -n ___BREAK_POS=$3
local -n ___IN_QUOTES=$4
___RESULT="$result"
___BREAK_POS=$___break_pos
___IN_QUOTES=$___in_quotes
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

_GET_PREFIX_SUFFIX_LEN = helpers.ShellFunction('get_prefix_suffix_len', r'''
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
      echo 0
    else
      echo $((len1-k))
    fi

    return
  fi

  ((k--))
done

echo ${#s1}
''')

_COMMANDLINE_STRING = helpers.ShellFunction('commandline_string', r'''
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

_EXEC = helpers.ShellFunction('exec', r'''
local item desc special="$COMP_WORDBREAKS\"'><=;|&({:\\\$\`"

while IFS=$'\t' read -r item desc; do
  if [[ "$item" == "$cur"* ]]; then
    [[ "$item" == *[$special]* ]] && item="$(printf '%q' "$item")"
    COMPREPLY+=("$item")
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

_ARRAY_CONTAINS = helpers.ShellFunction('array_contains', r'''
local w='' search="$1"; shift;
for w; do [[ "$search" == "$w" ]] && return 0; done
return 1
''')

_VALUE_LIST = helpers.ShellFunction('value_list', r'''
local duplicates=0
[[ "$1" == '-d' ]] && { duplicates=1; shift; }
local separator="$1"; shift

compopt -o nospace

local cur_unquoted break_pos in_quotes
dequote "$cur" cur_unquoted break_pos in_quotes

if [[ -z "$cur_unquoted" ]]; then
  COMPREPLY=("$@")
  return
fi

local value having_value having_values=() remaining_values=()

IFS="$separator" read -r -a having_values <<< "$cur_unquoted"

if (( duplicates )); then
  remaining_values=("$@")
else
  for value; do
    if ! array_contains "$value" "${having_values[@]}"; then
      remaining_values+=("$value")
    fi
  done
fi

COMPREPLY=()

local cur_stripped="$cur_unquoted"
if (( break_pos > -1 )); then
  cur_stripped="${cur_stripped:break_pos}"
fi

if [[ "${cur_unquoted: -1}" == "$separator" ]]; then
  for value in "${remaining_values[@]}"; do
    COMPREPLY+=("$cur_stripped$value")
  done
elif (( ${#remaining_values[@]} )); then
  if array_contains "${having_values[-1]}" "$@"; then
    COMPREPLY+=("$cur_stripped$separator")
  elif (( ${#having_values[@]} )); then
    local cur_last_value=${having_values[-1]}
    cur_stripped="${cur_stripped%"$cur_last_value"}"

    for value in "${remaining_values[@]}"; do
      if [[ "$value" == "$cur_last_value"* ]]; then
        COMPREPLY+=("$cur_stripped$value")
      fi
    done
  fi
fi
''', ['dequote', 'array_contains'])

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
local cur="$cur" break_pos in_quotes
dequote "$cur" cur break_pos in_quotes

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
''', ['dequote'])

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

_GET_LAST_BREAK_POSITION = helpers.ShellFunction('get_last_break_position', r'''
local in="$1" i=0 len=${#1} pos=-1

for ((i=0; i < len; ++i)); do
  case "${in:i:1}" in
    '"')
      for ((++i; i < len; ++i)); do
        if [[ "${in:i:1}" == '\' ]]; then
          ((++i))
        elif [[ "${in:i:1}" == '"' ]]; then
          break;
        fi
      done;;
    "'")
      for ((++i; i < len; ++i)); do
        [[ "${in:i:1}" == "'" ]] && break;
      done;;
    '\')
      ((++i));;
    [$COMP_WORDBREAKS])
      pos=$i;;
  esac
done

echo $pos
''')

_PREFIX = helpers.ShellFunction('prefix', r'''
local prefix="$1" func="$2"
local stripped="$(strip_prefix_keep_quoting "$prefix" "$cur")"

if [[ "$stripped" == "$cur" ]]; then
  COMPREPLY=($(compgen -W "$1" -- "$cur"))
  compopt -o nospace
  return
fi

local break_position=$(get_last_break_position "$cur")

local cur_old="$cur" cur="$stripped"
$func

if (( break_position < 0 )); then
  for i in "${!COMPREPLY[@]}"; do
    COMPREPLY[i]="$prefix${COMPREPLY[i]}"
  done
fi
''', ['get_last_break_position', 'strip_prefix_keep_quoting'])

_STRIP_PREFIX_KEEP_QUOTING = helpers.ShellFunction('strip_prefix_keep_quoting', r'''
local p="$1" pi=0 plen=${#1}
local s="$2" si=0 slen=${#2} state=w

for (( pi=0; pi < plen; ++pi )); do
  pc=${p:pi:1}
  sc=''

  while (( si < slen )); do
    case "$state" in
      w)
        case "${s:si:1}" in
          '"') state=dq; ((++si));;
          "'") state=sq; ((++si));;
          '\')           ((++si)); sc="${s:si:1}"; ((++si));   break;;
          *)             sc="${s:si:1}"; ((++si));             break;;
        esac;;
      sq)
        case "${s:si:1}" in
          "'") state=w;  ((++si));;
          *)             sc="${s:si:1}"; ((++si));             break;;
        esac;;
      dq)
        case "${s:si:1}" in
          '"') state=w;  ((++si));;
          '\')           ((++si)); sc="${s:si:1}"; ((++si));   break;;
          *)             sc="${s:si:1}"; ((++si));             break;;
        esac;;
    esac
  done

  [[ "$pc" != "$sc" ]] && { echo "$s"; return; }
done

case "$state" in
  w)  printf '%s\n' "${s:si}";;
  sq) printf '%s\n' "'${s:si}";;
  dq) printf '%s\n' "\"${s:si}";;
esac
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

_FILE_FILTER = helpers.ShellFunction('file_filter', '''
local pattern REPLY COMPREPLY_OLD=("${COMPREPLY[@]}")

COMPREPLY=()

for REPLY in "${COMPREPLY_OLD[@]}"; do
  for pattern; do
    [[ "${REPLY##*/}" == $pattern ]] && continue 2
  done

  COMPREPLY+=("$REPLY")
done
''')

# =============================================================================
# Bonus
# =============================================================================

_LOCALES = helpers.ShellFunction('''locales''', r'''
COMPREPLY=($(compgen -W "$(command locale -a)" -- "$cur"))
''')

_CHARSETS = helpers.ShellFunction('''charsets''', r'''
COMPREPLY=($(compgen -W "$(command locale -m)" -- "$cur"))
''')

_TIMEZONE_LIST = helpers.ShellFunction('timezone_list', r'''
if ! command timedatectl list-timezones 2>/dev/null; then
  command find /usr/share/zoneinfo -type f |\
  command sed 's|/usr/share/zoneinfo/||g'  |\
  command grep -E -v '^(posix|right)'
fi''')

_ALSA_LIST_CARDS = helpers.ShellFunction('alsa_list_cards', r'''
local card id cards=()
while builtin read card; do
  card="${card#card }"
  id="${card%%: *}"
  cards+=("$id")
done < <(command aplay -l | command grep -Eo '^card [0-9]+: [^,]+')

COMPREPLY=($(compgen -W "${cards[*]}" -- "$cur"))
''')

_ALSA_LIST_DEVICES = helpers.ShellFunction('alsa_list_devices', r'''
local card id devices=()
while builtin read card; do
  card="${card#card }"
  id="${card%%: *}"
  devices+=("hw:$id")
done < <(command aplay -l | command grep -Eo '^card [0-9]+: [^,]+')

COMPREPLY=($(compgen -W "${devices[*]}" -- "$cur"))
''')


class BashHelpers(helpers.GeneralHelpers):
    '''Class holding helper functions for Bash.'''

    def __init__(self, config, function_prefix):
        super().__init__(config, function_prefix, helpers.ShellFunction)
        self.add_function(_VALUES)
        self.add_function(_DEQUOTE)
        self.add_function(_PREFIX)
        self.add_function(_STRIP_PREFIX_KEEP_QUOTING)
        self.add_function(_ARRAY_CONTAINS)
        self.add_function(_GET_LAST_BREAK_POSITION)
        self.add_function(_PARSE_LINE)
        self.add_function(_GET_PREFIX_SUFFIX_LEN)
        self.add_function(_COMMANDLINE_STRING)
        self.add_function(_EXEC)
        self.add_function(_EXEC_FAST)
        self.add_function(_VALUE_LIST)
        self.add_function(_KEY_VALUE_LIST)
        self.add_function(_FILE_FILTER)
        self.add_function(_PREFIX_COMPREPLY)
        self.add_function(_HISTORY)
        self.add_function(_MIME_FILE)
        self.add_function(_LOCALES)
        self.add_function(_CHARSETS)
        self.add_function(_TIMEZONE_LIST)
        self.add_function(_ALSA_LIST_CARDS)
        self.add_function(_ALSA_LIST_DEVICES)
