#!/bin/sh

set -e

cd "$(dirname "$0")"

export PYTHONPATH=../..

for file in *.input.yaml; do
  base="${file%%.input.yaml}"
  outfile="${base}.output.yaml"
  expected="${base}.expected.yaml"

  if [[ "$1" == "--update" ]]; then
    python3 -m crazy_complete.main --input-type completely yaml "$file" -o "$expected"
  else
    python3 -m crazy_complete.main --input-type completely yaml "$file" -o "$outfile"
    diff -q "$outfile" "$expected"
  fi
done
