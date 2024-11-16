import os
import sys
import subprocess

from terminal_base import TerminalBase

def run(args, env=None):
    result = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=env)

    if result.returncode != 0:
        raise Exception("Command %r failed: %s" % (args, result.stderr))

    return result.stdout

try:
    run(['sh', '-c', 'which tmux'])
except Exception:
    print('Program `tmux` not found.')
    sys.exit(2)

class TmuxTerminal(TerminalBase):
    def __init__(self, session):
        self.session = session

    def _run(self, args):
        env = os.environ.copy()
        env.pop('TMUX', None)
        return run(['tmux'] + args, env)

    def start(self, command_args=(), env=None):
        tmux_env_args = []

        if env:
            for var, value in env.items():
                tmux_env_args.append(f'-e{var}={value}')

        cmd = ['new-session', '-d', '-s', self.session]
        cmd.extend(tmux_env_args)
        cmd.extend(command_args)
        self._run(cmd)

    def stop(self):
        self._run(['kill-session', '-t', self.session])

    def resize_window(self, x, y):
        self._run(['resize-window', '-t', self.session, '-x', str(x), '-y', str(y)])

    def send(self, line):
        self._run(['send-keys', '-t', self.session, line])

    def send_line(self, line):
        self._run(['send-keys', '-t', self.session, f'{line}\n'])

    def send_tab(self):
        self._run(['send-keys', '-t', self.session, 'Tab'])

    def send_ctrl_c(self):
        self._run(['send-keys', '-t', self.session, 'C-c'])

    def get_output(self):
        return self._run(['capture-pane', '-t', self.session, '-p'])
