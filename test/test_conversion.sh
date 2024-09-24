#!/bin/bash

set -x -e

cc=../crazy-complete

$cc --debug --input-type=python json ./crazy-complete-test > /tmp/crazy-complete-test.json
$cc --debug --input-type=python yaml ./crazy-complete-test > /tmp/crazy-complete-test.yaml
$cc --debug bash /tmp/crazy-complete-test.yaml > /tmp/crazy-complete-test.bash
$cc --debug bash /tmp/crazy-complete-test.json > /tmp/crazy-complete-test.bash

