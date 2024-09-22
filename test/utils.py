#!/usr/bin/python3

import os
import time
import subprocess

def run(args, env=None):
    result = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=env)

    if result.returncode != 0:
        raise Exception("Cmd %r failed: %s" % (args, result.stderr))

    return result.stdout

class TmuxClient:
    def __init__(self, session):
        self.session = session

    def run(self, args):
        env = os.environ.copy()
        env.pop('TMUX', None)
        return run(['tmux'] + args, env)

    def new_session(self, command_args=[]):
        self.run(['new-session', '-d', '-s', self.session] + command_args)

    def kill_session(self):
        self.run(['kill-session', '-t', self.session])

    def send_keys(self, *keys):
        self.run(['send-keys', '-t', self.session] + list(keys))

    def capture_pane(self):
        return self.run(['capture-pane', '-t', self.session, '-p'])

    def resize_window(self, x, y):
        self.run(['resize-window', '-t', self.session, '-x', str(x), '-y', str(y)])

class ShellBase:
    def __init__(self, tmux):
        self.tmux = tmux

    def stop(self):
        self.tmux.kill_session()

class BashShell(ShellBase):
    def start(self):
        self.tmux.new_session(['bash', '--norc'])

    def set_prompt(self):
        self.tmux.send_keys("PS1='> '\n")

    def init_completion(self):
        self.tmux.send_keys('source /usr/share/bash-completion/bash_completion\n')

    def load_completion(self, file):
        self.tmux.send_keys('source %s\n' % file)

class FishShell(ShellBase):
    def start(self):
        self.tmux.new_session(['fish', '--no-config'])

    def set_prompt(self):
        self.tmux.send_keys("function fish_prompt; printf '> '; end\n")

    def init_completion(self):
        pass

    def load_completion(self, file):
        self.tmux.send_keys('source %s\n' % file)

class ZshShell(ShellBase):
    def start(self):
        self.tmux.new_session(['zsh', '--no-rcs'])

    def set_prompt(self):
        self.tmux.send_keys("PROMPT='> '\n")

    def init_completion(self):
        self.tmux.send_keys('autoload -U compinit && compinit\n')
        time.sleep(0.5)

    def load_completion(self, file):
        self.tmux.send_keys('source %s\n' % file)

def complete(tmux, commandline, num_tabs=1):
    # Clear screen
    tmux.send_keys('C-c')
    tmux.send_keys('clear')
    tmux.send_keys('Enter')

    time.sleep(0.3)

    # Write commandline
    tmux.send_keys(commandline)

    # Write tabs
    for i in range(num_tabs):
        tmux.send_keys('Tab')

    time.sleep(1)

    result = tmux.capture_pane()
    result = result.rstrip()
    return result
