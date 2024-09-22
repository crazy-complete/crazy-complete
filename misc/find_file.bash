#!/bin/bash

_find_files() {
  local APPEND=false
  local DIRECTORY='.'
  local ONLY_DIRECTORIES=''
  local REGEX=''
  local REGEX_EXTENDED=''

  while getopts ":D:R:adE" opt; do
    case "$opt" in
      D) DIRECTORY="$OPTARG";;
      R) REGEX="$OPTARG";;
      a) APPEND=true;;
      d) ONLY_DIRECTORIES='-d';;
      E) REGEX_EXTENDED='-E';;
     \?) echo "Invalid option: $OPTARG" >&2;
         return 1;;
      :) echo "Option -$OPTARG requires an argument" >&2;
         return 1;;
     esac
  done

  local -a COMPREPLY_BACK=("${COMPREPLY[@]}")

  if [[ "$DIRECTORY" != '.' ]]; then
    if pushd "$DIRECTORY"; then
      _filedir $ONLY_DIRECTORIES
      popd
    else
      return 1
    fi
  else
    _filedir $ONLY_DIRECTORIES
  fi

  if [[ -n "$REGEX" ]]; then
    local -a COMPREPLY_NEW
    local FILE
    for FILE in ; do
      grep -q $REGEX_EXTENDED -- "$REGEX" <<< "$FILE" && COMPREPLY_NEW+=("$FILE")
    done
    COMPREPLY=("${COMPREPLY_NEW[@]}")
  fi

  if $APPEND; then
    COMPREPLY=("${COMPREPLY_BACK[@]}" "${COMPREPLY[@]}")
  fi
}

_find_files
