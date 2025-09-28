#!/bin/bash

RELEASE=42
CACHE_DIR=/tmp/fedora.cache
REPOS_DIR=/tmp/fedora.repos

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

# Install dnf
pacman -S --needed dnf5

# Make chroot dir
mkdir -p "$CHROOT_DIR"

# Make repos and cache dir
mkdir -p "$REPOS_DIR" "$CACHE_DIR"

# Copy repo file
cp ./fedora.repo "$REPOS_DIR"

# Install fedora into chroot
dnf5 \
  -y \
  --setopt=reposdir="$REPOS_DIR" \
  --setopt=cachedir="$CACHE_DIR" \
  --releasever=$RELEASE \
  --installroot="$CHROOT_DIR" \
  --nogpgcheck \
  install @core
