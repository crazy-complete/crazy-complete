'''This module contains functions for transforming bash glob patterns.'''


from .string_stream import StringStream


class PatternBase:
    '''Base class for glob patterns.'''

    def to_regex(self):
        '''Make a regular expression.'''
        raise NotImplementedError

    def to_zsh_glob(self):
        '''Make a zsh glob.'''
        raise NotImplementedError


class Literal(PatternBase):
    '''Holds a literal string.'''

    REGEX_ESCAPE_CHARS = '.?*+|{}[]()'

    def __init__(self, string):
        self.string = string

    def __str__(self):
        return self.string

    def __repr__(self):
        return self.string

    def to_regex(self):
        string = self.string

        for c in Literal.REGEX_ESCAPE_CHARS:
            string = string.replace(c, f'\\{c}')

        return string

    def to_zsh_glob(self):
        string = ''

        for c in self.string:
            if c in ('[', ']', '?', '*', '"', ' ', '\\'):
                string += f"'{c}'"
            elif c == "'":
                string += f'"{c}"'
            else:
                string += c

        return string


class Star(PatternBase):
    '''Represents a star glob (*).'''

    def to_regex(self):
        return '.*'

    def to_zsh_glob(self):
        return '*'


class Question(PatternBase):
    '''Represents a question glob (?).'''

    def to_regex(self):
        return '.'

    def to_zsh_glob(self):
        return '?'


class CharClass(PatternBase):
    '''Represents a character class.'''

    REGEX_ESCAPE_CHARS = r'^\.[]'

    def __init__(self, chars, negated):
        self.chars = chars
        self.negated = negated

    def to_regex(self):
        chars = self.chars

        for c in CharClass.REGEX_ESCAPE_CHARS:
            chars = chars.replace(c, f'\\{c}')

        if self.negated:
            return f'[^{chars}]'

        return f'[{chars}]'

    def to_zsh_glob(self):
        chars = ''

        for c in self.chars:
            if c in ('[', ']', '!'):
                chars += f"'{c}'"
            else:
                chars += c

        if self.negated:
            return f'[!{chars}]'

        return f'[{chars}]'


class ExtGlob(PatternBase):
    '''Holds an extglob: @(), *(), ?(), +(), !().'''

    def __init__(self, type_, alternatives):
        self.type = type_
        self.alternatives = alternatives

    def to_regex(self):
        r = []

        for alternative in self.alternatives:
            r.append(alternative.to_regex())

        p = '(%s)' % '|'.join(r)

        if self.type == '@':
            return p

        if self.type == '*':
            return p + '*'

        if self.type == '+':
            return p + '+'

        if self.type == '?':
            return p + '?'

        if self.type == '!':
            raise ValueError('Negated glob !(...) not supported in regex')

        raise AssertionError("Not reached")

    def to_zsh_glob(self):
        r = []

        for alternative in self.alternatives:
            r.append(alternative.to_zsh_glob())

        p = '(%s)' % '|'.join(r)

        if self.type == '@':
            return p

        if self.type in ('*', '+', '?', '!'):
            raise ValueError(f'Extended glob of form {self.type}(...) not supported in zsh glob')

        raise AssertionError("Not reached")


class PatternList(PatternBase):
    '''Holds a list of patterns.'''

    def __init__(self):
        self.tokens = []

    def to_regex(self):
        return ''.join(t.to_regex() for t in self.tokens)

    def to_zsh_glob(self):
        return ''.join(t.to_zsh_glob() for t in self.tokens)

    def append(self, token):
        '''Add a token.'''
        self.tokens.append(token)


EXTGLOB_TOKENS = ('@(', '*(', '+(', '?(', '!(', '+(')
EXTGLOB_TOKENS_PRE = ('@', '*', '+', '?', '!', '+')


