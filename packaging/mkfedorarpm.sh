#!/bin/bash

set -e

(( UID )) && {
  echo "This script needs to be run as root!" >&2
  exit 1
}

(( $# != 1 )) && {
  echo "Usage: $0 <CHROOT_DIR>" >&2
  exit 1
}

[[ -e "$1" ]] || {
  ./chroots/fedora.sh "$1"
}

cp ./package/fedora.sh "$1/root"

arch-chroot "$1" "/root/fedora.sh"

mv "$1"/root/*.rpm .
