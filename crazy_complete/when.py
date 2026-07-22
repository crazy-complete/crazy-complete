# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2025-2026 Benjamin Abendroth <braph93@gmx.de>

'''Functions for parsing the `when` attribute.'''

from . import shell_parser
from . import messages as m
from .errors import CrazyError
from .str_utils import is_valid_option_string


# pylint: disable=too-few-public-methods


class OptionIs:
    '''Class for holding `option_is`.'''

    def __init__(self, args):
        self.options = []
        self.values = []
        self.ignore_case = False
        has_end_of_options = False

        if args and args[0].lower() == 'nocase':
            self.ignore_case = True
            args.pop(0)

        for arg in args:
            if arg == '--':
                has_end_of_options = True
            elif not has_end_of_options:
                self.options.append(arg)
            elif has_end_of_options:
                self.values.append(arg)

        for option in self.options:
            if not is_valid_option_string(option):
                msg = 'option_is: %s: %s' % (m.invalid_value(), option)
                raise CrazyError(msg)

        if not self.options:
            msg = 'option_is: %s: %s' % (m.missing_arg(), 'options')
            raise CrazyError(msg)

        if not self.values:
            msg = 'option_is: %s: %s' % (m.missing_arg(), 'values')
            raise CrazyError(msg)


class HasOption:
    '''Class for holding `has_option`.'''

    def __init__(self, args):
        self.options = args

        if not self.options:
            msg = 'has_option: %s: %s' % (m.missing_arg(), 'options')
            raise CrazyError(msg)


class PositionalCount:
    '''Class for holding `positional_count`.'''

    OPERATORS = ('==', '!=', '<=', '>=', '<', '>')

    def __init__(self, args):
        if len(args) > 2:
            msg = 'positional_count: %s' % (m.too_many_arguments())
            raise CrazyError(msg)

        try:
            self.operator = args[0]
        except IndexError:
            msg = 'positional_count: %s: %s' % (m.missing_arg(), 'operator')
            raise CrazyError(msg)

        if self.operator not in self.OPERATORS:
            msg = 'positional_count: operator: %s' % (
                m.invalid_value_expected_values(', '.join(self.OPERATORS)))
            raise CrazyError(msg)

        try:
            self.number = int(args[1])
        except ValueError:
            msg = 'positional_count: number: %s' % (m.invalid_value())
            raise CrazyError(msg)
        except IndexError:
            msg = 'positional_count: %s: %s' % (m.missing_arg(), 'number')
            raise CrazyError(msg)


class PositionalContains:
    '''Class for holding `positional_contains`.'''

    def __init__(self, args):
        try:
            self.number = int(args.pop(0))
        except ValueError:
            msg = 'positional_contains: number: %s' % (m.invalid_value())
            raise CrazyError(msg)
        except IndexError:
            msg = 'positional_contains: %s: %s' % (m.missing_arg(), 'number')
            raise CrazyError(msg)

        if len(args) == 0:
            msg = 'positional_contains: %s: %s' % (m.missing_arg(), 'values')
            raise CrazyError(msg)

        self.values = args


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
            elif cmd == 'positional_count':
                r.append(PositionalCount(args))
            elif cmd == 'positional_contains':
                r.append(PositionalContains(args))
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

    try:
        tokens = shell_parser.parse(s)
    except ValueError as e:
        raise CrazyError(str(e))

    return replace_commands(tokens)