class GlobLexer(StringStream):
    '''Class for splitting a pattern into tokens.'''

    def __init__(self, pattern):
        super().__init__(pattern)
        self.tokens = []

    def parse(self):
        tokens = []

        while True:
            try:
                tokens.append(self._parse_token())
            except IndexError:
                return tokens

    def _parse_token(self):
        c = self.get()

        if c in EXTGLOB_TOKENS_PRE and self.peek() == '(':
            return f'{c}{self.get()}'

        if c in ('[', ']', ')', '?', '!', '*', '|'):
            return c

        if c == '"':
            return Literal(self.parse_shell_double_quote(in_quotes=True))

        if c == "'":
            return Literal(self.parse_shell_single_quote(in_quotes=True))

        literal = c
        while True:
            c = self.peek()
            if c is None:
                break
            if c in EXTGLOB_TOKENS_PRE and self.peek(1) == '(':
                break
            if c in ('*', '?', '[', ']', ')', '|', '"', "'"):
                break
            literal += c
            self.get()

        return Literal(literal)


class GlobParser:
    '''Parses tokens from GlobLexer.'''

    def __init__(self, tokens):
        self.tokens = tokens
        self.i = 0

    def get(self):
        '''Return a token and advance position.'''
        token = self.tokens[self.i]
        self.i += 1
        return token

    def peek(self):
        '''Return current token without advancing the position.'''
        try:
            return self.tokens[self.i]
        except IndexError:
            return None

    def have(self):
        '''Return True if there are any tokens left.'''
        return self.i < len(self.tokens)

    def parse(self):
        root = PatternList()
        while self.have():
            root.append(self._parse_token())
        return root

    def _parse_char_class(self):
        chars = ''
        negated = False

        try:
            token = self.get()
        except IndexError as e:
            raise ValueError('Unclosed character class') from e

        if token == '!':
            negated = True
        elif token == ']':
            raise ValueError('Empty character class')
        else:
            chars += str(token)

        while True:
            try:
                token = self.get()
            except IndexError as e:
                raise ValueError('Unclosed character class') from e

            if token == ']':
                return CharClass(chars, negated)

            chars += str(token)

    def _parse_ext_glob(self, token):
        type_ = token[0]
        alternatives = [PatternList()]

        while True:
            token = self.peek()

            if token == ')':
                self.get()
                return ExtGlob(type_, alternatives)

            if token == '|':
                self.get()
                alternatives.append(PatternList())
            elif token is None:
                raise ValueError('Unclosed extglob')
            else:
                alternatives[-1].append(self._parse_token())

    def _parse_token(self):
        token = self.get()

        if token == '[':
            return self._parse_char_class()

        if token == '*':
            return Star()

        if token == '?':
            return Question()

        if token in EXTGLOB_TOKENS:
            return self._parse_ext_glob(token)

        return token


def bash_glob_to_regex(pattern):
    '''Transform a bash glob to regex.'''

    tokens = GlobLexer(pattern).parse()
    tokens = GlobParser(tokens).parse()
    return tokens.to_regex()


def bash_glob_to_zsh_glob(pattern):
    '''Transform a bash glob to zsh glob.'''

    tokens = GlobLexer(pattern).parse()
    tokens = GlobParser(tokens).parse()
    return tokens.to_zsh_glob()


