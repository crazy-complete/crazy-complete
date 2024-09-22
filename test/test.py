#!/usr/bin/python3

import os
import sys
import time
import json
import yaml
import queue
import threading

from utils import *

SHELLS = ['bash', 'fish', 'zsh']
TMUX_SESSION_NAME = 'crazy-complete-test'
TESTS_INFILE = 'tests.yaml'
TESTS_OUTFILE = 'tests.new.yaml'

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def generate_completion(shell, outfile, args):
    run(['../crazy-complete', '--debug', '--input-type=python', shell, '-o', outfile, 'crazy-complete-test'] + args)

def test_to_str(test):
    r  = "number: %d\n"         % test['number']
    r += "description: %s\n"    % json.dumps(test['description'])
    if 'comment' in test:
        r += "comment: %s\n"    % json.dumps(test['comment'])
    r += "send: %s\n"           % json.dumps(test['send'])
    if test.get('bash_tabs', 1) != 1:
        r += "bash_tabs: %d\n"  % test['bash_tabs']
    r += "bash_expected: |\n%s\n" % indent(test['bash_result'], 2)
    if test.get('fish_tabs', 1) != 1:
        r += "fish_tabs: %d\n" % test['fish_tabs']
    r += "fish_expected: |\n%s\n" % indent(test['fish_result'], 2)
    if test.get('zsh_tabs', 1) != 1:
        r += "zsh_tabs: %d\n" % test['zsh_tabs']
    r += "zsh_expected: |\n%s"  % indent(test['zsh_result'], 2)
    return r

def indent(string, num_spaces):
    lines = string.split('\n')
    indented_lines = [((' ' * num_spaces) + line) if line.strip() else line for line in lines]
    return '\n'.join(indented_lines)

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

    def add_empty_expected_to_tests(self):
        for test in self.tests:
            if 'generate-scripts' in test:  continue
            if 'bash_expected' not in test: test['bash_expected'] = ''
            if 'fish_expected' not in test: test['fish_expected'] = ''
            if 'zsh_expected'  not in test: test['zsh_expected']  = ''

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
                r += [test_to_str(test)]

        r = '\n---\n'.join(r)

        with open(file, 'w') as fh:
            fh.write(r)

def do_tests(tests, shell, result_queue):
    tmux = TmuxClient(TMUX_SESSION_NAME + '-' + shell)
    tmux_shell = {'bash': BashShell, 'fish': FishShell, 'zsh': ZshShell}[shell](tmux)

    for test in tests:
        test = test.copy()
        if 'generate-scripts' in test:
            try:    tmux_shell.stop()
            except: pass
            completion_file = 'out.%s' % shell
            generate_completion(shell, completion_file, ['--zsh-compdef=False'] + test['generate-scripts'])
            tmux_shell.start()
            tmux.resize_window(80, 100)
            tmux_shell.set_prompt()
            tmux_shell.init_completion()
            tmux_shell.load_completion(completion_file)
            time.sleep(0.5)

        else:
            test[shell+'_result'] = complete(tmux, test['send'], test.get(shell+'_tabs', 1))
            result_queue.put(test)

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
            self.threads.append(thread)
            thread.start()

        while self.threads_are_running():
            self.eat_queue()
            time.sleep(0.5)
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
        test = tests.find_test_by_number(result['number'])
        for shell in SHELLS:
            shell_result_key   = '%s_result' % shell
            shell_expected_key = '%s_expected' % shell

            if shell_result_key in result:
                test[shell_result_key] = result[shell_result_key]

                if test[shell_result_key] != test[shell_expected_key]:
                    self.failed = True
                    print("Test #%02d (%-4s - %s) failed" % (test['number'], shell, test['description']))
                else:
                    print("Test #%02d (%-4s - %s) OK" % (test['number'], shell, test['description']))

                break

# =============================================================================
# Main
# =============================================================================

with open(TESTS_INFILE, 'r') as fh:
    tests = Tests(list(yaml.safe_load_all(fh)))

tests.strip_expected()
tests.enumerate_tests()
tests.add_empty_expected_to_tests()
tester = Tester(tests)
tester.run()
tests.write_tests_file(TESTS_OUTFILE)
if tester.failed:
    sys.exit(1)
