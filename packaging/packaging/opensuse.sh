#!/bin/bash

FPM=fpm.ruby4.0

set -e

cd "$(dirname "$0")"

zypper -n --gpg-auto-import-keys install --no-recommends \
  python3 python3-setuptools python3-pip \
  ruby \
  git \
  unzip \
  rpm-build

export PATH="$HOME/.local/share/gem/ruby/4.0.0/bin/:$PATH"

type $FPM || {
  gem install --user-install fpm
}

rm -rf crazy-complete

git clone https://github.com/crazy-complete/crazy-complete

cd crazy-complete

$FPM -s python -t rpm -d python313-PyYAML --python-bin /usr/bin/python3 --python-scripts-executable /usr/bin/python3 setup.py

mv *.rpm ..
