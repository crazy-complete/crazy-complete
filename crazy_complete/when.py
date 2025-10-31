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


def replace_commands(obj):
    '''Replaced `shell_parser.Command` objects by condition objects.'''

    if isinstance(obj, shell_parser.And):
        obj.left  = replace_commands(obj.left)
        obj.right = replace_commands(obj.right)
        return obj

    if isinstance(obj, shell_parser.Or):
        obj.left  = replace_commands(obj.left)
        obj.right = replace_commands(obj.right)
        return obj

    if isinstance(obj, shell_parser.Not):
        obj.expr = replace_commands(obj.expr)
        return obj

    if isinstance(obj, shell_parser.Command):
        cmd, *args = obj.args

        if cmd == 'option_is':
            return OptionIs(args)

        if cmd == 'has_option':
            return HasOption(args)

        raise CrazyError("Invalid command: %r" % cmd)

    raise AssertionError("Not reached")


def parse_when(s):
    '''Parse `when` string and return an object.'''

    obj = shell_parser.parse(s)
    return replace_commands(obj)
