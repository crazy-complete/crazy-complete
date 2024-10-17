#!/usr/bin/python3

'''
This script is for checking error messages of cracy-complete.
'''

import os
import sys
import yaml

SCRIPT_FILE = os.path.basename(__file__)
SCRIPT_DIR  = os.path.dirname(__file__)

# We want to import the development version of cracy-complete,
# not the installed version.
CRAZY_COMPLETE_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..'))
sys.path.insert(0, CRAZY_COMPLETE_DIR)

import crazy_complete

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def load_definition_file(file):
    expected_error = None

    with open(file, 'r') as fh:
        definition = list(yaml.safe_load_all(fh))

    for dictionary in definition:
        if 'expected_error' in dictionary:
            expected_error = dictionary['expected_error']
            definition.remove(dictionary)
            return (definition, expected_error)

    raise Exception(f'Did not found `expected_error` in `{file}`')

def run_test(definition, expected_error):
    print(f'Testing {file}', end=' ... ')

    have_error = ''

    try:
        cmdline = crazy_complete.dictionary_source.dictionaries_to_commandline(definition)
        crazy_complete.bash.generate_completion(cmdline, None, None)
    except crazy_complete.errors.CrazyError as e:
        have_error = str(e)

    if have_error != expected_error:
        print('Failed')
        print('Expected:', expected_error)
        print('Having:  ', have_error)
        sys.exit(1)
    else:
        print('OK')

for file in sorted(os.listdir('.')):
    if file in (SCRIPT_FILE, 'TODO'):
        continue

    definition, expected_error = load_definition_file(file)
    run_test(definition, expected_error)
