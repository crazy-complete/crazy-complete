#!/usr/bin/env python3

import sys
import subprocess
import crazy_complete

def get_msg_ids():
    '''Return an array of possible msg ids.'''
    cmd = "pylint --list-msgs | grep -Eo '^:[^ ]+' | tr -d :"
    r = subprocess.run(['sh', '-c', cmd], stdout=subprocess.PIPE, text=True, check=True)
    return r.stdout.split()

# These options are mutually exclusive
MUTEX_GROUP = '--help --rcfile --output --help-msg --list-msgs --list-msgs-enabled --list-groups --list-conf-levels --list-extensions --full-documentation --generate-rcfile --generate-toml-config --long-help'.split()

# These options take a file as argument
FILE_OPTIONS = '--import-graph --ext-import-graph --int-import-graph --rcfile --output --spelling-private-dict-file'.split()

try:
    in_file = sys.argv[1]
except IndexError:
    raise Exception('Missing input file argument') from None

cmdline = crazy_complete.yaml_source.load_from_file(in_file)

cmdline.help = 'static code analyser for Python 2 or 3'

cmdline.add_positional(1, metavar='FILE', repeatable=True, complete=['file'])

for option in cmdline.options:
    for option_string in option.option_strings:
        if option_string in MUTEX_GROUP:
            option.groups = ['group1']

        if option_string in FILE_OPTIONS:
            option.complete = ['file']

    if '--help-msg' in option.option_strings:
        option.help = option.help.replace('[HELP_MSG ...] ', '')
        
    if option.metavar in ('<y or n>', '<yn>'):
        option.complete = ['choices', ['y', 'n']]

    elif option.metavar == '<style>':
        option.complete = ['choices', ['snake_case', 'camelCase', 'PascalCase', 'UPPER_CASE', 'any']]

    elif option.metavar == '<msg ids>':
        option.complete = ['value_list', {'values': get_msg_ids()}]

    elif "--logging-format-style" in option.option_strings:
        option.complete = ['choices', ['new', 'old']]

    if option.metavar and not option.complete:
        option.complete = ["none"]

for option in cmdline.options:
    if option.metavar and option.complete[0] == 'none':
        print('Option %r=%s has no complete' % (option.option_strings, option.metavar), file=sys.stderr)

output = crazy_complete.yaml_source.commandline_to_yaml(cmdline)

print(output)
