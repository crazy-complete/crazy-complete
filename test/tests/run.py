#!/usr/bin/env python3

import os
import sys
import time
import json
import shlex
import yaml
import argparse
import subprocess
import threading
import difflib
from collections import OrderedDict
from concurrent.futures import ThreadPoolExecutor

from shells import BashShell, FishShell, ZshShell

# =============================================================================
# Script configuration
# =============================================================================

SHELLS              = ['bash', 'fish', 'zsh']
TMUX_SESSION_PREFIX = 'crazy-complete-test'
TESTS_FILENAME      = 'tests.yaml'
RESULTS_FILENAME    = 'tests.new.yaml'
CRAZY_COMPLETE      = [sys.executable, '-m', 'crazy_complete.main']
COMPLETIONS_OUTDIR  = 'output'
TEMP_DIR            = 'tmp'
OUTPUT_WAIT         = 5

# =============================================================================
# Switch to the script's directory
# =============================================================================

os.chdir(os.path.dirname(os.path.abspath(__file__)))
CURRENT_DIRECTORY = os.path.abspath(os.getcwd())

# =============================================================================
# Override PYTHONPATH
# =============================================================================

os.environ['PYTHONPATH'] = '../..'

# =============================================================================
# Commandline parser
# =============================================================================

argp = argparse.ArgumentParser()
argp.add_argument('-f', '--fast', action='store_true', default=False,
    help='Enable fast testing mode. For tests where the input matches the expected output, these tests will always pass')
argp.add_argument('-d', '--driver', default='tmux', choices=['pyte', 'tmux'],
    help='Select driver for tests')
argp.add_argument('-w', '--wait', default=OUTPUT_WAIT, type=float,
    help='Set how many seconds to wait for terminal output')
argp.add_argument('-s', '--select', action='append',
    help='Select test directories to run')
argp.add_argument('-t', '--threaded', action='store_true', default=False,
    help='Run each shell of a test-file in its own thread (the three shells of one file run concurrently)')
argp.add_argument('-p', '--parallel', default=1, type=int,
    help='Max number of test-files to run in parallel (default 1); <= 0 runs all files at once')
opts = argp.parse_args()

OUTPUT_WAIT = opts.wait

# =============================================================================
# Helper functions
# =============================================================================

PRINT_LOCK = threading.Lock()

def print_err(*args):
    with PRINT_LOCK:
        print(*args, file=sys.stderr)

def run(args, env=None):
    result = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=env)

    if result.returncode != 0:
        raise Exception("Command %r failed: %s" % (args, result.stderr))

    return result.stdout

def indent(string, num_spaces):
    lines = string.split('\n')
    indented_lines = [((' ' * num_spaces) + line) if line.strip() else line for line in lines]
    return '\n'.join(indented_lines)

def make_yaml_block_string(s):
    return "|\n%s" % indent(s, 2)

def generate_diff(base_file, new_file):
    with open(base_file) as f:
        a = [line.rstrip('\n') for line in f]
    if os.path.exists(new_file):
        with open(new_file) as f:
            b = [line.rstrip('\n') for line in f]
    else:
        b = []
    return '\n'.join(difflib.unified_diff(a, b, fromfile=base_file, tofile=new_file, lineterm=''))

# =============================================================================
# Import driver depending on command line arguments
# =============================================================================

if opts.driver == 'tmux':
    from tmux_driver import TmuxTerminal
elif opts.driver == 'pyte':
    print_err("The `pyte` driver has been disabled because it does not implement the `kitty`")
    print_err("protocol used by the Fish shell, causing tests to fail.")
    sys.exit(2)

# =============================================================================
# Ensure all dependencies are available
# =============================================================================

for shell in SHELLS:
    try:
        run(['sh', '-c', f'type {shell}'])
    except Exception:
        print_err(f'Program `{shell}` not found')
        sys.exit(2)

if not os.path.exists('/usr/share/bash-completion/bash_completion'):
    print_err('File `/usr/share/bash-completion/bash_completion` not found. Is `bash-completion` installed?')
    sys.exit(2)

# =============================================================================
# Test code
# =============================================================================

