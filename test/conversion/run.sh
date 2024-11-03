#!/bin/bash

set -x -e

cd "$(dirname "$0")"

CRAZY_COMPLETE=../../crazy-complete
TEST_FILE=../tests/crazy-complete-test

$CRAZY_COMPLETE --debug --input-type=python json "$TEST_FILE" -o out.json
$CRAZY_COMPLETE --debug --input-type=python yaml "$TEST_FILE" -o out.yaml

$CRAZY_COMPLETE --debug bash out.yaml -o /tmp/out.bash
$CRAZY_COMPLETE --debug bash out.json -o /tmp/out.bash

grep --help > help.txt
$CRAZY_COMPLETE --debug --input-type=help yaml help.txt -o out.yaml
