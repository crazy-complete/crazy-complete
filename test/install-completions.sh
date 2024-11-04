#!/bin/bash

set -e

cd "$(dirname "$0")"

CRAZY_COMPLETE_TEST=./tests/crazy-complete-test
CRAZY_COMPLETE_TEST_BIN_FILE=/bin/crazy-complete-test
SHELLS=(bash fish zsh)

usage() {
  cat << EOF
Usage: $0 install|uninstall

Install or uninstall system-wide completions for 'crazy-complete-test'
EOF
}

if [[ $# -ne 1 ]]; then
  usage
  exit 1
elif [[ "$1" == 'install' ]]; then
  cmd='install-completions'
elif [[ "$1" == 'uninstall' ]]; then
  cmd='uninstall-completions'
else
  usage
  exit 1
fi

if [[ $EUID -ne 0 ]]; then
  echo 'This script must be run as root' >&2
  exit 1
fi

if [[ -x ../crazy-complete ]]; then
  CRAZY_COMPLETE='../crazy-complete'
  printf '%s\n\n' 'Using development version of crazy-complete' >&2
elif which crazy-complete &>/dev/null; then
  CRAZY_COMPLETE='crazy-complete'
  printf '%s\n\n' 'Using installed version of crazy-complete' >&2
else
  echo 'No crazy-complete found' >&2
  exit 1
fi

install-completions() {
  cp -v "$CRAZY_COMPLETE_TEST" "$CRAZY_COMPLETE_TEST_BIN_FILE"

  for SHELL_ in ${SHELLS[@]}; do
    case "$SHELL_" in
      bash)
        $CRAZY_COMPLETE -i --input-type=python \
          bash "$CRAZY_COMPLETE_TEST" || {
          echo "$CRAZY_COMPLETE bash failed" >&2
          exit 1
        };;
      fish)
        $CRAZY_COMPLETE -i --input-type=python \
          fish "$CRAZY_COMPLETE_TEST" || {
          echo "$CRAZY_COMPLETE fish failed" >&2
          exit 1
        };;
      zsh)
        $CRAZY_COMPLETE -i --input-type=python \
          zsh  "$CRAZY_COMPLETE_TEST" || {
          echo "$CRAZY_COMPLETE zsh failed" >&2
          exit 1
        };;
    esac
  done
}

uninstall-completions() {
  rm -vf "$CRAZY_COMPLETE_TEST_BIN_FILE"

  for SHELL_ in ${SHELLS[@]}; do
    case "$SHELL_" in
      bash) $CRAZY_COMPLETE -u --input-type=python bash "$CRAZY_COMPLETE_TEST";;
      fish) $CRAZY_COMPLETE -u --input-type=python fish "$CRAZY_COMPLETE_TEST";;
      zsh)  $CRAZY_COMPLETE -u --input-type=python zsh  "$CRAZY_COMPLETE_TEST";;
    esac
  done
}

$cmd
