'''Fish utility functions.'''

from .errors import InternalError
from . import shell

class FishString:
    '''
    A utility class for handling command-line strings that may or may not require escaping.

    When building command-line commands, it's important to ensure that strings are properly
    escaped to prevent shell injection vulnerabilities or syntax errors. However, in some
    cases, the string may already be escaped, and applying escaping again would result in
    incorrect behavior. The `FishString` class provides an abstraction to manage both
    escaped and unescaped strings.

    Attributes:
        s (str):
            The string that represents the command or command argument.
        raw (bool):
            A flag that indicates whether the string is already escaped. If `True`,
            the string is assumed to be already escaped and will not be escaped again.

    Args:
        s (str):
            The string to be used in the command.
        raw (bool, optional):
            If `True`, the string will be treated as already escaped. Defaults to `False`.

    Methods:
        escape():
            Returns the escaped version of the string, unless the string is already escaped (`raw=True`).
        __str__():
            Returns the raw string `s` for direct use or display.
    '''

    def __init__(self, s, raw=False):
        '''
        Initializes a FishString instance.

        Args:
            s (str): The string to be used for command-line purposes.
            raw (bool, optional): If True, indicates that the string `s` is already escaped
                                  and should not be escaped again. Defaults to False.
        '''
        assert isinstance(s, str)
        self.s = s
        self.raw = raw

    def escape(self):
        '''
        Escapes the string unless it's marked as already escaped.

        If the `raw` attribute is set to `True`, the method returns the string without any changes.
        Otherwise, it applies shell escaping to ensure the string is safe to use in a command-line context.

        Returns:
            str: The escaped string, or the raw string if it's already escaped.
        '''
        if self.raw:
            return self.s
        return shell.escape(self.s)

    def __str__(self):
        return self.s

    def __repr__(self):
        return repr(self.s)

def make_fish_string(s, raw):
    if s is not None:
        return FishString(s, raw)
    else:
        return None

class FishCompleteCommand:
    '''
    Class for creating FISH's `complete` command.
    '''
    def __init__(self):
        self.command       = None
        self.description   = None
        self.condition     = None
        self.arguments     = None
        self.short_options = []
        self.long_options  = []
        self.old_options   = []
        self.flags         = set()

    def set_command(self, command, raw=False):
        self.command = make_fish_string(command, raw)

    def set_description(self, description, raw=False):
        self.description = make_fish_string(description, raw)

    def add_short_options(self, opts, raw=False):
        self.short_options.extend(make_fish_string(o.lstrip('-'), raw) for o in opts)

    def add_long_options(self, opts, raw=False):
        self.long_options.extend(make_fish_string(o.lstrip('-'), raw) for o in opts)

    def add_old_options(self, opts, raw=False):
        self.old_options.extend(make_fish_string(o.lstrip('-'), raw) for o in opts)

    def set_condition(self, condition, raw=False):
        self.condition = make_fish_string(condition, raw)

    def set_arguments(self, arguments, raw=False):
        self.arguments = make_fish_string(arguments, raw)

    def add_flag(self, flag):
        self.flags.add(flag)

    def parse_args(self, args):
        while len(args):
            arg = args.pop(0)

            if arg == '-f':
                self.add_flag('f')
            elif arg == '-F':
                self.add_flag('F')
            elif arg == '-a':
                try:
                    self.set_arguments(args.pop(0))
                except IndexError as e:
                    raise InternalError('Option `-a` requires an argument') from e
            else:
                raise InternalError(f'Unknown option for `complete`: {arg}')

    def get(self):
        r = ['complete']

        if self.command is not None:
            r.extend(['-c', self.command])

        if self.condition is not None:
            r.extend(['-n', self.condition])

        for o in self.short_options:
            r.extend(['-s', o])

        for o in self.long_options:
            r.extend(['-l', o])

        for o in self.old_options:
            r.extend(['-o', o])

        if self.description is not None:
            r.extend(['-d', self.description])

        # -r -f is the same as -x
        if 'r' in self.flags and 'f' in self.flags:
            self.flags.add('x')

        # -x implies -r -f
        if 'x' in self.flags:
            self.flags.discard('r')
            self.flags.discard('f')

        if self.flags:
            r.append('-%s' % ''.join(sorted(self.flags)))

        if self.arguments is not None:
            r.extend(['-a', self.arguments])

        return ' '.join(v if isinstance(v, str) else v.escape() for v in r)

class VariableManager:
    def __init__(self, variable_name):
        self.variable_name = variable_name
        self.value_to_variable  = {}
        self.counter = 0

    def add(self, value):
        if value in self.value_to_variable:
            return '$%s' % self.value_to_variable[value]

        var = '%s%03d' % (self.variable_name, self.counter)
        self.value_to_variable[value] = var
        self.counter += 1
        return '$%s' % var

    def get_lines(self):
        r = []
        for value, variable in self.value_to_variable.items():
            r.append('set -l %s %s' % (variable, value))
        return r
