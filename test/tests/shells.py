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

class ShellBase:
    def __init__(self, term):
        self.term = term

    def stop(self):
        self.term.stop()

class BashShell(ShellBase):
    def start(self):
        self.term.start(['bash', '--norc', '--noprofile', '+o', 'history'], SHELL_ENV)

    def set_prompt(self):
        self.term.send_line("PS1='> '")

    def init_completion(self):
        self.term.send_line('source /usr/share/bash-completion/bash_completion')
        self.term.send_line('bind "set show-all-if-ambiguous on"')
        self.term.send_line('bind "set show-all-if-unmodified on"')

    def load_completion(self, file):
        self.term.send_line('source %s' % file)

class FishShell(ShellBase):
    def start(self):
        self.term.start(['fish', '--no-config'], SHELL_ENV)

    def set_prompt(self):
        self.term.send_line("function fish_prompt; printf '> '; end")

    def init_completion(self):
        pass

    def load_completion(self, file):
        self.term.send_line('source %s' % file)

class ZshShell(ShellBase):
    def start(self):
        self.term.start(['zsh', '--no-rcs'], SHELL_ENV)

    def set_prompt(self):
        self.term.send_line("PROMPT='> '")

    def init_completion(self):
        self.term.send_line('autoload -U compinit && compinit')
        time.sleep(0.5)

    def load_completion(self, file):
        self.term.send_line('source %s' % file)

