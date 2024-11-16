"""This module contains functions to parse the --help output of a program."""

import re
from collections import namedtuple

# Characters that should not be considered option chars
OPTION_BREAK_CHARS = [' ', '\t', '\n', ',', '|', '=', '[']

# Characters that delimit options
OPTION_DELIMITER_CHARS = [',', '|']

Unparsed = namedtuple('Unparsed', ['text'])
OptionWithMetavar = namedtuple('OptionWithMetavar', ['option', 'metavar', 'optional'])
OptionsWithDescription = namedtuple('OptionsWithDescription', ['options', 'description'])

class CharStream:
    """A utility class for sequentially reading characters from a string."""

    def __init__(self, string, pos = 0):
        self.string = string
        self.len = len(string)
        self.pos = pos

    def peek(self, relative_pos = 0):
        """
        Returns the character at the current position plus an optional relative offset 
        without advancing the stream. Returns None if the position is out of bounds.
        """
        try:
            return self.string[self.pos + relative_pos]
        except IndexError:
            return None

    def peek_str(self, length):
        """
        Returns a substring of the specified length starting from the current position 
        without advancing the stream.
        """
        return self.string[self.pos:self.pos + length]

    def get(self):
        """Returns the current character and advances the position by one."""
        c = self.string[self.pos]
        self.pos += 1
        return c

    def is_space(self):
        """Checks if the current character is a space or a tab."""
        return self.peek() in (' ', '\t')

    def is_end(self):
        """Checks if the current position has reached the end of the string."""
        return self.pos >= self.len

    def copy(self):
        """Creates and returns a new CharStream object at the current position."""
        return CharStream(self.string, self.pos)

    def __repr__(self):
        line = ''
        i = self.pos
        while i < self.len:
            if self.string[i] == '\n':
                break
            line += self.string[i]
            i += 1
        return f"CharStream({line!r})"

def eat_line(stream):
    '''Read the remainling line and return it (including the newline character).'''
    content = ''
    while not stream.is_end():
        char = stream.get()
        content += char
        if char == '\n':
            break
    return content

def eat_space(stream):
    '''Read spaces and tabs and return it.'''
    content = ''
    while stream.is_space():
        content += stream.get()
    return content

def parse_option_string(stream):
    '''
    Read an option string and return it.

    All chars except OPTION_BREAK_CHARS are considered valid option chars.

    Example option strings: --help, -h

    If the resulting option string is '-' or '--', it is not considered an option.
    '''
    option = ''
    p = stream.copy()

    eat_space(p)

    if p.peek() != '-':
        return None

    while not p.is_end() and p.peek() not in OPTION_BREAK_CHARS:
        option += p.get()

    if option in ('-', '--'):
        return None

    stream.pos = p.pos
    return option

def parse_bracket(stream):
    '''
    Read and return a bracketed expression.

    Bracketed expressions are:
        <foo bar>
        [foo bar]
        (foo bar)
        {foo bar}
    '''
    content = stream.peek()
    try:
        closing = {'<':'>', '[':']', '(':')', '{':'}'}[content]
    except KeyError:
        return None

    stream.get()
    while not stream.is_end():
        char = stream.get()
        content += char
        if char == closing:
            break

    return content

def parse_quoted_string(stream):
    '''
    Read and return a string.

    Strings are:
        'foo bar'
        "foo bar"

    Since it is unlikely that we encounter escape sequences in a description string
    of an option, we don't process any escape sequences.
    '''
    quote = stream.peek()
    if quote not in ('"', "'"):
        return None

    stream.get()
    content = quote
    while not stream.is_end():
        char = stream.get()
        content += char
        if char == quote:
            break

    return content

