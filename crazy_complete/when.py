'''Functions for parsing the `when` attribute.'''

from . import shell_parser
from .errors import CrazyError


# pylint: disable=too-few-public-methods


class OptionIs:
    '''Class for holding `option_is`.'''

    def __init__(self, args):
        self.options = []
        self.values = []
        has_end_of_options = False

        for arg in args:
            if arg == '--':
                has_end_of_options = True
            elif not has_end_of_options:
                self.options.append(arg)
            elif has_end_of_options:
                self.values.append(arg)

        if not self.options:
            raise CrazyError('OptionIs: Empty options')

        if not self.values:
            raise CrazyError('OptionIs: Empty values')


class HasOption:
    '''Class for holding `has_option`.'''

    def __init__(self, args):
        self.options = args

        if not self.options:
            raise CrazyError('HasOption: Empty options')


def replace_commands(tokens):
    '''Replaced `shell_parser.Command` objects by condition objects.'''

    r = []

    for token in tokens:
        if isinstance(token, shell_parser.Command):
            cmd, *args = token.args

            if cmd == 'option_is':
                r.append(OptionIs(args))
            elif cmd == 'has_option':
                r.append(HasOption(args))
            else:
                raise CrazyError(f"Invalid command: {cmd!r}")
        else:
            r.append(token)

    return r


def needs_braces(tokens):
    '''Check if we need braces around our tokens.

    We don't need braces if:
        - We only have one token (single command)
        - We only have two tokens (negated single command)
        - We don't have an OR inside the tokens
    '''
    return len(tokens) > 2 and '||' in tokens


def parse_when(s):
    '''Parse `when` string and return an object.'''

    tokens = shell_parser.parse(s)
    return replace_commands(tokens)
