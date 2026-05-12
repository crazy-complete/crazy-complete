#!/bin/bash

# Downloads a Podman container image and exports its filesystem
# into a directory that can be used as a chroot environment.

set -e

if [ "$EUID" -ne 0 ]; then
  echo "Please run this script as root"
  exit 1
fi

if [ "$#" != 4 ]; then
  echo "Usage: $0 <PODMAN_ROOT> <PODMAN_RUNROOT> <IMAGE> <CHROOT_DIR>"
  exit 1
fi

PODMAN_ROOT="$1"
PODMAN_RUNROOT="$2"
IMAGE="$3"
CHROOT_DIR="$4"

mkdir -p "$CHROOT_DIR"
mkdir -p "$PODMAN_ROOT"
mkdir -p "$PODMAN_RUNROOT"

pm() {
  podman --root "$PODMAN_ROOT" --runroot "$PODMAN_RUNROOT" "$@"
}

pm pull "$IMAGE"

CID=$(pm create "$IMAGE")

echo "Container ID is: $CID" >&2

pm export "$CID" | tar -C "$CHROOT_DIR" -xpf -

pm rm "$CID"
