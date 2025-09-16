'''Bash utility functions.'''

from . import shell

def make_option_variable_name(option, prefix=''):
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
        var = make_option_variable_name(option, self.prefix)
        self.variables.add(var)
        return var

    def get_variables(self):
        return list(sorted(self.variables))

class CasePatterns:
    '''Functions for creating case patterns.'''

    @staticmethod
    def for_long_without_arg(option_strings):
        return '|'.join(option_strings)

    @staticmethod
    def for_long_with_arg(option_strings):
        return '|'.join(f'{o}=*' for o in option_strings)

    @staticmethod
    def for_short(option_strings):
        return '|'.join(o[1] for o in option_strings)
