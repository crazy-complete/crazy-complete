#!/bin/bash

FPM=fpm.ruby3.4

set -e

cd "$(dirname "$0")"

type ruby || {
  zypper -n --gpg-auto-import-keys install --no-recommends ruby
}

type git || {
  zypper -n --gpg-auto-import-keys install --no-recommends git
}

type rpmbuild || {
  zypper -n --gpg-auto-import-keys install --no-recommends rpm-build
}

type python3 || {
  zypper -n --gpg-auto-import-keys install --no-recommends python3
}

zypper -n --gpg-auto-import-keys install --no-recommends python3-setuptools python3-pyaml

export PATH="$HOME/.local/share/gem/ruby/3.4.0/bin/:$PATH"

type $FPM || {
  gem install --user-install fpm
}

rm -rf crazy-complete

git clone https://github.com/crazy-complete/crazy-complete

cd crazy-complete

$FPM -s python -t rpm -d python3-pyyaml --python-bin /usr/bin/python3 --python-scripts-executable /usr/bin/python3 setup.py

mv *.rpm ..
