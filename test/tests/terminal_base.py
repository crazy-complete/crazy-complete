import time

def strip_lines(string):
    return '\n'.join(s.rstrip() for s in string.split('\n')).rstrip()

class TerminalBase:
    def get_output_stripped(self):
        return strip_lines(self.get_output())

    def clear_screen(self):
        result = ''
        while result != '>':
            # Cancel potentially running task
            self.send_ctrl("c")
            # Clear current command line, as fish does not do it on ^C
            self.send_ctrl("u")
            self.wait_for_last_line('>', 5, 0.01)
            self.send_line('clear')
            result = self.wait_for_text('>', 5, 0.01)

    def complete(self, commandline, num_tabs=1, wait=5, expected=None, fast=False):
        self.clear_screen()
        self.send(commandline)

        for _ in range(num_tabs):
            self.send_tab()

        if fast:
            return self.wait_for_text(expected, wait, 0.01)
        else:
            time.sleep(wait)
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

    def wait_for_last_line(self, expected, timeout, poll_interval):
        expected = expected.rstrip()

        while timeout > 0.0:
            result = self.get_output_stripped().split('\n')[-1]
            if result == expected:
                return True
            timeout -= poll_interval
            time.sleep(poll_interval)
        return False
