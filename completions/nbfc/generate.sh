#!/bin/sh

if [ -x ../../crazy-complete ]; then
  crazy_complete='../../crazy-complete'
elif type crazy-complete >/dev/null; then
  crazy_complete=crazy-complete
else
  echo "No crazy-complete found"
  exit 1
fi

if [ $# -eq 0 ]; then
  echo "Usage: $0 {ec_probe,nbfc,nbfc_service} {bash,fish,zsh}" >&2
  exit 1
elif [ $# -eq 1 ]; then
  echo "Missing argument: [bash, fish, zsh]"
  exit 1
elif [ $# -gt 2 ]; then
  echo "Too many arguments provided" >&2
  exit 1
fi

[ "$1" = "ec_probe" ] || [ "$1" = "nbfc" ] || [ "$1" = "nbfc_service" ] || {
  echo "\$1: invalid argument: $1" >&2
  exit 1
}

[ "$2" = "bash" ] || [ "$2" = "fish" ] || [ "$2" = "zsh" ] || {
  echo "\$2: invalid argument: $2" >&2
  exit 1
}

$crazy_complete "$2" "$1.yaml"
