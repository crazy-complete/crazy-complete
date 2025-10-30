'''This module contains functions for transforming bash glob patterns.'''


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
        self.tokens.append(token)


EXTGLOB_TOKENS = ('@(', '*(', '+(', '?(', '!(', '+(')
EXTGLOB_TOKENS_PRE = ('@', '*', '+', '?', '!', '+')


class GlobLexer:
    '''Class for splitting a pattern into tokens.'''

    def __init__(self, pattern):
        self.pattern = pattern
        self.i = 0
        self.tokens = []

    def peek(self, seek=0):
        try:
            return self.pattern[self.i + seek]
        except IndexError:
            return None

    def get(self):
        c = self.pattern[self.i]
        self.i += 1
        return c

    def parse(self):
        tokens = []

        while True:
            try:
                tokens.append(self.parse_token())
            except IndexError:
                return tokens

    def parse_token(self):
        c = self.get()

        if c in EXTGLOB_TOKENS_PRE and self.peek() == '(':
            return f'{c}{self.get()}'

        if c in ('[', ']', ')', '?', '!', '*', '|'):
            return c

        literal = ''

        if c == '"':
            while True:
                try:
                    c = self.get()
                except IndexError:
                    raise ValueError("Unclosed sinqle quote") from None

                if c == '\\':
                    try:
                        literal += self.get()
                    except IndexError:
                        raise ValueError("Missing character after backslash") from None

                if c == '"':
                    return Literal(literal)

                literal += c

        if c == "'":
            while True:
                try:
                    c = self.get()
                except IndexError:
                    raise ValueError("Unclosed double quote") from None

                if c == "'":
                    return Literal(literal)

                literal += c

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
        token = self.tokens[self.i]
        self.i += 1
        return token

    def peek(self):
        try:
            return self.tokens[self.i]
        except IndexError:
            return None

    def have(self):
        return self.i < len(self.tokens)

    def parse_char_class(self):
        chars = ''
        negated = False

        token = self.get()
        if token == '!':
            negated = True
        elif token == ']':
            raise Exception('Empty character class')
        else:
            chars += str(token)

        while True:
            try:
                token = self.get()
            except IndexError:
                raise ValueError('Unclosed character class')

            if token == ']':
                return CharClass(chars, negated)
            else:
                chars += str(token)

    def parse_ext_glob(self, token):
        type_ = token[0]
        alternatives = [PatternList()]

        while True:
            token = self.peek()
            if token == ')':
                self.get()
                return ExtGlob(type_, alternatives)
            elif token == '|':
                self.get()
                alternatives.append(PatternList())
            elif token is None:
                raise ValueError('Unclosed extglob')
            else:
                alternatives[-1].append(self.parse_token())

    def parse(self):
        root = PatternList()
        while self.have():
            root.append(self.parse_token())
        return root

    def parse_token(self):
        token = self.get()

        if token == '[':
            return self.parse_char_class()

        if token == '*':
            return Star()

        if token == '?':
            return Question()

        if token in EXTGLOB_TOKENS:
            return self.parse_ext_glob(token)

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


if __name__ == '__main__':
    def test(num, bash_pattern, expected_regex, expected_zsh_glob):
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
            raise Exception('Test failed')

        if zsh_glob_result != expected_zsh_glob:
            print('Test %d (zsh glob):' % num)
            print('Having:   %s' % zsh_glob_result)
            print('Expected: %s' % expected_zsh_glob)
            raise Exception('Test failed')

    # Literals
    test(0,  r'a',                   r'a',                  r'a')
    test(1,  r'abc',                 r'abc',                r'abc')
    test(3,  r'"abc"',               r'abc',                r'abc')
    test(4,  r"'abc'",               r'abc',                r'abc')
    test(5,  r"'a'b'c'",             r'abc',                r'abc')
    test(6,  r'.',                   r'\.',                 r'.')
    test(7,  r'+',                   r'\+',                 r'+')
    test(8,  r'@',                   r'@',                  r'@')
    test(9,  r'"["',                 r'\[',                 r"'['")
    test(10, r"'['",                 r'\[',                 r"'['")
    test(11, r'"]"',                 r'\]',                 r"']'")
    test(12, r"']'",                 r'\]',                 r"']'")
    test(13, r"'*'",                 r'\*',                 r"'*'")
    test(14, r"'?'",                 r'\?',                 r"'?'")

    # Simple globbing
    test(15, r'*',                   r'.*',                 r'*')
    test(16, r'?',                   r'.',                  r'?')
    test(17, r'???',                 r'...',                r'???')

    # Literals + simple globbing
    test(18, r'*abc*',               r'.*abc.*',            r'*abc*')
    test(19, r'*.*',                 r'.*\..*',             r'*.*')
    test(20, r'*+*',                 r'.*\+.*',             r'*+*')

    # Character classes
    test(21, r'[abc]',               r'[abc]',              r'[abc]')
    test(22, r'[.]',                 r'[\.]',               r'[.]')
    test(23, r'[+]',                 r'[+]',                r'[+]')
    test(24, r'[}]',                 r'[}]',                r'[}]')
    test(25, r'[{]',                 r'[{]',                r'[{]')
    test(26, r'[*]',                 r'[*]',                r'[*]')
    test(27, r'[(]',                 r'[(]',                r'[(]')
    test(28, r'[)]',                 r'[)]',                r'[)]')
    test(29, r'["["]',               r'[\[]',               r"['[']")
    test(30, r'["]"]',               r'[\]]',               r"[']']")

    # Extglob @
    test(31, r'@(foo)',              r'(foo)',              r'(foo)')
    test(32, r'@(foo|bar)',          r'(foo|bar)',          r'(foo|bar)')
    test(33, r'@(|foo)',             r'(|foo)',             r'(|foo)')

    # Extglob *
    test(34, r'*(foo|bar)',          r'(foo|bar)*',         ValueError)
    test(35, r'*(foo)',              r'(foo)*',             ValueError)
    test(36, r'*(|foo)',             r'(|foo)*',            ValueError)

    # Extglob +
    test(37, r'+(foo|bar)',          r'(foo|bar)+',         ValueError)
    test(38, r'+(foo)',              r'(foo)+',             ValueError)
    test(39, r'+(|foo)',             r'(|foo)+',            ValueError)

    # Extglob ?
    test(40, r'?(foo|bar)',          r'(foo|bar)?',         ValueError)
    test(41, r'?(foo)',              r'(foo)?',             ValueError)
    test(42, r'?(|foo)',             r'(|foo)?',            ValueError)

    # Extglob !
    test(43, r'!(foo|bar)',          ValueError,            ValueError)

    # Nested
    test(44, r'@([abc]|foo)',        r'([abc]|foo)',        r'([abc]|foo)')
    test(45, r'@(@(foo|bar))',       r'((foo|bar))',        r'((foo|bar))')
    test(46, r'@(@("foo"|bar))',     r'((foo|bar))',        r'((foo|bar))')
    test(47, r'@(?|bar)',            r'(.|bar)',            r'(?|bar)')
    test(48, r'@(*baz|bar)',         r'(.*baz|bar)',        r'(*baz|bar)')

    # Syntax errors
    test(70, r'@(foo',               ValueError,            ValueError)
    test(71, r'[abc',                ValueError,            ValueError)
    test(71, r'"abc',                ValueError,            ValueError)
    test(71, r"'abc",                ValueError,            ValueError)
