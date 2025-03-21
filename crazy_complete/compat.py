'''Code for maintaining backward compatibility with previous versions of crazy-complete.'''

from . import utils

# Wrong types in configuration structures are silently ignored, because
# they are handled elsewhere

def fix_option_dictionary(dictionary):
    if not isinstance(dictionary, dict):
        return

    if 'group' in dictionary:
        if 'groups' in dictionary:
            utils.warn('Both `group` and `groups` found. `group` is deprecated. Removing `group` in favour of `groups`')
            dictionary.pop('group')
        else:
            utils.warn('`group` is deprecated. Please use `groups` instead')
            dictionary['groups'] = [dictionary.pop('group')]

    if 'multiple_option' in dictionary:
        if 'repeatable' in dictionary:
            utils.warn('Both `multiple_option` and `repeatable` found. `multiple_option` is deprecated. Removing `multiple_option` in favour of `repeatable`')
            dictionary.pop('multiple_option')
        else:
            utils.warn('`multiple_option` is deprecated. Please use `repeatable` instead')
            dictionary['repeatable'] = dictionary.pop('multiple_option')

def fix_commandline_dictionary(dictionary):
    if not isinstance(dictionary, dict):
        return

    options = dictionary.get('options', [])

    if isinstance(options, list):
        for option in options:
            fix_option_dictionary(option)

def fix_commandline_dictionaries(dictionaries):
    if not isinstance(dictionaries, list):
        return

    for commandline_dictionary in dictionaries:
        fix_commandline_dictionary(commandline_dictionary)
