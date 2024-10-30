'''
Code for maintaining backward compatibility with previous versions of crazy-complete
'''

from . import utils

def fix_option_dictionary(dictionary):
    if 'group' in dictionary:
        if 'groups' in dictionary:
            utils.warn('Both `group` and `groups` found. `group` is deprecated. Removing `group` in favour of `groups`')
            dictionary.pop('group')
        else:
            utils.warn('`group` is deprecated. Please use `groups` instead')
            dictionary['groups'] = [dictionary.pop('group')]

def fix_commandline_dictionaries(dictionaries):
    for commandline_dictionary in dictionaries:
        for option in commandline_dictionary.get('options', []):
            fix_option_dictionary(option)
