#!/usr/bin/env python3

import os
import sys
import time
import json
import yaml
import queue
import argparse
import threading
import subprocess
from collections import OrderedDict

from shells import *

# =============================================================================
# Script configuration
# =============================================================================

SHELLS              = ['bash', 'fish', 'zsh']
TMUX_SESSION_PREFIX = 'crazy-complete-test'
TESTS_INFILE        = 'tests.yaml'
TESTS_OUTFILE       = 'tests.new.yaml'
CRAZY_COMPLETE      = '../../crazy-complete'
COMPLETIONS_OUTDIR  = 'output'

# =============================================================================
# Switch to the script's directory
# =============================================================================

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# =============================================================================
# Commandline parser
# =============================================================================

argp = argparse.ArgumentParser()
argp.add_argument('-f', '--fast', action='store_true', default=False,
    help='Enable fast testing mode. For tests where the input matches the expected output, these tests will always pass')
argp.add_argument('-d', '--driver', default='pyte', choices=['pyte', 'tmux'],
    help='Select driver for tests')
argp.add_argument('-t', '--threads', default=1, type=int,
    help='Set the number of threads per shell')
opts = argp.parse_args()

# =============================================================================
# Helper functions
# =============================================================================

def print_err(*args):
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

def test_to_yaml(test):
    r = OrderedDict()

    r['number']          = str(test['number'])
    r['definition_file'] = json.dumps(test['definition_file'])
    r['description']     = json.dumps(test['description'])
    if 'comment' in test:
        r['comment']     = json.dumps(test['comment'])
    r['send']            = json.dumps(test['send'])
    if test.get('bash_tabs', 1) != 1:
        r['bash_tabs']   = str(test['bash_tabs'])
    r['bash_expected']   = make_yaml_block_string(test['bash_result'])
    if test.get('fish_tabs', 1) != 1:
        r['fish_tabs']   = str(test['fish_tabs'])
    r['fish_expected']   = make_yaml_block_string(test['fish_result'])
    if test.get('zsh_tabs', 1) != 1:
        r['zsh_tabs']    = str(test['zsh_tabs'])
    r['zsh_expected']    = make_yaml_block_string(test['zsh_result'])

    return '\n'.join('%s: %s' % key_value for key_value in r.items())

# =============================================================================
# Import driver depending on command line arguments
# =============================================================================

if opts.driver == 'pyte':
    try:
        from pyte_driver import *
    except ImportError as e:
        print_err(e)
        print_err('Please install the missing modules.')
        print_err('Alternatively, you can use --driver=tmux if you have tmux installed')
        sys.exit(2)
elif opts.driver == 'tmux':
    from tmux_driver import *

# =============================================================================
# Ensure all dependencies are available
# =============================================================================

for program in SHELLS:
    try:
        run(['sh', '-c', f'type {program}'])
    except:
        print_err(f'Program `{program}` not found')
        sys.exit(2)

if not os.path.exists('/usr/share/bash-completion/bash_completion'):
    print_err('File `/usr/share/bash-completion/bash_completion` not found. Is `bash-completion` installed?')
    sys.exit(2)

# =============================================================================
# Test code
# =============================================================================

class Tests:
    def __init__(self, tests):
        self.definition_files = tests.pop(0)
        self.tests = tests

    def enumerate_tests(self):
        number = 1
        for test in self.tests:
            test['number'] = number
            number += 1

    def add_empty_expected(self):
        for test in self.tests:
            test.setdefault('bash_expected', '')
            test.setdefault('fish_expected', '')
            test.setdefault('zsh_expected',  '')

    def strip_expected(self):
        for test in self.tests:
            for key in ['bash_expected', 'fish_expected', 'zsh_expected']:
                test[key] = test[key].strip()

    def find_test_by_number(self, num):
        for test in self.tests:
            if test['number'] == num:
                return test

        raise Exception(f"No test with number {num} found")

    def write_tests_file(self, outfile):
        r = []

        files = ''
        for file, args in self.definition_files.items():
            files += '%s: %s\n' % (file, json.dumps(args))
        r += [files.strip()]

        for test in self.tests:
            r += [test_to_yaml(test)]

        r = '\n---\n'.join(r)

        with open(outfile, 'w') as fh:
            fh.write(r)

    def generate_completion_files(self):
        try:
            os.mkdir(COMPLETIONS_OUTDIR)
        except FileExistsError:
            if not os.path.isdir(COMPLETIONS_OUTDIR):
                raise NotADirectoryError(COMPLETIONS_OUTDIR) from None

        print_err('Generating completion files ...')
        for file, args in self.definition_files.items():
            for shell in SHELLS:
                cmd =  [CRAZY_COMPLETE, '--debug', '--zsh-compdef=False']
                cmd += args['args']
                cmd += ['-o', f'{COMPLETIONS_OUTDIR}/{file}.{shell}']
                cmd += [shell, args['definition_file']]
                print_err('Running', ' '.join(cmd))
                run(cmd)

