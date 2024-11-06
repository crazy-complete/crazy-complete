import os
import pyte
import pexpect

from terminal_base import TerminalBase

class PyteTerminal(TerminalBase):
    def __init__(self, width=80, height=100):
        self.width = width
        self.height = height
        self.screen = pyte.Screen(width, height)
        self.stream = pyte.Stream(self.screen)
    
    def start(self, command_args, env=None):
        spawn_env = None
        if env:
            spawn_env = os.environ.copy()
            spawn_env.update(env)

        command = command_args.pop(0)
        self.terminal = pexpect.spawn(command, command_args, dimensions=(self.height, self.width), env=spawn_env)

    def stop(self):
        self.terminal.close()

    def resize_window(self, x, y):
        pass # TODO
    
    def send(self, text):
        self.terminal.send(text)

    def send_line(self, line):
        self.terminal.sendline(line)
    
    def send_tab(self):
        self.terminal.send("\t")
    
    def send_ctrl_c(self):
        self.terminal.sendcontrol("c")
    
    def _read_output(self):
        try:
            while True:
                data = self.terminal.read_nonblocking(size=1024, timeout=0.1)
                self.stream.feed(data.decode('utf-8'))
        except pexpect.exceptions.TIMEOUT:
            pass
    
    def get_output(self):
        self._read_output()
        return "\n".join(self.screen.display)
