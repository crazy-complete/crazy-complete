'''Functions for getting shell versions.'''

import re
import subprocess

from .utils import warn

def get_fish_major_version():
    '''Return the major version of the installed fish shell.'''
    try:
        result = subprocess.run(
            ['fish', '--version'],
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
            text=True,
            check=False)
    except FileNotFoundError:
        warn('Program `fish` not found. Falling back to Fish version 4')
        return 4

    if result.returncode != 0:
        warn('Command `fish --version` failed. Falling back to Fish version 4')
        return 4

    try:
        version = re.search(r'\d+\.\d+\.\d+', result.stdout)[0]
        if version.startswith('4'):
            return 4
        else:
            return 3
    except IndexError:
        warn('Could not fetch version from `fish --version`. Falling back to Fish version 4')
        return 4
