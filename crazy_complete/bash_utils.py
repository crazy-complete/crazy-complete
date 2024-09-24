from . import shell
from . import utils

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

def make_long_options_case_without_arg(options):
    return '|'.join(options)

def make_long_options_case_with_arg(options):
    return '|'.join(f'{o}=*' for o in options)

def make_short_options_case(options):
    return '|'.join(o[1] for o in options)

def get_OptionAbbreviationGenerator(options):
    all_option_strings = []
    for option in options:
        all_option_strings.extend(option.get_long_option_strings())
        all_option_strings.extend(option.get_old_option_strings())

    return utils.OptionAbbreviationGenerator(all_option_strings)
