'''
This module provides functions to retrieve file paths for
autocompletion scripts for Bash, Fish, and Zsh.
'''

import subprocess

from . import utils

def _pkg_config(args):
    command = ['pkg-config'] + args
    try:
        result = subprocess.run(
            command,
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
            text=True,
            check=False)
    except FileNotFoundError:
        raise Exception('program `pkg-config` not found')

    if result.returncode == 0:
        return result.stdout.strip()

    raise Exception('%s failed: %s' % (' '.join(command), result.stderr.strip()))

def get_bash_completion_file(program_name):
    directory = '/usr/share/bash-completion/completions'
    try:
        directory = _pkg_config(['--variable=completionsdir', 'bash-completion'])
    except Exception as e:
        utils.warn(e)

    return f'{directory}/{program_name}'

def get_fish_completion_file(program_name):
    directory = '/usr/share/fish/vendor_completions.d'
    try:
        directory = _pkg_config(['--variable=completionsdir', 'fish'])
    except Exception as e:
        utils.warn(e)

    return f'{directory}/{program_name}.fish'

def get_zsh_completion_file(program_name):
    directory = '/usr/share/zsh/site-functions'
    return f'{directory}/_{program_name}'
