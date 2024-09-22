#!/bin/bash

set -x -e

cc=../crazy-complete

$cc --input-type=python json ./crazy-complete-test > /tmp/crazy-complete-test.json
$cc --input-type=python yaml ./crazy-complete-test > /tmp/crazy-complete-test.yaml
$cc bash /tmp/crazy-complete-test.yaml > /tmp/crazy-complete-test.bash
$cc bash /tmp/crazy-complete-test.json > /tmp/crazy-complete-test.bash

