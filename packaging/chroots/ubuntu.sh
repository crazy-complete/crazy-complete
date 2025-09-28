#!/bin/bash

ARCH=amd64
RELEASE=jammy
CACHE_DIR=/tmp/ubuntu.cache

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

# Install debootstrap
pacman -S --needed debootstrap

# Make chroot dir
mkdir -p "$CHROOT_DIR"

# Make cache dir
mkdir -p "$CACHE_DIR"

# Install debian into chroot
debootstrap \
  --arch=$ARCH \
  --cache-dir="$CACHE_DIR" \
  $RELEASE "$CHROOT_DIR" http://archive.ubuntu.com/ubuntu
