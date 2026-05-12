#!/usr/bin/env python3

import sys
import requests

OWNER = "crazy-complete"
REPO  = "crazy-complete"

def replace_package_data(content):
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/releases/latest"
    response = requests.get(url)
    response.raise_for_status()
    releases = response.json()

    mapping = {
        'debian-trixie':    'DEBIAN_TRIXIE',
        'debian-bookworm':  'DEBIAN_BOOKWORM',
        'ubuntu-noble':     'UBUNTU_NOBLE',
        'ubuntu-jammy':     'UBUNTU_JAMMY',
        'linux-mint-22':    'LINUX_MINT_22',
        'linux-mint-21':    'LINUX_MINT_21',
        'fedora-44':        'FEDORA_44',
        'fedora-43':        'FEDORA_43',
        'opensuse':         'OPENSUSE',
        'arch-linux':       'ARCHLINUX',
    }

    TAG = releases['tag_name']
    content = content.replace('%TAG%', TAG)

    for release in releases['assets']:
        name = release['name']
        url  = release['browser_download_url']

        for file_prefix, replacement_prefix in mapping.items():
            if name.startswith(file_prefix):
                content = content.replace(f'%{replacement_prefix}_PACKAGE%', name)
                content = content.replace(f'%{replacement_prefix}_URL%', url)

    return content

with open(sys.argv[1]) as fh:
    content = fh.read()

content = replace_package_data(content)

print(content)
