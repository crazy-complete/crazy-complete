'''Module containing code for parsing strings as a stream.'''

class StringStream:
    '''String stream class for reading a string.'''

    def __init__(self, string):
        self.s = string
        self.i = 0

    def peek(self, seek=0):
        '''Return character at current position + seek without advancing.'''

        try:
            return self.s[self.i + seek]
        except IndexError:
            return None

    def peek_str(self, length=1):
        '''Return substring of given length from current position.'''

        return self.s[self.i:length]

    def get(self):
        '''Return current character and advance position by one.'''

        c = self.s[self.i]
        self.i += 1
        return c

    def advance(self, length):
        '''Advance the stream by a given length.'''

        self.i += length

    def parse_shell_single_quote(self, in_quotes=False):
        '''Parse a single-quoted shell string.'''

        if not in_quotes:
            assert self.get() == "'"

        string = ''

        while True:
            try:
                c = self.get()
            except IndexError as e:
                raise ValueError("Unclosed single quote") from e

            if c == "'":
                return string

            string += c

    def parse_shell_double_quote(self, in_quotes=False):
        '''Parse a double-quoted shell string.'''

        if not in_quotes:
            assert self.get() == '"'

        string = ''

        while True:
            try:
                c = self.get()
            except IndexError as e:
                raise ValueError("Unclosed double quote") from e

            if c == '\\':
                try:
                    string += self.get()
                except IndexError:
                    raise ValueError("Missing character after backslash") from e

            elif c == '"':
                return string

            else:
                string += c
