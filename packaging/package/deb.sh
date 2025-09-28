#!/bin/bash

set -e -x

cd "$(dirname "$0")"

type ruby || {
  apt install -y ruby
}

type git || {
  apt install -y git
}

type python3 || {
  apt install -y python3
}

type python || {
  apt install -y python-is-python3
}

type ar || {
  apt install -y binutils
}

apt install -y python3-pkg-resources python3-setuptools

export PATH="$HOME/.local/share/gem/ruby/3.1.0/bin/:$PATH"

type fpm || {
  gem install --user-install fpm
}

rm -rf crazy-complete

git clone https://github.com/crazy-complete/crazy-complete

cd crazy-complete

fpm -s python -t deb -d python3-yaml --python-scripts-executable=/usr/bin/python3 setup.py

mv *.deb ..
