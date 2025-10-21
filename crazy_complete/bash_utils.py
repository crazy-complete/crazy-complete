'''Bash utility functions.'''

from . import shell


def make_option_variable_name(option, prefix=''):
    '''Make a variable for an option.'''
    long_options = option.get_long_option_strings()
    if long_options:
        return prefix + shell.make_identifier(long_options[0].lstrip('-'))

    old_options = option.get_old_option_strings()
    if old_options:
        return prefix + shell.make_identifier(old_options[0].lstrip('-'))

    short_options = option.get_short_option_strings()
    if short_options:
        return prefix + short_options[0][1]

    raise AssertionError("make_option_variable_name: Should not be reached")


class VariableManager:
    '''Variable manager.'''

    def __init__(self, prefix):
        self.prefix = prefix
        self.variables = set()

    def make_variable(self, option):
        '''Make a variable for an option.'''

        var = make_option_variable_name(option, self.prefix)
        self.variables.add(var)
        return var

    def capture_variable(self, option):
        if option.capture is None:
            option.capture = self.make_variable(option)
        return option.capture

    def get_variables(self):
        '''Get a list of all defined variables.'''

        return list(sorted(self.variables))


class CasePatterns:
    '''Functions for creating case patterns.'''

    @staticmethod
    def for_long_without_arg(option_strings):
        '''Return a case pattern for long options that don't take an argument.'''

        return '|'.join(option_strings)

    @staticmethod
    def for_long_with_arg(option_strings):
        '''Return a case pattern for long options that take an argument.'''

        return '|'.join(f'{o}=*' for o in option_strings)

    @staticmethod
    def for_short(option_strings):
        '''Return a case pattern for short options.'''

        return '|'.join(o[1] for o in option_strings)

    @staticmethod
    def for_old_without_arg(option_strings):
        '''Return a case pattern for old options that don't take an argument.'''

        if len(option_strings) <= 2:
            return '|'.join(option_strings)

        return '-@(%s)' % '|'.join(o.lstrip('-') for o in option_strings)


def make_file_extension_pattern(extensions, fuzzy):
    '''Make a case-insensitive glob pattern matching `extensions`.

    Takes a list of extensions (e.g. ['txt', 'jpg']) and returns a Bash-style
    pattern that matches all of them, ignoring case.

    Example output:
        '@([tT][xX][tT]|[jJ][pP][gG])'
    '''

    patterns = []

    for extension in extensions:
        pattern = ''
        for c in extension:
            if c.isalpha():
                pattern += '[%s%s]' % (c.lower(), c.upper())
            else:
                pattern += c

        patterns.append(pattern)

    if not fuzzy:
        return '@(%s)' % '|'.join(patterns)
    
    return '@(%s)*' % '|'.join(patterns)
