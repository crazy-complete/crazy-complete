#!/usr/bin/python3

import shlex

class OptionIs:
    def __init__(self, args):
        self.options = []
        self.values = []
        has_end_of_options=False

        for arg in args:
            if arg == '--':
                has_end_of_options=True
            elif has_end_of_options is False:
                self.options.append(arg)
            elif has_end_of_options is True:
                self.values.append(arg)

        if not self.options:
            raise Exception('OptionIs: Empty options')

        if not self.values:
            raise Exception('OptionIs: Empty values')

class HasOption:
    def __init__(self, args):
        self.options = args

        if not self.options:
            raise Exception('HasOption: Empty options')

def parse_when(s):
    splitted = shlex.split(s)

    if not len(splitted):
        raise Exception("parse_when: Empty arguments")

    cmd = splitted[0]
    del splitted[0]

    if cmd == 'option_is':
        return OptionIs(splitted)
    elif cmd == 'has_option':
        return HasOption(splitted)
    else:
        raise Exception("parse_when: Invalid command: %r" % cmd)

