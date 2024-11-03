#!/bin/bash

set -e

cd "$(dirname "$0")"

TEST_ARGS=''

usage() {
  cat << EOF
Usage: $0 [-f|--fast]

  -f|--fast
    Enable fast testing mode for ./tests/run.py
    For tests where the input matches the expected output, these tests will always pass.
EOF
}

if (( $# == 1 )); then
  if [[ "$1" == "-f" ]] || [[ "$1" == "--fast" ]]; then
    TEST_ARGS="$1"
  else
    usage
    exit 1
  fi
elif (( $# )); then
  usage
  exit 1
fi

set -x

./conversion/run.sh
./error_messages/run.py
./tests/run.py $TEST_ARGS
