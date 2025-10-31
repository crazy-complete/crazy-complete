'''Module for parsing shell-like commands with logical operators.'''

from .string_stream import StringStream


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


class And:
    '''And operator.'''

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return f"And({self.left!r}, {self.right!r})"


class Or:
    '''Or operator.'''

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return f"Or({self.left!r}, {self.right!r})"


class Not:
    '''Not operator.'''

    def __init__(self, expr):
        self.expr = expr

    def __repr__(self):
        return f"Not({self.expr!r})"


class Lexer(StringStream):
    def parse(self):
        tokens = []
        while True:
            token = self.parse_token()
            if token is not None:
                tokens.append(token)
            else:
                return tokens

    def parse_token(self):
        c = self.peek()

        if c is None:
            return None

        if c in ('!', '(', ')'):
            self.advance(1)
            return c

        if c.isspace():
            self.advance(1)
            return self.parse_token()

        if c == '&':
            if not self.peek(1) == '&':
                raise ValueError('Single "&" found')
            self.advance(2)
            return '&&'

        if c == '|':
            if not self.peek(1) == '|':
                raise ValueError('Single "|" found')
            self.advance(2)
            return '||'

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
    '''Pre-parse tokens.
    
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


def parse_tokens(tokens):
    '''Parse tokens and return And/Or/Not/Command objects.'''

    tokens = list(tokens)
    pos = 0

    def peek():
        return tokens[pos] if pos < len(tokens) else None

    def consume(expected=None):
        nonlocal pos
        tok = peek()
        if expected is not None and tok != expected:
            raise SyntaxError(f"Expected {expected!r}, but found {tok!r}")
        if tok is None:
            raise SyntaxError("Unexpected end of input")
        pos += 1
        return tok

    # Grammar:
    # expr      := or_expr
    # or_expr   := and_expr { "||" and_expr }
    # and_expr  := not_expr { "&&" not_expr }
    # not_expr  := "!" not_expr | primary
    # primary   := COMMAND_OBJ | "(" expr ")"

    def parse_expr():
        return parse_or()

    def parse_or():
        left = parse_and()
        while peek() == "||":
            consume("||")
            right = parse_and()
            left = Or(left, right)
        return left

    def parse_and():
        left = parse_not()
        while peek() == "&&":
            consume("&&")
            right = parse_not()
            left = And(left, right)
        return left

    def parse_not():
        if peek() == "!":
            consume("!")
            return Not(parse_not())
        return parse_primary()

    def parse_primary():
        tok = peek()
        if tok == "(":
            consume("(")
            expr = parse_expr()
            consume(")")
            return expr

        if tok is None:
            raise SyntaxError("Unexpected end of input")
        if not isinstance(tok, str):
            return consume()
        raise SyntaxError(f"Unexpected token: {tok!r}")

    result = parse_expr()
    if peek() is not None:
        raise SyntaxError(f"Unexpected token after expression: {peek()!r}")
    return result


def parse(string):
    '''Parse a string and turn it into And/Or/Not/Command objects.'''

    lex_tokens = Lexer(string).parse()
    tokens = make_commands(lex_tokens)
    return parse_tokens(tokens)
