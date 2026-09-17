#!/usr/bin/env python3

import os
import sys
import glob
import shutil
import argparse
import tempfile
import subprocess

parser = argparse.ArgumentParser()

parser.add_argument('--dir', default='/tmp',
    help='Directory for podman')

parser.add_argument('--package-dir', default='/tmp/packages',
    help='Directory where packages will be stored')

parser.add_argument('--ignore-errors', action='store_true',
    help='Ignore errors')

parser.add_argument('--recreate', action='store_true',
    help='Recreate containers before building')

parser.add_argument('--project', action='append',
    help='Only build project. Can be specified multiple times')

parser.add_argument('--os', action='append',
    help='Only build for OS. Can be specified multiple times')

parser.add_argument('--dry', action='store_true',
    help='Only print out what would be built')

OPTS = parser.parse_args()

SCRIPT_PATH = os.path.abspath(sys.argv[0])
SCRIPT_DIR = os.path.dirname(SCRIPT_PATH)
os.chdir(SCRIPT_DIR)

def run(*args):
    result = subprocess.run(
        args,
        stderr=sys.stderr,
        stdout=sys.stdout,
        check=False)

    if result.returncode != 0:
        raise Exception('Command `%s` failed' % ' '.join(args))

class PodMan:
    def __init__(self, root, run_root, name, image):
        self.root = root
        self.run_root = run_root
        self.name = name
        self.image = image

    def _run(self, *args):
        run('podman', '--root', self.root, '--runroot', self.run_root, *args)

    def create(self):
        print('Creating container %s with image %s ...' % (self.name, self.image))
        self._run('create', '--name', self.name, self.image, 'sleep', 'infinity')

    def start(self):
        print('Starting container %s ...' % self.name)
        self._run('start', self.name)

    def stop(self):
        print('Stopping container %s ...' % self.name)
        self._run('stop', '-t', '1', self.name)

    def exec(self, *args):
        print('Container %s: executing ...' % self.name, args)
        self._run('exec', self.name, *args)

    def cp_to_container(self, source, dest):
        print('Copying %s to %s:%s ...' % (source, self.name, dest))
        self._run('cp', source, '%s:%s' % (self.name, dest))

    def cp_from_container(self, source, dest):
        print('Copying %s:%s to %s ...' % (self.name, source, dest))
        self._run('cp', '%s:%s' % (self.name, source), dest)

    def remove(self):
        print('Removing container %s ...' % self.name)
        self._run('rm', self.name)

class ProjectBuild:
    def __init__(self, os, build_script, image, project, package_glob):
        self.os = os
        self.build_script = build_script
        self.image = image
        self.project = project
        self.package_glob = package_glob
        self.directory = OPTS.dir

        podman_root = '%s/podman-root' % self.directory
        podman_runroot = '%s/podman-runroot' % self.directory
        name = '%s-%s' % (self.os, self.project)
        self.podman = PodMan(podman_root, podman_runroot, name, image)

    def build(self):
        if OPTS.recreate:
            try:
                self.podman.remove()
            except:
                pass

        try:
            self.podman.create()
        except:
            pass

        self.package()
        self.copy_package()

    def package(self):
        script = './packaging/%s/%s' % (self.project, self.build_script)
        self.podman.cp_to_container(script, '/root')

        try:
            self.podman.start()
            self.podman.exec('/root/%s' % self.build_script)
        finally:
            self.podman.stop()

    def copy_package(self):
        with tempfile.TemporaryDirectory() as tempdir:
            self.podman.cp_from_container('/root/%s' % self.project, tempdir)

            pattern = '%s/%s/%s' % (tempdir, self.project, self.package_glob)
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
DEBIAN_LATEST     = DEBIAN_TRIXIE

UBUNTU_RESOLUTE   = "ubuntu:resolute"
UBUNTU_NOBLE      = "ubuntu:noble"
UBUNTU_JAMMY      = "ubuntu:jammy"
UBUNTU_LATEST     = UBUNTU_RESOLUTE

LINUX_MINT_22     = "docker.io/linuxmintd/mint22-amd64"
LINUX_MINT_21     = "docker.io/linuxmintd/mint21-amd64"
LINUX_MINT_LATEST = LINUX_MINT_22

FEDORA_44         = "registry.fedoraproject.org/fedora:44"
FEDORA_43         = "registry.fedoraproject.org/fedora:43"
FEDORA_LATEST     = FEDORA_44

OPENSUSE_IMAGE    = "registry.opensuse.org/opensuse/tumbleweed:latest"
ARCHLINUX_IMAGE   = "docker.io/library/archlinux:latest"

builds = [
    ProjectBuild("debian-trixie",   "debian.sh",     DEBIAN_TRIXIE,   "crazy-complete", "*.deb"),
    ProjectBuild("debian-bookworm", "debian.sh",     DEBIAN_BOOKWORM, "crazy-complete", "*.deb"),
    ProjectBuild("ubuntu-resolute", "debian.sh",     UBUNTU_RESOLUTE, "crazy-complete", "*.deb"),
    ProjectBuild("ubuntu-noble",    "debian.sh",     UBUNTU_NOBLE,    "crazy-complete", "*.deb"),
    ProjectBuild("ubuntu-jammy",    "debian.sh",     UBUNTU_JAMMY,    "crazy-complete", "*.deb"),
    ProjectBuild("linux-mint-22",   "debian.sh",     LINUX_MINT_22,   "crazy-complete", "*.deb"),
    ProjectBuild("linux-mint-21",   "debian.sh",     LINUX_MINT_21,   "crazy-complete", "*.deb"),
    ProjectBuild("fedora-44",       "fedora.sh",     FEDORA_44,       "crazy-complete", "*.rpm"),
    ProjectBuild("fedora-43",       "fedora.sh",     FEDORA_43,       "crazy-complete", "*.rpm"),
    ProjectBuild("opensuse",        "opensuse.sh",   OPENSUSE_IMAGE,  "crazy-complete", "*.rpm"),
    ProjectBuild("arch-linux",      "arch-linux.sh", ARCHLINUX_IMAGE, "crazy-complete", "*.pkg.tar.zst"),
]

selected_builds = builds

if OPTS.project:
    selected_builds = filter(lambda rule: rule.project in OPTS.project, selected_builds)

if OPTS.os:
    selected_builds = filter(lambda rule: rule.os in OPTS.os, selected_builds)

for build in selected_builds:
    print('Building %s for %s ...' % (build.project, build.os))
    if OPTS.dry:
        continue

    try:
        build.build()
    except Exception as e:
        if OPTS.ignore_errors:
            continue
        else:
            raise e