def tests_worker_thread(thread_id, shell, input_queue, result_queue):
    if opts.driver == 'tmux':
        term = TmuxTerminal(f'{TMUX_SESSION_PREFIX}-{shell}-{thread_id}')
    elif opts.driver == 'pyte':
        term = PyteTerminal()

    term_shell = {
        'bash': BashShell,
        'fish': FishShell,
        'zsh':  ZshShell
    }[shell](term)

    old_definition_file = None

    while True:
        try:
            test = input_queue.get_nowait()
        except queue.Empty:
            break

        if old_definition_file != test['definition_file']:
            old_definition_file = test['definition_file']

            try:    term_shell.stop()
            except: pass
            completion_file = '%s/%s.%s' % (COMPLETIONS_OUTDIR, test['definition_file'], shell)
            term_shell.start()
            term.resize_window(80, 100)
            term_shell.set_prompt()
            term_shell.init_completion()
            term_shell.load_completion(completion_file)
            time.sleep(1.5)

        output = term.complete(
            test['send'],
            test.get(shell+'_tabs', 1),
            test[shell+'_expected'],
            opts.fast)

        result = {
            'number': test['number'],
            'shell':  shell,
            'result': output
        }

        result_queue.put(result)

    try:
        term_shell.stop()
    except:
        pass

class Tester():
    def __init__(self, tests):
        self.tests = tests
        self.result_queue = queue.Queue()
        self.input_queues = {}
        self.threads = []
        self.num_failed = 0

    def run(self):
        for shell in SHELLS:
            self.input_queues[shell] = queue.Queue()
            for test in self.tests.tests:
                self.input_queues[shell].put(test)

        for thread_id in range(opts.threads):
            for shell in SHELLS:
                thread = threading.Thread(
                    target=tests_worker_thread,
                    args=(thread_id, shell, self.input_queues[shell], self.result_queue)
                )

                thread.start()
                self.threads.append(thread)

        while self.threads_are_running():
            self.eat_queue()
            time.sleep(0.1)
        self.eat_queue()

    def threads_are_running(self):
        for thread in self.threads:
            if thread.is_alive():
                return True
        return False

    def eat_queue(self):
        while not self.result_queue.empty():
            self.process_result(self.result_queue.get())

    def process_result(self, result):
        test = self.tests.find_test_by_number(result['number'])
        shell = result['shell']
        shell_result_key   = '%s_result'   % shell
        shell_expected_key = '%s_expected' % shell
        test[shell_result_key] = result['result']

        if test[shell_result_key] != test[shell_expected_key]:
            self.num_failed += 1
            print_err("Test #%02d (%-4s - %s) failed" % (test['number'], shell, test['description']))
        else:
            print_err("Test #%02d (%-4s - %s) OK" % (test['number'], shell, test['description']))

# =============================================================================
# Main
# =============================================================================

with open(TESTS_INFILE, 'r') as fh:
    tests = Tests(list(yaml.safe_load_all(fh)))

tests.enumerate_tests()
tests.add_empty_expected()
tests.strip_expected()
tests.generate_completion_files()
tester = Tester(tests)
tester.run()
tests.write_tests_file(TESTS_OUTFILE)
if tester.num_failed:
    print_err(f'{tester.num_failed} tests failed.')
    print_err(f'Use diff or vimdiff on `{TESTS_INFILE}` and `{TESTS_OUTFILE}` for further details')
    if opts.threads > 2:
        print_err('NOTE:')
        print_err(' A high value for -t|--threads may cause that tests fail.')
        print_err(' Consider running this script again with `-t 1`.')
    sys.exit(1)
else:
    print_err("All tests passed")
    sys.exit(0)