class Test:
    def __init__(self, data):
        self.number = data.get('number', None)
        self.definition_file = data.get('definition_file')
        self.description = data['description']
        self.comment = data.get('comment', None)
        self.send = data['send']
        self.require_order = data.get('require_order', False)
        self.bash_tabs = data.get('bash_tabs', 1)
        self.fish_tabs = data.get('fish_tabs', 1)
        self.zsh_tabs = data.get('zsh_tabs', 1)
        self.bash_expected = data.get('bash_expected', '').strip()
        self.fish_expected = data.get('fish_expected', '').strip()
        self.zsh_expected = data.get('zsh_expected', '').strip()
        self.bash_result = None
        self.fish_result = None
        self.zsh_result = None

    def get_tabs(self, shell):
        if shell == 'bash':
            return self.bash_tabs
        if shell == 'fish':
            return self.fish_tabs
        if shell == 'zsh':
            return self.zsh_tabs
        raise

    def get_expected(self, shell):
        if shell == 'bash':
            return self.bash_expected
        if shell == 'fish':
            return self.fish_expected
        if shell == 'zsh':
            return self.zsh_expected

    def get_result(self, shell):
        if shell == 'bash':
            return self.bash_result
        if shell == 'fish':
            return self.fish_result
        if shell == 'zsh':
            return self.zsh_result
        raise

    def set_result(self, shell, result):
        if shell == 'bash':
            self.bash_result = result
        elif shell == 'fish':
            self.fish_result = result
        elif shell == 'zsh':
            self.zsh_result = result
        else:
            raise

    def passed(self, shell):
        result = self.get_result(shell)
        expected = self.get_expected(shell)

        if self.require_order:
            return result.split() == expected.split()
        else:
            return sorted(result.split()) == sorted(expected.split())

    def to_yaml(self):
        r = OrderedDict()

        r['number']          = str(self.number)
        if self.definition_file is not None:
            r['definition_file'] = json.dumps(self.definition_file)
        r['description']     = json.dumps(self.description)
        if self.comment:
            r['comment']     = json.dumps(self.comment)
        r['send']            = json.dumps(self.send)
        if self.require_order:
            r['require_order'] = 'true'
        if self.bash_tabs != 1:
            r['bash_tabs']   = str(self.bash_tabs)
        r['bash_expected']   = make_yaml_block_string(self.bash_result)
        if self.fish_tabs != 1:
            r['fish_tabs']   = str(self.fish_tabs)
        r['fish_expected']   = make_yaml_block_string(self.fish_result)
        if self.zsh_tabs != 1:
            r['zsh_tabs']    = str(self.zsh_tabs)
        r['zsh_expected']    = make_yaml_block_string(self.zsh_result)

        return '\n'.join('%s: %s' % key_value for key_value in r.items())

class Tests:
    def __init__(self, tests):
        self.definition_files = tests.pop(0)
        self.tests = [Test(data) for data in tests]

    def write_tests_file(self, outfile):
        r = []

        files = ''
        for file, args in self.definition_files.items():
            files += '%s: %s\n' % (file, json.dumps(args))
        r += [files.strip()]

        for test in self.tests:
            r += [test.to_yaml()]

        r = '\n---\n'.join(r)

        with open(outfile, 'w') as fh:
            fh.write(r + '\n')

    def generate_completion_files(self, directory):
        temp_directory = '%s/%s' % (TEMP_DIR, directory)
        os.makedirs(temp_directory, exist_ok=True)

        batch_commands = []
        name = os.path.basename(directory.rstrip('/'))

        definition_file = self.definition_files['definition_file']
        args_list = self.definition_files['args']
        temp_definition_file = '%s/%s' % (temp_directory, definition_file)

        with open('%s/%s' % (directory, definition_file), 'r', encoding='UTF-8') as fh:
            content = fh.read()
            content = content.replace('%TEST_DIR%', CURRENT_DIRECTORY)

        with open(temp_definition_file, 'w', encoding='UTF-8') as fh:
            fh.write(content)

        for shell in SHELLS:
            cmd =  ['--debug', '--zsh-compdef=False']
            cmd += [arg.replace('$shell', shell) for arg in args_list]
            cmd += ['-o', f'{COMPLETIONS_OUTDIR}/{name}.{shell}']
            cmd += [shell, temp_definition_file]
            cmd = ' '.join(shlex.quote(arg) for arg in cmd)
            batch_commands.append(cmd)

        return batch_commands

# =============================================================================
# Test directories
# =============================================================================

def get_test_directories(selected):
    directories = []
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in (COMPLETIONS_OUTDIR, TEMP_DIR)]
        if TESTS_FILENAME in files:
            rel = os.path.relpath(root, '.')
            if rel != '.':
                directories.append(rel)
    directories = sorted(directories)

    if selected is None:
        return directories

    basenames = {os.path.basename(d.rstrip('/')) for d in directories}
    unknown = [s for s in selected if s not in directories and s not in basenames]
    if unknown:
        print_err('Unknown test directory: %s' % ', '.join(unknown))
        print_err('Available test directories: %s' % ', '.join(directories))
        sys.exit(2)

    result = []
    for s in selected:
        if s in directories:
            result.append(s)
        else:
            result += [d for d in directories if os.path.basename(d.rstrip('/')) == s]

    return list(dict.fromkeys(result))

