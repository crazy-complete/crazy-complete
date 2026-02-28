import time

SHELL_ENV = {
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

def wait_for_prompt(terminal):
    terminal.wait_for_text('>', 5, 0.1)

class ShellBase:
    def __init__(self, term):
        self.term = term

    def stop(self):
        self.term.stop()

class BashShell(ShellBase):
    def start(self):
        self.term.start(['bash', '--norc', '--noprofile', '+o', 'history'], SHELL_ENV)

    def set_prompt(self):
        self.term.send_line("clear; PS1='> '")
        wait_for_prompt(self.term)

    def init_completion(self):
        self.term.send_line('source /usr/share/bash-completion/bash_completion')
        self.term.send_line('bind "set show-all-if-ambiguous on"')
        self.term.send_line('bind "set show-all-if-unmodified on"')
        self.term.send_line('clear')
        wait_for_prompt(self.term)

    def load_completion(self, file):
        self.term.send_line('clear; source %s' % file)
        wait_for_prompt(self.term)

class FishShell(ShellBase):
    def start(self):
        self.term.start(['fish', '--no-config'], SHELL_ENV)

    def set_prompt(self):
        self.term.send_line("clear; function fish_prompt; printf '> '; end")
        wait_for_prompt(self.term)

    def init_completion(self):
        pass

    def load_completion(self, file):
        self.term.send_line('clear; source %s' % file)
        wait_for_prompt(self.term)

class ZshShell(ShellBase):
    def start(self):
        self.term.start(['zsh', '--no-rcs'], SHELL_ENV)

    def set_prompt(self):
        self.term.send_line("clear; PROMPT='> '")
        wait_for_prompt(self.term)

    def init_completion(self):
        self.term.send_line('clear; autoload -U compinit && compinit')
        wait_for_prompt(self.term)

    def load_completion(self, file):
        self.term.send_line('clear; source %s' % file)
        wait_for_prompt(self.term)
