#!/bin/sh

if [ -x ../../crazy-complete ]; then
  crazy_complete='../../crazy-complete'
  echo "Using development version of crazy-complete" >&2
elif type crazy-complete >/dev/null; then
  crazy_complete=crazy-complete
else
  echo "No crazy-complete found"
  exit 1
fi

if [ $# -eq 0 ]; then
  echo "Usage: $0 {bash,fish,zsh} <options>" >&2
  exit 1
fi

[ "$1" = "bash" ] || [ "$1" = "fish" ] || [ "$1" = "zsh" ] || {
  echo "$0: \$1: invalid argument: $1" >&2
  exit 1
}

opts=''
if [ "$1" = 'fish' ]; then
  # --repeatable-options=False (which is the default) makes the
  # commpletion slower.
  opts='--repeatable-options=True'
fi

$crazy_complete $opts "$@" fpm.yaml
