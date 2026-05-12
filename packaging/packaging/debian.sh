#!/bin/bash

set -e -x

cd "$(dirname "$0")"

apt update

apt install -y \
  python3 \
  python3-pip \
  python3-pkg-resources \
  python3-setuptools \
  python3-wheel \
  python3-packaging \
  python-is-python3 \
  ruby \
  git \
  binutils

export PATH="$HOME/.local/share/gem/ruby/3.3.0/bin/:$PATH" # debian trixie
export PATH="$HOME/.local/share/gem/ruby/3.2.0/bin/:$PATH" # ubuntu noble
export PATH="$HOME/.local/share/gem/ruby/3.1.0/bin/:$PATH" # debian bookworm
export PATH="$HOME/.local/share/gem/ruby/3.0.0/bin/:$PATH" # ubuntu jammy

type fpm || {
  gem install --user-install fpm
}

rm -rf crazy-complete

git clone https://github.com/crazy-complete/crazy-complete

cd crazy-complete

fpm -s python -t deb -d python3-yaml --python-scripts-executable=/usr/bin/python3 setup.py

mv *.deb ..
