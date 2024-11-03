#!/usr/bin/python3

import os
import sys
import time
import json
import yaml
import queue
import argparse
import threading
from collections import OrderedDict

from utils import *

SHELLS = ['bash', 'fish', 'zsh']
TMUX_SESSION_PREFIX = 'crazy-complete-test'
TESTS_INFILE = 'tests.yaml'
TESTS_OUTFILE = 'tests.new.yaml'
CRAZY_COMPLETE = '../../crazy-complete'

os.chdir(os.path.dirname(os.path.abspath(__file__)))

argp = argparse.ArgumentParser()
argp.add_argument('-f', '--fast', action='store_true', default=False,
                  help='Enable fast testing mode. For tests where the input matches the expected output, these tests will always pass.')
opts = argp.parse_args()

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
    tmux = TmuxClient(TMUX_SESSION_PREFIX + '-' + shell)
    tmux_shell = {'bash': BashShell, 'fish': FishShell, 'zsh': ZshShell}[shell](tmux)

    for test in tests:
        test = test.copy()
        if 'generate-scripts' in test:
            try:    tmux_shell.stop()
            except: pass
            completion_file = 'out.%s' % shell
            generate_completion(shell, completion_file, test['generate-scripts'])
            tmux_shell.start()
            tmux.resize_window(80, 100)
            tmux_shell.set_prompt()
            tmux_shell.init_completion()
            tmux_shell.load_completion(completion_file)
            time.sleep(0.5)

        else:
            result = {
                'number': test['number'],
                'shell':  shell,
                'result': complete(tmux, test['send'],
                                         test.get(shell+'_tabs', 1),
                                         test[shell+'_expected'],
                                         opts.fast)
            }
            result_queue.put(result)

    try:
        tmux_shell.stop()
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
