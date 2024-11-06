#!/usr/bin/python3

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

SHELLS = ['bash', 'fish', 'zsh']
TMUX_SESSION_PREFIX = 'crazy-complete-test'
TESTS_INFILE = 'tests.yaml'
TESTS_OUTFILE = 'tests.new.yaml'
CRAZY_COMPLETE = '../../crazy-complete'

os.chdir(os.path.dirname(os.path.abspath(__file__)))

argp = argparse.ArgumentParser()
argp.add_argument('-f', '--fast', action='store_true', default=False,
    help='Enable fast testing mode. For tests where the input matches the expected output, these tests will always pass')
argp.add_argument('-d', '--driver', default='pyte', choices=['pyte', 'tmux'],
    help='Select driver for tests')
opts = argp.parse_args()

if opts.driver == 'pyte':
    try:
        from pyte_driver import *
    except ImportError as e:
        print(e)
        print('Please install the missing modules.')
        print('Alternatively, you can use --driver=tmux if you have tmux installed')
        sys.exit(2)
elif opts.driver == 'tmux':
    from tmux_driver import *

def run(args, env=None):
    result = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=env)

    if result.returncode != 0:
        raise Exception("Command %r failed: %s" % (args, result.stderr))

    return result.stdout

for program in SHELLS:
    try:
        run(['sh', '-c', f'which {program}'])
    except:
        print(f'Program `{program}` not found')
        sys.exit(2)

if not os.path.exists('/usr/share/bash-completion/bash_completion'):
    print('File `/usr/share/bash-completion/bash_completion` not found. Is `bash-completion` installed?')
    sys.exit(2)

def generate_completion(shell, outfile, args):
    definition_file = args['definition_file']
    args = args['args']
    cmd = [CRAZY_COMPLETE, '--debug', '--zsh-compdef=False', *args, shell, '-o', outfile, definition_file]
    print('RUNNING:', cmd)
    run(cmd)

def indent(string, num_spaces):
    lines = string.split('\n')
    indented_lines = [((' ' * num_spaces) + line) if line.strip() else line for line in lines]
    return '\n'.join(indented_lines)

def make_yaml_block_string(s):
    return "|\n%s" % indent(s, 2)

def test_to_yaml(test):
    r = OrderedDict()
    r['number']         = str(test['number'])
    r['description']    = json.dumps(test['description'])
    if 'comment' in test:
        r['comment']    = json.dumps(test['comment'])
    r['send']           = json.dumps(test['send'])
    if test.get('bash_tabs', 1) != 1:
        r['bash_tabs']  = str(test['bash_tabs'])
    r['bash_expected']  = make_yaml_block_string(test['bash_result'])
    if test.get('fish_tabs', 1) != 1:
        r['fish_tabs']  = str(test['fish_tabs'])
    r['fish_expected']  = make_yaml_block_string(test['fish_result'])
    if test.get('zsh_tabs', 1) != 1:
        r['zsh_tabs']   = str(test['zsh_tabs'])
    r['zsh_expected']   = make_yaml_block_string(test['zsh_result'])
    return '\n'.join('%s: %s' % o for o in r.items())

class Tests:
    def __init__(self, tests):
        self.tests = tests

    def strip_expected(self):
        for test in self.tests:
            for key in ['bash_expected', 'zsh_expected', 'fish_expected']:
                if key in test:
                    test[key] = test[key].strip()

    def enumerate_tests(self):
        number = 1
        for test in self.tests:
            if 'send' in test:
                test['number'] = number
                number += 1

    def add_empty_expected(self):
        for test in self.tests:
            if 'generate-scripts' in test:
                continue
            test.setdefault('bash_expected', '')
            test.setdefault('fish_expected', '')
            test.setdefault('zsh_expected',  '')

    def find_test_by_number(self, num):
        for test in self.tests:
            if 'number' in test and test['number'] == num:
                return test

        raise Exception("No test with number %r found" % num)

    def write_tests_file(self, file):
        r = []
        for test in self.tests:
            if 'generate-scripts' in test:
                r += ['generate-scripts: %s' % json.dumps(test['generate-scripts'])]
            else:
                r += [test_to_yaml(test)]

        r = '\n---\n'.join(r)

        with open(file, 'w') as fh:
            fh.write(r)

def do_tests(tests, shell, result_queue):
    if opts.driver == 'tmux':
        term = TmuxTerminal(TMUX_SESSION_PREFIX + '-' + shell)
    elif opts.driver == 'pyte':
        term = PyteTerminal()

    term_shell = {'bash': BashShell, 'fish': FishShell, 'zsh': ZshShell}[shell](term)

    for test in tests:
        test = test.copy()
        if 'generate-scripts' in test:
            try:    term_shell.stop()
            except: pass
            completion_file = 'out.%s' % shell
            generate_completion(shell, completion_file, test['generate-scripts'])
            term_shell.start()
            term.resize_window(80, 100)
            term_shell.set_prompt()
            term_shell.init_completion()
            term_shell.load_completion(completion_file)
            time.sleep(0.5)

        else:
            result = {
                'number': test['number'],
                'shell':  shell,
                'result': term.complete(test['send'],
                                        test.get(shell+'_tabs', 1),
                                        test[shell+'_expected'],
                                        opts.fast)
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
        self.threads = []
        self.failed = False

    def run(self):
        for shell in SHELLS:
            thread = threading.Thread(target=do_tests, args=(self.tests.tests, shell, self.result_queue))
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
            self.failed = True
            print("Test #%02d (%-4s - %s) failed" % (test['number'], shell, test['description']))
        else:
            print("Test #%02d (%-4s - %s) OK" % (test['number'], shell, test['description']))

# =============================================================================
# Main
# =============================================================================

with open(TESTS_INFILE, 'r') as fh:
    tests = Tests(list(yaml.safe_load_all(fh)))

tests.enumerate_tests()
tests.add_empty_expected()
tests.strip_expected()
tester = Tester(tests)
tester.run()
tests.write_tests_file(TESTS_OUTFILE)
if tester.failed:
    sys.exit(1)
