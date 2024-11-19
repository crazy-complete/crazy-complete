#!/usr/bin/env python3

import os
import re
import shlex

PATHS = ['/bin', '/sbin', '/usr/bin', '/usr/sbin']
BASH_COMPLETION_PATHS = ['/etc/bash_completion.d', '/usr/share/bash-completion/completions']
FISH_COMPLETION_PATHS = ['/usr/share/fish/completions', '/usr/share/fish/vendor_completions.d']
ZSH_COMPLETION_PATHS = '''\
/usr/share/zsh/site-functions
/usr/share/zsh/functions/Zle
/usr/share/zsh/functions/VCS_Info
/usr/share/zsh/functions/VCS_Info/Backends
/usr/share/zsh/functions/Chpwd
/usr/share/zsh/functions/MIME
/usr/share/zsh/functions/Newuser
/usr/share/zsh/functions/TCP
/usr/share/zsh/functions/Math
/usr/share/zsh/functions/Calendar
/usr/share/zsh/functions/Exceptions
/usr/share/zsh/functions/Prompts
/usr/share/zsh/functions/Zftp
/usr/share/zsh/functions/Misc
/usr/share/zsh/functions/Completion
/usr/share/zsh/functions/Completion/Linux
/usr/share/zsh/functions/Completion/Unix
/usr/share/zsh/functions/Completion/Base
/usr/share/zsh/functions/Completion/Zsh
/usr/share/zsh/functions/Completion/X'''.split('\n')

def find_programs(path):
    try:
        return os.listdir(path)
    except FileNotFoundError:
        pass

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
    r = []

    for path in BASH_COMPLETION_PATHS:
        try:
            files = sorted(os.listdir(path))
        except FileNotFoundError:
            continue

        for file in files:
            with open(os.path.join(path, file), 'r') as fh:
                content = fh.read()

            content = content.replace('\\\n', '')

            for line in content.split('\n'):
                m = re.search('complete [^;&|]+', line)
                if m:
                    programs = parse_bash_complete_command(m[0])
                    r.extend(programs)

    return sorted(set(r))

def get_fish_completions():
    r = []

    for path in FISH_COMPLETION_PATHS:
        try:
            files = sorted(os.listdir(path))
        except FileNotFoundError:
            continue

        for file in files:
            with open(os.path.join(path, file), 'r') as fh:
                content = fh.read()

            content = content.replace('\\\n', '')

            for line in content.split('\n'):
                m = re.search('complete .*', line)
                if m:
                    programs = parse_fish_complete_command(m[0])
                    r.extend(programs)

    return sorted(set(r))

def get_zsh_completions():
    r = []

    for path in ZSH_COMPLETION_PATHS:
        try:
            files = sorted(os.listdir(path))
        except FileNotFoundError:
            continue

        for file in files:
            try:
                with open(os.path.join(path, file), 'r') as fh:
                    content = fh.read()
            except IsADirectoryError:
                continue

            content = content.replace('\\\n', '')

            for line in content.split('\n'):
                m = re.search('#compdef .*', line)
                if m:
                    programs = parse_zsh_compdef(m[0])
                    r.extend(programs)

    return sorted(set(r))

fish_completions = get_fish_completions()
bash_completions = get_bash_completions()
zsh_completions = get_zsh_completions()

programs = set()
for path in PATHS:
    programs.update(find_programs(path))
programs = sorted(programs)

for program in programs:
    have_bash_completion = (program in bash_completions)
    have_fish_completion = (program in fish_completions)
    have_zsh_completion  = (program in zsh_completions)

    print('%-40s %-5s %-5s %-5s' % (program, have_bash_completion, have_fish_completion, have_zsh_completion))

