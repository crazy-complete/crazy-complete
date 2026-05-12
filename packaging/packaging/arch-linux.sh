#!/bin/bash

set -e

grep -i "arch linux" /etc/os-release || {
  echo "Not on Arch Linux";
  exit 1
}

SCRIPT_DIR="$(realpath "$(dirname "$0")")"

cd /tmp

pacman -Sy

pacman -S --noconfirm --needed \
  git \
  base-devel \
  python3 \
  python-build \
  python-installer \
  python-wheel \
  python-setuptools-scm

rm -rf crazy-complete

runuser -u nobody -- git clone https://github.com/crazy-complete/crazy-complete

cd crazy-complete

runuser -u nobody -- makepkg -d

PACKAGE=$(ls | grep pkg.tar.zst | grep -v debug)

mv "$PACKAGE" "$SCRIPT_DIR"
