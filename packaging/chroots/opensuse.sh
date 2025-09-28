#!/bin/bash

set -e

cd "$(dirname "$0")"

if [ "$EUID" -ne 0 ]; then
  echo "Please run as root"
  exit 1
fi

if [[ "$#" != 1 ]]; then
  echo "Usage: $0 <CHROOT_DIR>"
  exit 1
fi

CHROOT_DIR="$1"

if [[ "${CHROOT_DIR:0:1}" != '/' ]]; then
  echo "$0: <CHROOT_DIR> has to be an absolute path!"
  exit 1
fi

# Install zypper
pacman -S --needed zypper

# Make chroot dir
mkdir -p "$CHROOT_DIR"

zypper --gpg-auto-import-keys --root "$CHROOT_DIR" ar \
  "https://download.opensuse.org/tumbleweed/repo/oss/" \
  tumbleweed-oss

zypper --gpg-auto-import-keys --root "$CHROOT_DIR" refresh

zypper --gpg-auto-import-keys --root "$CHROOT_DIR" -n install \
  openSUSE-release zypper bash coreutils glibc vim less iputils

cp /etc/resolv.conf "$CHROOT_DIR/etc"
