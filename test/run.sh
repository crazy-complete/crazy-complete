#!/bin/sh

set -e

cd "$(dirname "$0")"

set -x

./tests/run.py "$@"
./error_messages/run.py
./conversion/run.sh
