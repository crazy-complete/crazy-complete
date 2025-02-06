#!/usr/bin/env python3

import os
import re
import sys
import shlex
import argparse

# =============================================================================
# Constants
# =============================================================================

PROGRAM_PATHS = ['/bin', '/sbin', '/usr/bin', '/usr/sbin']

BASH_COMPLETION_PATHS = [
    '/etc/bash_completion.d',
    '/usr/share/bash-completion/completions',
]

FISH_COMPLETION_PATHS = [
    '/usr/share/fish/completions',
    '/usr/share/fish/vendor_completions.d',
]

ZSH_COMPLETION_PATHS = [
    '/usr/share/zsh/site-functions',
    '/usr/share/zsh/vendor-completions',
    '/usr/share/zsh/functions/Completion/Linux',
    '/usr/share/zsh/functions/Completion/Unix',
    '/usr/share/zsh/functions/Completion/Base',
    '/usr/share/zsh/functions/Completion/Zsh',
    '/usr/share/zsh/functions/Completion/X',
]

# =============================================================================
# Functions
# =============================================================================

def find_programs(path):
    try:
        return os.listdir(path)
    except FileNotFoundError:
        pass

def get_all_files_in_directories(directories):
    r = []

    for directory in directories:
        try:
            for file in os.scandir(directory):
                r.append(file.path)
        except FileNotFoundError:
            continue

    return r

def process_file(filename, callback):
    try:
        with open(filename, 'r', encoding='UTF-8') as fh:
            content = fh.read()
        return callback(filename, content)
    except FileNotFoundError:
        return None
    except UnicodeDecodeError:
        return None

def process_files(files, callback):
    r = []

    for file in files:
        with open(file, 'r', encoding='UTF-8') as fh:
            content = fh.read()
            result = callback(file, content)

            if result:
                r.append(result)

    return r

def parse_bash_complete_command(line):
    try:
        split = shlex.split(line)
    except Exception:
        return []

    i = 1
    have_F = False
    programs = []

    while i < len(split):
        arg = split[i]
        if arg == '-F':
            have_F = True
            i += 1
        elif arg == '-o':
            i += 1
        elif arg == '-X':
            i += 1
        elif arg.startswith('-'):
            pass
        else:
            programs.append(arg)
        i += 1

    if have_F:
        return programs
    else:
        return []

def parse_fish_complete_command(line):
    try:
        split = shlex.split(line)
    except Exception:
        return []

    i = 1
    while i < len(split):
        arg = split[i]
        if arg == '-c':
            return [split[i + 1]]
        elif arg.startswith('-c'):
            return [arg[2:]]
        i += 1

    return []

def parse_zsh_compdef(line):
    split = line.split()
    return split[1:]

def get_bash_completions():
    def callback(filename, content):
        r = []
        content = content.replace('\\\n', '')

        matches = re.findall('complete [^;&|\n]+', content)
        for m in matches:
            programs = parse_bash_complete_command(m)
            r.extend(programs)

        if not r:
            r = [os.path.basename(filename).lstrip('_')]

        return r

    files = get_all_files_in_directories(BASH_COMPLETION_PATHS)
    results = process_files(files, callback)

    r = set()
    for result in results:
        r.update(result)
    return sorted(r)

def get_fish_completions():
    def callback(filename, content):
        r = set()
        content = content.replace('\\\n', '')

        matches = re.findall('complete [^\n]+', content)
        for m in matches:
            programs = parse_fish_complete_command(m)
            r.update(programs)

        return r

    files = get_all_files_in_directories(FISH_COMPLETION_PATHS)
    results = process_files(files, callback)

    r = set()
    for result in results:
        r.update(result)
    return sorted(r)

def get_zsh_completions():
    def callback(filename, content):
        content = content.replace('\\\n', '')

        match = re.search('#compdef [^\n]+', content)
        if match:
            programs = parse_zsh_compdef(match[0])
            return programs

        return []

    files = get_all_files_in_directories(ZSH_COMPLETION_PATHS)
    results = process_files(files, callback)

    r = set()
    for result in results:
        r.update(result)
    return sorted(r)

# =============================================================================
# Classes
# =============================================================================

class Program:
    def __init__(self, program, has_bash, has_fish, has_zsh):
        self.program = program
        self.has_bash = has_bash
        self.has_fish = has_fish
        self.has_zsh = has_zsh

    def print(self):
        print('%-40s %-5s %-5s %-5s' % (
            self.program,
            self.has_bash,
            self.has_fish,
            self.has_zsh))

class Filter:
    def __init__(self, s):
        self.filters = {}

        for shell_filter in s.split(','):
            try:
                shell, filter_ = shell_filter.split('=')
            except ValueError:
                raise Exception('Invalid format. Format has to be SHELL=BOOL') from None

            if shell not in ['bash', 'fish', 'zsh']:
                raise Exception(f'Invalid shell: {shell}')

            if filter_ not in ['True', 'False']:
                raise Exception(f'Invalid filter: {filter_}')

            if shell in self.filters:
                raise Exception(f'Double shell key: {shell}')

            self.filters[shell] = {'True': True, 'False': False}[filter_]

    def accept(self, program):
        for shell, filter_ in self.filters.items():
            if shell == 'bash':
                if program.has_bash != filter_:
                    return False
            elif shell == 'fish':
                if program.has_fish != filter_:
                    return False
            elif shell == 'zsh':
                if program.has_zsh != filter_:
                    return False

        return True

# =============================================================================
# Command line arguments
# =============================================================================

p = argparse.ArgumentParser()
p.add_argument('-f', '--filter', metavar='SHELL=True|False',
    type=Filter, action='append',
    help='Filter results. Example: -f bash=True,zsh=False')
opts = p.parse_args()

# =============================================================================
# Collect data
# =============================================================================

bash_completions = get_bash_completions()
fish_completions = get_fish_completions()
zsh_completions = get_zsh_completions()

programs = set()
for path in PROGRAM_PATHS:
    programs.update(find_programs(path))
programs = sorted(programs)

# =============================================================================
# Filter and print results
# =============================================================================

for program in programs:
    program = Program(program,
        (program in bash_completions),
        (program in fish_completions),
        (program in zsh_completions))

    if opts.filter:
        for filter_ in opts.filter:
            if filter_.accept(program):
                program.print()
                break
    else:
        program.print()
