import os
import time
import subprocess

def run(args, env=None):
    result = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=env)

    if result.returncode != 0:
        raise Exception("Command %r failed: %s" % (args, result.stderr))

    return result.stdout

class TmuxClient:
    def __init__(self, session):
        self.session = session

    def run(self, args):
        env = os.environ.copy()
        env.pop('TMUX', None)
        return run(['tmux'] + args, env)

    def new_session(self, command_args=[]):
        tmux_env = {
            # disable readline's rcfile for bash
            'INPUTRC': '/dev/null',

            # set locale to C to ensure same ordering of options
            'LANG':              'C',
            'LC_CTYPE':          'C',
            'LC_NUMERIC':        'C',
            'LC_TIME':           'C',
            'LC_COLLATE':        'C',
            'LC_MONETARY':       'C',
            'LC_MESSAGES':       'C',
            'LC_PAPER':          'C',
            'LC_NAME':           'C',
            'LC_ADDRESS':        'C',
            'LC_TELEPHONE':      'C',
            'LC_MEASUREMENT':    'C',
            'LC_IDENTIFICATION': 'C',
            'LC_ALL':            'C'
        }

        tmux_env_args = []
        for var, value in tmux_env.items():
            tmux_env_args.append(f'-e{var}={value}')

        cmd = ['new-session', '-d', '-s', self.session]
        cmd.extend(tmux_env_args)
        cmd.extend(command_args)
        self.run(cmd)

    def kill_session(self):
        self.run(['kill-session', '-t', self.session])

    def send_keys(self, *keys):
        self.run(['send-keys', '-t', self.session] + list(keys))

    def capture_pane(self):
        return self.run(['capture-pane', '-t', self.session, '-p'])

    def resize_window(self, x, y):
        self.run(['resize-window', '-t', self.session, '-x', str(x), '-y', str(y)])

    def wait_for_text(self, expected, timeout, poll_interval):
        while timeout > 0.0:
            result = self.capture_pane().strip()
            if result == expected:
                return result
            timeout -= poll_interval
            time.sleep(poll_interval)
        return self.capture_pane().strip()

class ShellBase:
    def __init__(self, tmux):
        self.tmux = tmux

    def stop(self):
        self.tmux.kill_session()

class BashShell(ShellBase):
    def start(self):
        self.tmux.new_session(['bash', '--norc', '--noprofile', '+o', 'history'])

    def set_prompt(self):
        self.tmux.send_keys("PS1='> '\n")

    def init_completion(self):
        self.tmux.send_keys('source /usr/share/bash-completion/bash_completion\n')
        self.tmux.send_keys('bind "set show-all-if-ambiguous on"\n')
        self.tmux.send_keys('bind "set show-all-if-unmodified on"\n')

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

def clear_screen(tmux):
    tmux.send_keys('C-c')
    tmux.send_keys('clear')
    tmux.send_keys('Enter')

    result = tmux.wait_for_text('>', 1, 0.01)
    if result != '>':
        # Idk why, but sometime we have to try again
        clear_screen(tmux)

def complete(tmux, commandline, num_tabs=1, expected=None, fast=False):
    clear_screen(tmux)

    # Write commandline
    tmux.send_keys(commandline)

    # Write tabs
    for i in range(num_tabs):
        tmux.send_keys('Tab')

    if fast:
        return tmux.wait_for_text(expected, 1, 0.01)
    else:
        time.sleep(1)
        return tmux.capture_pane().strip()
