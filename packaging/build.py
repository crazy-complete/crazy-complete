#!/usr/bin/env python3

import os
import sys
import glob
import shutil
import subprocess
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--dir', default='/tmp')
parser.add_argument('--package-dir', default='/tmp/crazy-complete-packages')
parser.add_argument('--ignore-errors', action='store_true')
parser.add_argument('--os', action='append',
    help='Only build for OS. Can be specified multiple times')
parser.add_argument('--dry', action='store_true',
    help='Only print out what would be built')

OPTS = parser.parse_args()

SCRIPT_PATH = os.path.abspath(sys.argv[0])
SCRIPT_DIR = os.path.dirname(SCRIPT_PATH)
os.chdir(SCRIPT_DIR)

if os.geteuid() != 0:
    raise Exception("Please run this script as root")

def run(*args):
    result = subprocess.run(
        args,
        stderr=sys.stderr,
        stdout=sys.stdout,
        check=False)

    if result.returncode != 0:
        raise Exception('Command `%s` failed' % ' '.join(args))

class ProjectBuild:
    def __init__(self, os, build_script, image, package_glob):
        self.os = os
        self.build_script = build_script
        self.image = image
        self.package_glob = package_glob
        self.directory = OPTS.dir
        self.chroot_dir = '%s/%s-crazy-complete-chroot' % (self.directory, self.os)
        self.podman_root = '%s/podman-root' % self.directory
        self.podman_runroot = '%s/podman-runroot' % self.directory

    def create_chroot(self):
        if os.path.exists(self.chroot_dir):
            print('Skip installing chroot %s ...' % self.chroot_dir)
            return

        print('Installing chroot %s ...' % self.chroot_dir)
        run('./create_chroot.sh', self.podman_root, self.podman_runroot, self.image, self.chroot_dir)

    def mount_chroot(self):
        shutil.copy('/etc/resolv.conf', '%s/etc/resolv.conf' % self.chroot_dir)

        run('mount', '-t', 'proc', 'proc', '%s/proc' % self.chroot_dir)

        run('mount', '--rbind', '/sys',    '%s/sys'  % self.chroot_dir)
        run('mount', '--make-rslave',      '%s/sys'  % self.chroot_dir)

        run('mount', '--rbind', '/dev',    '%s/dev'  % self.chroot_dir)
        run('mount', '--make-rslave',      '%s/dev'  % self.chroot_dir)

        run('mount', '--rbind', '/run',    '%s/run'  % self.chroot_dir)
        run('mount', '--make-rslave',      '%s/run'  % self.chroot_dir)

    def umount_chroot(self):
        try: run('umount', '-R', '%s/dev'  % self.chroot_dir)
        except: pass
        try: run('umount', '-R', '%s/sys'  % self.chroot_dir)
        except: pass
        try: run('umount', '-R', '%s/proc' % self.chroot_dir)
        except: pass
        try: run('umount', '-R', '%s/run'  % self.chroot_dir)
        except: pass

    def package(self):
        print('Building for %s ...' % self.os)
        script = './packaging/%s' % self.build_script
        dest = '%s/root' % self.chroot_dir
        print("Copying %s to %s" % (script, dest))
        shutil.copy(script, dest)
        run('chroot', self.chroot_dir, './root/%s' % self.build_script)

    def move_package(self):
        pattern = '%s/root/%s' % (self.chroot_dir, self.package_glob)
        files = glob.glob(pattern)
        if not files:
            raise Exception('No package found')
        if len(files) > 1:
            raise Exception('Too much packages found: %s' % files)
        package = files[0]
        package_basename = os.path.basename(package)
        print("Found package: ", package)
        dest_package = '%s/%s-%s' % (OPTS.package_dir, self.os, package_basename)
        print("Copying %s to %s" % (package, dest_package))
        shutil.copy(package, dest_package)

os.makedirs(OPTS.package_dir, exist_ok=True)

DEBIAN_TRIXIE     = "docker.io/library/debian:trixie"
DEBIAN_BOOKWORM   = "docker.io/library/debian:bookworm"

UBUNTU_NOBLE      = "ubuntu:noble"
UBUNTU_JAMMY      = "ubuntu:jammy"

LINUX_MINT_22     = "docker.io/linuxmintd/mint22-amd64"
LINUX_MINT_21     = "docker.io/linuxmintd/mint21-amd64"

FEDORA_44         = "registry.fedoraproject.org/fedora:44"
FEDORA_43         = "registry.fedoraproject.org/fedora:43"

OPENSUSE_IMAGE    = "registry.opensuse.org/opensuse/tumbleweed:latest"
ARCHLINUX_IMAGE   = "docker.io/library/archlinux:latest"

builds = [
    ProjectBuild("debian-trixie",   "debian.sh",     DEBIAN_TRIXIE,    "*.deb"),
    ProjectBuild("debian-bookworm", "debian.sh",     DEBIAN_BOOKWORM,  "*.deb"),
    ProjectBuild("ubuntu-noble",    "debian.sh",     UBUNTU_NOBLE,     "*.deb"),
    ProjectBuild("ubuntu-jammy",    "debian.sh",     UBUNTU_JAMMY,     "*.deb"),
    ProjectBuild("linux-mint-22",   "debian.sh",     LINUX_MINT_22,    "*.deb"),
    ProjectBuild("linux-mint-21",   "debian.sh",     LINUX_MINT_21,    "*.deb"),
    ProjectBuild("fedora-44",       "fedora.sh",     FEDORA_44,        "*.rpm"),
    ProjectBuild("fedora-43",       "fedora.sh",     FEDORA_43,        "*.rpm"),
    ProjectBuild("opensuse",        "opensuse.sh",   OPENSUSE_IMAGE,   "*.rpm"),
    ProjectBuild("arch-linux",      "arch-linux.sh", ARCHLINUX_IMAGE,  "*.pkg.tar.zst"),
]

selected_builds = builds

if OPTS.os:
    selected_builds = filter(lambda rule: rule.os in OPTS.os, selected_builds)

for build in selected_builds:
    if OPTS.dry:
        print('Building for:', build.os)
        continue

    try:
        build.create_chroot()
    except Exception as e:
        if OPTS.ignore_errors:
            continue
        else:
            raise e

    try:
        build.mount_chroot()
        build.package()
        build.move_package()
    except Exception as e:
        if OPTS.ignore_errors:
            continue
        else:
            raise e
    finally:
        build.umount_chroot()
