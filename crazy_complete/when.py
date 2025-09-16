'''Functions for parsing the `when` attribute.'''

import shlex

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

def parse_when(s):
    '''Parse `when` string and return an object.'''

    split = shlex.split(s)

    if not split:
        raise CrazyError("parse_when: Empty arguments")

    cmd = split[0]
    del split[0]

    if cmd == 'option_is':
        return OptionIs(split)

    if cmd == 'has_option':
        return HasOption(split)

    raise CrazyError("Invalid command: %r" % cmd)
