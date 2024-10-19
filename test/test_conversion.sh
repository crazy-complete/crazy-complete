#!/bin/bash

set -x -e

cc=../crazy-complete

$cc --debug --input-type=python json ./crazy-complete-test -o /tmp/crazy-complete-test.json
$cc --debug --input-type=python yaml ./crazy-complete-test -o /tmp/crazy-complete-test.yaml
$cc --debug bash /tmp/crazy-complete-test.yaml -o /tmp/crazy-complete-test.bash
$cc --debug bash /tmp/crazy-complete-test.json -o /tmp/crazy-complete-test.bash

grep --help > /tmp/grep.help.txt
$cc --debug --input-type=help yaml /tmp/grep.help.txt -o /tmp/grep.yaml