def test():
    '''Tests.'''

    def do_test(num, bash_pattern, expected_regex, expected_zsh_glob):
        '''Do a test case.'''

        try:
            regex_result = bash_glob_to_regex(bash_pattern)
        except ValueError:
            regex_result = ValueError

        try:
            zsh_glob_result = bash_glob_to_zsh_glob(bash_pattern)
        except ValueError:
            zsh_glob_result = ValueError

        if regex_result != expected_regex:
            print('Test %d (regex):' % num)
            print('Having:   %s' % regex_result)
            print('Expected: %s' % expected_regex)
            raise AssertionError('Test failed')

        if zsh_glob_result != expected_zsh_glob:
            print('Test %d (zsh glob):' % num)
            print('Having:   %s' % zsh_glob_result)
            print('Expected: %s' % expected_zsh_glob)
            raise AssertionError('Test failed')

    tests = [
        # Literals
        (0,  r'a',                   r'a',                  r'a'),
        (1,  r'abc',                 r'abc',                r'abc'),
        (3,  r'"abc"',               r'abc',                r'abc'),
        (4,  r"'abc'",               r'abc',                r'abc'),
        (5,  r"'a'b'c'",             r'abc',                r'abc'),
        (6,  r'.',                   r'\.',                 r'.'),
        (7,  r'+',                   r'\+',                 r'+'),
        (8,  r'@',                   r'@',                  r'@'),
        (9,  r'"["',                 r'\[',                 r"'['"),
        (10, r"'['",                 r'\[',                 r"'['"),
        (11, r'"]"',                 r'\]',                 r"']'"),
        (12, r"']'",                 r'\]',                 r"']'"),
        (13, r"'*'",                 r'\*',                 r"'*'"),
        (14, r"'?'",                 r'\?',                 r"'?'"),

        # Simple globbing
        (15, r'*',                   r'.*',                 r'*'),
        (16, r'?',                   r'.',                  r'?'),
        (17, r'???',                 r'...',                r'???'),

        # Literals + simple globbing
        (18, r'*abc*',               r'.*abc.*',            r'*abc*'),
        (19, r'*.*',                 r'.*\..*',             r'*.*'),
        (20, r'*+*',                 r'.*\+.*',             r'*+*'),

        # Character classes
        (21, r'[abc]',               r'[abc]',              r'[abc]'),
        (22, r'[.]',                 r'[\.]',               r'[.]'),
        (23, r'[+]',                 r'[+]',                r'[+]'),
        (24, r'[}]',                 r'[}]',                r'[}]'),
        (25, r'[{]',                 r'[{]',                r'[{]'),
        (26, r'[*]',                 r'[*]',                r'[*]'),
        (27, r'[(]',                 r'[(]',                r'[(]'),
        (28, r'[)]',                 r'[)]',                r'[)]'),
        (29, r'["["]',               r'[\[]',               r"['[']"),
        (30, r'["]"]',               r'[\]]',               r"[']']"),

        # Extglob @
        (31, r'@(foo)',              r'(foo)',              r'(foo)'),
        (32, r'@(foo|bar)',          r'(foo|bar)',          r'(foo|bar)'),
        (33, r'@(|foo)',             r'(|foo)',             r'(|foo)'),

        # Extglob *
        (34, r'*(foo|bar)',          r'(foo|bar)*',         ValueError),
        (35, r'*(foo)',              r'(foo)*',             ValueError),
        (36, r'*(|foo)',             r'(|foo)*',            ValueError),

        # Extglob +
        (37, r'+(foo|bar)',          r'(foo|bar)+',         ValueError),
        (38, r'+(foo)',              r'(foo)+',             ValueError),
        (39, r'+(|foo)',             r'(|foo)+',            ValueError),

        # Extglob ?
        (40, r'?(foo|bar)',          r'(foo|bar)?',         ValueError),
        (41, r'?(foo)',              r'(foo)?',             ValueError),
        (42, r'?(|foo)',             r'(|foo)?',            ValueError),

        # Extglob !
        (43, r'!(foo|bar)',          ValueError,            ValueError),

        # Nested
        (44, r'@([abc]|foo)',        r'([abc]|foo)',        r'([abc]|foo)'),
        (45, r'@(@(foo|bar))',       r'((foo|bar))',        r'((foo|bar))'),
        (46, r'@(@("foo"|bar))',     r'((foo|bar))',        r'((foo|bar))'),
        (47, r'@(?|bar)',            r'(.|bar)',            r'(?|bar)'),
        (48, r'@(*baz|bar)',         r'(.*baz|bar)',        r'(*baz|bar)'),

        # Syntax errors
        (70, r'@(foo',               ValueError,            ValueError),
        (71, r'[abc',                ValueError,            ValueError),
        (71, r'"abc',                ValueError,            ValueError),
        (71, r"'abc",                ValueError,            ValueError),
    ]

    for case in tests:
        do_test(*case)