def parse_metavar(stream):
    '''
    Read and return a metavar.

    Everything until a tab, space or newline is considered a metavar.

    Special cases:
      - Bracketed expressions (e.g., '<foo bar>') and quoted strings (e.g., '"foo bar"') 
        are handled, and the spaces within them are preserved.
      - The function supports metavars enclosed by `<`, `[`, `(`, `{`, as well as 
        single (`'`) and double (`"`) quotes.

    Metavars are:
        foo_bar
        'foo bar'
        "foo bar"
        <foo bar>
    '''
    metavar = ''

    while not stream.is_end() and not stream.peek() in (' ', '\t', '\n'):
        if stream.peek() in ('<', '[', '(', '{'):
            metavar += parse_bracket(stream)
        elif stream.peek() in ('"', "'"):
            metavar += parse_quoted_string(stream)
        elif stream.peek() in OPTION_DELIMITER_CHARS:
            break
        else:
            metavar += stream.get()

    return metavar

def parse_trailing_description_line(stream):
    '''
    Reads and returns a trailing description line.

    A line is considered a trailing description line if it meets the following criteria:
      - It starts with whitespace (indicating continuation from a previous line).
      - It does not begin with a hyphen ('-'), which would indicate the start of a new option.
    '''
    p = stream.copy()

    if not p.is_space():
        return None

    space = eat_space(p)

    if p.peek() == '-' and len(space) < 10:
        return None

    content = eat_line(p)
    stream.pos = p.pos
    return content

def parse_description(stream):
    '''Reads and returns the description of an option.'''
    eat_space(stream)
    content = eat_line(stream)
    while True:
        line = parse_trailing_description_line(stream)
        if line:
            content += line
        else:
            break

    return content

def parse_option_with_metavar(stream):
    '''
    Read and return an option with its metavar (if any).

    Valid inputs are:
      --option=METAVAR
      --option[=METAVAR] (in this case, 'optional' is set to True)
      --option METAVAR

    Invalid inputs are:
      --option  METAVAR (notice two spaces)
    '''
    opt = parse_option_string(stream)
    metavar = None
    optional = False

    if opt:
        if stream.peek_str(2) == '[=':
            optional = True
            metavar = parse_metavar(stream)

        elif stream.peek() == '=':
            stream.get()
            metavar = parse_metavar(stream)

        # Two spaces after --option means the description follows
        elif stream.peek_str(2).isspace():
            return OptionWithMetavar(opt, metavar, optional)

        # An option delimiter cannot be a metavar
        elif parse_option_delimiter(stream.copy()):
            return OptionWithMetavar(opt, metavar, optional)

        elif not stream.is_end() and stream.is_space():
            stream.get()
            return OptionWithMetavar(opt, parse_metavar(stream), optional)

        return OptionWithMetavar(opt, metavar, optional)
    else:
        return None

def parse_option_delimiter(stream):
    '''Parse an option delimiter and return True if it was found, False otherwise.'''
    p = stream.copy()
    eat_space(p)
    if p.get() in (',', '|'):
        stream.pos = p.pos
        return True
    return False

def parse_options_with_description(stream):
    options = []
    description = None

    while not stream.is_end():
        option = parse_option_with_metavar(stream)
        if option:
            options.append(option)
        else:
            break

        if not parse_option_delimiter(stream):
            break

    if not options:
        return None

    #if s.peek() == '\n' or s.peek_str(2) in ('  ', ' \n'):
    if stream.peek() in (' ', '\t', '\n'):
        description = parse_description(stream)

    return OptionsWithDescription(options, description)

def parse(stream):
    """Parses the stream and returns a list of options with descriptions or unparsed lines."""
    r = []

    while not stream.is_end():
        options = parse_options_with_description(stream)
        if options:
            r.append(options)
        else:
            line = eat_line(stream)
            r.append(Unparsed(line))

    return r

def get_program_name_from_help(string):
    """Extracts the program name from the help string."""
    m = re.match('usage:[\n\t ]+([^\n\t ]+)', string, re.I)
    if m:
        return m[1]
    else:
        return string.split()[0]
