#!/bin/bash

cd "$(dirname "$0")"

if [[ -x ../crazy-complete ]]; then
  crazy_complete='../crazy-complete'
elif which crazy-complete; then
  crazy_complete=crazy-complete
else
  echo "No crazy-complete found"
  exit 1
fi

ARGPARSE_SHELLCOMPLETE_TEST=./crazy-complete-test
ARGPARSE_SHELLCOMPLETE_TEST_BIN_FILE=/bin/crazy-complete-test

if [[ $EUID -ne 0 ]]; then
  echo "This script must be run as root"
  exit 1
fi

declare -a SHELLS=()
SHELLS+=(bash)
SHELLS+=(fish)
SHELLS+=(zsh)

install-completions() {
  cp "$ARGPARSE_SHELLCOMPLETE_TEST" "$ARGPARSE_SHELLCOMPLETE_TEST_BIN_FILE"

  for SHELL_ in ${SHELLS[@]}; do
    case "$SHELL_" in
      bash)
        $crazy_complete -i --input-type=python --include-file include.bash \
          bash crazy-complete-test || {
          echo "$crazy_complete bash failed" >&2
          exit 1
        };;
      fish)
        $crazy_complete -i --input-type=python --include-file include.fish \
          fish crazy-complete-test || {
          echo "$crazy_complete fish failed" >&2
          exit 1
        };;
      zsh)
        $crazy_complete -i --input-type=python --include-file include.zsh \
          zsh  crazy-complete-test || {
          echo "$crazy_complete zsh failed" >&2
          exit 1
        };;
    esac
  done
}

uninstall-completions() {
  rm -f "$ARGPARSE_SHELLCOMPLETE_TEST_BIN_FILE"

  for SHELL_ in ${SHELLS[@]}; do
    case "$SHELL_" in
      bash) $crazy_complete -u --input-type=python bash crazy-complete-test;;
      fish) $crazy_complete -u --input-type=python fish crazy-complete-test;;
      zsh)  $crazy_complete -u --input-type=python zsh  crazy-complete-test;;
    esac
  done
}

do-test() {
  echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
  echo ""
  echo "This script will install crazy-complete-test completions"
  echo ""
  echo "Press Enter to continue, or CTRL+C to exit"
  read

  install-completions

  echo ""
  echo "Press Enter to remove the completion files"
  read

  uninstall-completions
}

if [[ $# -eq 0 ]]; then
  cat << EOF
Usage: $0 test|install|uninstall
EOF
  exit 1
elif [[ "$1" == "test" ]]; then
  do-test
elif [[ "$1" == "install" ]]; then
  install-completions
elif [[ "$1" == "uninstall" ]]; then
  uninstall-completions
else
  echo "Invalid command: $1" >&2
  exit 1
fi
