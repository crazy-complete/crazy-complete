#!/bin/bash

set -e

cd "$(dirname "$0")"

dnf install -y \
  python3-setuptools \
  python3-wheel \
  python3-pip \
  python3-packaging \
  ruby \
  git \
  rpmbuild

export PATH="$HOME/.local/share/gem/ruby/bin/:$PATH"

type fpm || {
  gem install --user-install fpm
}

rm -rf crazy-complete

git clone https://github.com/crazy-complete/crazy-complete

cd crazy-complete

fpm -s python -t rpm -d python3-yaml setup.py

mv *.rpm ..
