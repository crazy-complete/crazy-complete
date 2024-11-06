import time

def strip_lines(string):
    return '\n'.join(s.rstrip() for s in string.split('\n')).rstrip()

class TerminalBase:
    def get_output_stripped(self):
        return strip_lines(self.get_output())

    def clear_screen(self):
        self.send_ctrl_c()
        self.send_line('clear')

        result = self.wait_for_text('>', 1, 0.01)
        if result != '>':
            # Idk why, but sometime we have to try again
            self.clear_screen()

    def complete(self, commandline, num_tabs=1, expected=None, fast=False):
        self.clear_screen()
        self.send(commandline)

        for i in range(num_tabs):
            self.send_tab()

        if fast:
            return self.wait_for_text(expected, 1, 0.01)
        else:
            time.sleep(1)
            return self.get_output_stripped()

    def wait_for_text(self, expected, timeout, poll_interval):
        expected = strip_lines(expected)

        while timeout > 0.0:
            result = self.get_output_stripped()
            if result == expected:
                return result
            timeout -= poll_interval
            time.sleep(poll_interval)
        return self.get_output_stripped()
