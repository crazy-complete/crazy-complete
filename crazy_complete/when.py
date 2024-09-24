import shlex

class OptionIs:
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
            raise Exception('OptionIs: Empty options')

        if not self.values:
            raise Exception('OptionIs: Empty values')

class HasOption:
    def __init__(self, args):
        self.options = args

        if not self.options:
            raise Exception('HasOption: Empty options')

def parse_when(s):
    split = shlex.split(s)

    if not split:
        raise Exception("parse_when: Empty arguments")

    cmd = split[0]
    del split[0]

    if cmd == 'option_is':
        return OptionIs(split)

    if cmd == 'has_option':
        return HasOption(split)

    raise Exception("parse_when: Invalid command: %r" % cmd)