# =============================================================================
# Test runner
# =============================================================================

def run_directory(shell, name, tests):
    print_err('Running `%s` (%s) ...' % (name, shell))

    term = TmuxTerminal(f'{TMUX_SESSION_PREFIX}-{name}-{shell}')

    term_shell = {
        'bash': BashShell,
        'fish': FishShell,
        'zsh':  ZshShell
    }[shell](term)

    completion_file = '%s/%s.%s' % (COMPLETIONS_OUTDIR, name, shell)
    num_failed = 0

    try:
        term_shell.start()
        term.resize_window(80, 100)
        term_shell.set_prompt()
        term_shell.init_completion()
        term_shell.load_completion(completion_file)
        time.sleep(1.5)

        for test in tests.tests:
            result = term.complete(
                test.send,
                test.get_tabs(shell),
                OUTPUT_WAIT,
                test.get_expected(shell),
                opts.fast)

            test.set_result(shell, result)

            if not test.passed(shell):
                num_failed += 1
                print_err("Test #%03d (%-4s - %s) failed" % (test.number, shell, test.description))
            else:
                print_err("Test #%03d (%-4s - %s) OK" % (test.number, shell, test.description))
    finally:
        try:
            term_shell.stop()
        except Exception:
            pass

    return num_failed

def run_group(directory, tests, threaded):
    if not tests.tests:
        return 0

    name = os.path.basename(directory.rstrip('/'))

    if not threaded:
        return sum(run_directory(shell, name, tests) for shell in SHELLS)

    with ThreadPoolExecutor(max_workers=len(SHELLS)) as ex:
        futures = [ex.submit(run_directory, shell, name, tests) for shell in SHELLS]
        return sum(f.result() for f in futures)

# =============================================================================
# Main
# =============================================================================

test_directories = get_test_directories(opts.select)

test_groups = []
for directory in test_directories:
    with open('%s/%s' % (directory, TESTS_FILENAME), 'r') as fh:
        test_groups.append((directory, Tests(list(yaml.safe_load_all(fh)))))

os.makedirs(COMPLETIONS_OUTDIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)

batch_file = '%s/%s' % (TEMP_DIR, 'batch.txt')
batch_commands = []
for directory, tests in test_groups:
    batch_commands += tests.generate_completion_files(directory)

with open(batch_file, 'w', encoding='utf-8') as fh:
    print_err("Writing batch file '%s' ..." % batch_file)
    fh.write('\n'.join(batch_commands))

print_err('Running batch file ...')
args = [*CRAZY_COMPLETE, '--batch', batch_file]
subprocess.run(args, check=True)
print_err('Finished running batch file ...')

if opts.parallel <= 0:
    resolved_workers = max(1, len(test_groups))
else:
    resolved_workers = max(1, opts.parallel)

num_total   = sum(len(tests.tests) * len(SHELLS) for _, tests in test_groups)
num_failed  = 0
failed_groups = []
with ThreadPoolExecutor(max_workers=resolved_workers) as ex:
    futures = {ex.submit(run_group, directory, tests, opts.threaded): (directory, tests)
        for directory, tests in test_groups}
    for fut, group in futures.items():
        n = fut.result()
        num_failed += n
        if n:
            failed_groups.append(group)

for directory, tests in test_groups:
    outfile = '%s/%s' % (directory, RESULTS_FILENAME)
    tests.write_tests_file(outfile)

if num_failed:
    for directory, tests in failed_groups:
        base = os.path.join(directory, TESTS_FILENAME)
        new  = os.path.join(directory, RESULTS_FILENAME)
        print_err('%s failed:' % base)
        diff = generate_diff(base, new)
        if diff:
            print_err(diff)
        else:
            print_err('(tests.yaml and tests.new.yaml are identical)')
        print_err('')
    print_err('The following test files failed:')
    for directory, tests in failed_groups:
        print_err('%s' % os.path.join(directory, TESTS_FILENAME))
    print_err('')
    print_err(f'{num_failed} tests failed.')
    sys.exit(1)
else:
    print_err(f'All {num_total} tests passed.')
    sys.exit(0)
