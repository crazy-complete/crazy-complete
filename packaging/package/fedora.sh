#!/bin/bash

set -e

cd "$(dirname "$0")"

type ruby || {
  dnf install -y ruby
}

type git || {
  dnf install -y git
}

type rpmbuild || {
  dnf install -y rpmbuild
}

dnf install -y python3-setuptools
dnf install -y python3-wheel
dnf install -y python3-pip
dnf install -y python3-packaging

export PATH="$HOME/.local/share/gem/ruby/bin/:$PATH"

type fpm || {
  gem install --user-install fpm
}

rm -rf crazy-complete

git clone https://github.com/crazy-complete/crazy-complete

cd crazy-complete

fpm -s python -t rpm -d python3-yaml setup.py

mv *.rpm ..
