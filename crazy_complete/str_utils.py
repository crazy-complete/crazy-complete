'''String utility functions.'''

import re

def contains_space(string):
    '''Check if string contains space type characters.'''

    return (' ' in string or '\t' in string or '\n' in string)

def is_empty_or_whitespace(string):
    '''Check if string is empty or whitespace.'''

    return not string.strip()

def indent(string, num_spaces):
    '''Indents each line in a string by a specified number of spaces,
    preserving empty lines.

    Args:
        string (str): The input string to be indented.
        num_spaces (int): The number of spaces to indent each line.

    Returns:
        str: The indented string.
    '''

    assert isinstance(string, str),     f"indent: string: expected str, got {string!r}"
    assert isinstance(num_spaces, int), f"indent: num_spaces: expected int, got {num_spaces!r}"

    lines = string.split('\n')
    indented_lines = [((' ' * num_spaces) + line) if line.strip() else line for line in lines]
    return '\n'.join(indented_lines)

_VALID_OPTION_STRING_RE = re.compile('-[^\\s,]+')

def is_valid_option_string(option_string):
    '''Check if `option_string` is a valid option string.'''

    if not _VALID_OPTION_STRING_RE.fullmatch(option_string):
        return False

    if option_string == '--':
        return False

    return True

_VALID_VARIABLE_RE = re.compile('[a-zA-Z_][a-zA-Z0-9_]*')

def is_valid_variable_name(string):
    '''Check if string is a valid shell variable name.'''

    return _VALID_VARIABLE_RE.fullmatch(string)
