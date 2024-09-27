from collections import namedtuple

# Characters that should not be considered option chars
OPTION_BREAK_CHARS = [' ', '\t', '\n', ',', '|', '=', '[']

# Characters that delimit options
OPTION_DELIMITER_CHARS = [',', '|']

Unparsed = namedtuple('Unparsed', ['text'])
OptionWithMetavar = namedtuple('OptionWithMetavar', ['option', 'metavar', 'optional'])
OptionsWithDescription = namedtuple('OptionsWithDescription', ['options', 'description'])

class CharStream:
    def __init__(self, s, pos = 0):
        self.s = s
        self.len = len(s)
        self.pos = pos

    def peek(self, relative_pos = 0):
        try:
            return self.s[self.pos + relative_pos]
        except IndexError:
            return None

    def peek_str(self, length):
        return self.s[self.pos:self.pos + length]

    def get(self):
        c = self.s[self.pos]
        self.pos += 1
        return c

    def is_space(self):
        return self.peek() in (' ', '\t')

    def is_end(self):
        return self.pos >= self.len

    def copy(self):
        return CharStream(self.s, self.pos)

    def __repr__(self):
        line = ''
        i = self.pos
        while i < self.len:
            if self.s[i] == '\n':
                break
            else:
                line += self.s[i]
            i += 1
        return "CharStream(%r)" % line

def eat_line(s):
    '''
    Read the remainling line and return it (including the newline character).
    '''
    content = ''
    while not s.is_end():
        char = s.get()
        content += char
        if char == '\n':
            break
    return content

def eat_space(s):
    '''
    Read spaces and tabs and return it.
    '''
    content = ''
    while s.is_space():
        content += s.get()
    return content

def parse_option_string(s):
    '''
    Read an option string and return it.

    All chars except OPTION_BREAK_CHARS are considered valid option chars.

    Example option strings: --help, -h

    If the resulting option string is '-' or '--', it is not considered an option.
    '''
    option = ''
    p = s.copy()

    eat_space(p)

    if p.peek() != '-':
        return None

    while not p.is_end() and p.peek() not in OPTION_BREAK_CHARS:
        option += p.get()

    if option == '-' or option == '--':
        return None

    s.pos = p.pos
    return option

def parse_bracket(s):
    '''
    Read and return a bracketed expression.

    Bracketed expressions are:
        <foo bar>
        [foo bar]
        (foo bar)
        {foo bar}
    '''
    content = s.peek()
    try:
        closing = {'<':'>', '[':']', '(':')', '{':'}'}[content]
    except KeyError:
        return None

    s.get()
    while not s.is_end():
        char = s.get()
        content += char
        if char == closing:
            break

    return content

def parse_string(s):
    '''
    Read and return a string.

    Strings are:
        'foo bar'
        "foo bar"

    Since it is unlikely that we encounter escape sequences in a description string
    of an option, we don't process any escape sequences.
    '''
    quote = s.peek()
    if quote not in ('"', "'"):
        return None

    s.get()
    content = quote
    while not s.is_end():
        char = s.get()
        content += char
        if char == quote:
            break

    return content

def parse_metavar(s):
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

    while not s.is_end() and not s.peek() in (' ', '\t', '\n'):
        if s.peek() in ('<', '[', '(', '{'):
            metavar += parse_bracket(s)
        elif s.peek() in ('"', "'"):
            metavar += parse_string(s)
        elif s.peek() in OPTION_DELIMITER_CHARS:
            break
        else:
            metavar += s.get()

    return metavar

def parse_trailing_description_line(s):
    '''
    Reads and returns a trailing description line.

    A line is considered a trailing description line if it meets the following criteria:
      - It starts with whitespace (indicating continuation from a previous line).
      - It does not begin with a hyphen ('-'), which would indicate the start of a new option.
    '''
    p = s.copy()

    if not p.is_space():
        return None

    space = eat_space(p)

    if p.peek() == '-' and len(space) < 10:
        return None

    content = eat_line(p)
    s.pos = p.pos
    return content

def parse_description(s):
    '''
    Reads and returns the description of an option.
    '''
    eat_space(s)
    content = eat_line(s)
    while True:
        line = parse_trailing_description_line(s)
        if line:
            content += line
        else:
            break

    return content

def parse_option_with_metavar(s):
    '''
    Read and return an option with its metavar (if any).

    Valid inputs are:
      --option=METAVAR
      --option[=METAVAR] (in this case, 'optional' is set to True)
      --option METAVAR

    Invalid inputs areE:
      --option  METAVAR (notice two spaces)
    '''
    opt = parse_option_string(s)
    metavar = None
    optional = False

    if opt:
        if s.peek_str(2) == '[=':
            optional = True
            metavar = parse_metavar(s)

        elif s.peek() == '=':
            s.get()
            metavar = parse_metavar(s)

        # Two spaces after --option means the descriptoin follows
        elif s.peek_str(2).isspace():
            return OptionWithMetavar(opt, metavar, optional)

        # An option delimiter cannot be a metavar
        elif parse_option_delimiter(s.copy()):
            return OptionWithMetavar(opt, metavar, optional)

        elif not s.is_end() and s.is_space():
            s.get()
            return OptionWithMetavar(opt, parse_metavar(s), optional)

        return OptionWithMetavar(opt, metavar, optional)
    else:
        return None

def parse_option_delimiter(s):
    '''
    Parse an option delimiter and return True if it was found, False otherwise.
    '''
    p = s.copy()
    eat_space(p)
    if p.get() in (',', '|'):
        s.pos = p.pos
        return True
    return False

def parse_options_with_description(s):
    options = []
    description = None

    while not s.is_end():
        option = parse_option_with_metavar(s)
        if option:
            options.append(option)
        else:
            break

        if not parse_option_delimiter(s):
            break

    if not options:
        return None

    #if s.peek() == '\n' or s.peek_str(2) in ('  ', ' \n'):
    if s.peek() in (' ', '\t', '\n'):
        description = parse_description(s)

    return OptionsWithDescription(options, description)

def parse(s):
    r = []

    while not s.is_end():
        options = parse_options_with_description(s)
        if options:
            r.append(options)
        else:
            line = eat_line(s)
            r.append(Unparsed(line))

    return r
