'''Module for parsing shell-like commands with logical operators.'''

from .string_stream import StringStream


# pylint: disable=too-few-public-methods


class Literal:
    '''Represents a literal string.'''

    def __init__(self, string):
        self.string = string

    def __str__(self):
        return self.string

    def __repr__(self):
        return f'Literal({self.string!r})'


class Command:
    '''Represents a command.'''

    def __init__(self):
        self.args = []

    def __repr__(self):
        return f'Command({self.args!r})'


class Lexer(StringStream):
    '''Lexer class.'''

    def parse(self):
        '''Split string into tokens (e.g. logical operators) and literals.'''

        tokens = []
        while True:
            token = self._parse_token()
            if token is not None:
                tokens.append(token)
            else:
                return tokens

    def _parse_token(self):
        c = self.peek()

        if c is None:
            return None

        if c in ('!', '(', ')'):
            self.advance(1)
            return c

        if c.isspace():
            self.advance(1)
            return self._parse_token()

        if c == '&':
            if not self.peek(1) == '&':
                raise ValueError('Single `&` found')
            self.advance(2)
            return '&&'

        if c == '|':
            if not self.peek(1) == '|':
                raise ValueError('Single `|` found')
            self.advance(2)
            return '||'

        return self._parse_literal()

    def _parse_literal(self):
        literal = ''

        while True:
            c = self.peek()

            if c is None:
                return Literal(literal)
            if c == '"':
                literal += self.parse_shell_double_quote(in_quotes=False)
            elif c == "'":
                literal += self.parse_shell_single_quote(in_quotes=False)
            elif c.isspace() or c in ('&', '|', '!', '(', ')'):
                return Literal(literal)
            else:
                self.advance(1)
                literal += c


def make_commands(tokens):
    '''Parse tokens.

    Input:
        [Literal("foo"), Literal("bar"), '&&' Literal("baz")]

    Output:
        [Command(["foo", "bar"]), '&&', Command(["baz"])]
    '''

    new_tokens = []
    current = Command()

    for token in tokens:
        if token in ('&&', '||', '!', '(', ')'):
            if current.args:
                new_tokens.append(current)
                current = Command()
            new_tokens.append(token)
        else:
            current.args.append(str(token))

    if current.args:
        new_tokens.append(current)

    return new_tokens


def check_syntax(tokens):
    '''Checks tokens for syntax errors.'''

    last = None
    parentheses = 0

    for token in tokens:
        if token == '(':
            parentheses += 1
            if last not in (None, '&&', '||', '!', '('):
                raise ValueError("Unexpected `(`")

        elif token == ')':
            parentheses -= 1
            if parentheses < 0 or last in (None, '(', '&&', '||', '!'):
                raise ValueError("Unexpected `)`")

        elif token in ('&&', '||'):
            if last in (None, '(', '&&', '||', '!'):
                raise ValueError(f"Unexpected `{token}`")

        elif token == '!':
            if last not in (None, '(', '&&', '||', '!'):
                raise ValueError("Unexpected `!`")

        last = token

    if parentheses > 0:
        raise ValueError("Unclosed `(`")

    if last is None:
        raise ValueError("No command found")


def parse(string):
    '''Parse a string and turn it into And/Or/Not/Command objects.'''

    lex_tokens = Lexer(string).parse()
    tokens = make_commands(lex_tokens)
    check_syntax(tokens)
    return tokens
