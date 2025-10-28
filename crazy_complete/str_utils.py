'''String utility functions.'''

import re
import subprocess

from .errors import CrazyError


_VALID_OPTION_STRING_RE = re.compile('-[^\\s,]+')
_VALID_VARIABLE_RE = re.compile('[a-zA-Z_][a-zA-Z0-9_]*')


def contains_space(string):
    '''Check if string contains space type characters.'''

    return (' ' in string or '\t' in string or '\n' in string)


def is_empty_or_whitespace(string):
    '''Check if string is empty or whitespace.'''

    return not string.strip()


def is_valid_extended_regex(string):
    '''Check if string is a valid extended regular expression.'''

    try:
        r = subprocess.run(
            ['grep', '-q', '-E', '--', string],
            input=b"",
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=1,
            check=False)

        return r.returncode != 2
    except (FileNotFoundError, PermissionError, subprocess.TimeoutExpired):
        return True


def validate_prog(string):
    '''Validate a program string.'''

    if is_empty_or_whitespace(string):
        raise CrazyError('value is empty')

    if string.startswith(' '):
        raise CrazyError('begins with space')

    if string.endswith(' '):
        raise CrazyError('ends with space')

    if '\t' in string:
        raise CrazyError('contains a tabulator')

    if '\n' in string:
        raise CrazyError('contains a newline')

    if '  ' in string:
        raise CrazyError('contains multiple spaces')


def indent(string, num_spaces):
    '''Indents each line in a string by a specified number of spaces,
    preserving empty lines.

    Args:
        string (str): The input string to be indented.
        num_spaces (int): The number of spaces to indent each line.

    Returns:
        str: The indented string.
    '''

    assert isinstance(string, str), \
        f"indent: string: expected str, got {string!r}"

    assert isinstance(num_spaces, int), \
        f"indent: num_spaces: expected int, got {num_spaces!r}"

    lines = string.split('\n')
    indented_lines = [((' ' * num_spaces) + line) if line.strip() else line for line in lines]
    return '\n'.join(indented_lines)


def join_with_wrap(primary_sep, secondary_sep, max_line_length, items):
    '''
    Join a list of strings with a primary separator, automatically wrapping
    to a new line (using the secondary separator) when the current line
    would exceed max_line_length.

    Args:
        primary_sep: String used to separate items on the same line.
        secondary_sep: String used to separate wrapped lines.
        max_line_length: Maximum number of characters per line.
        items: List of strings to join.

    Returns:
        str: Joined string with line wrapping
    '''
    lines = []
    current_line = ""

    for item in items:
        candidate = (current_line + primary_sep + item) if current_line else item
        if len(candidate) > max_line_length and current_line:
            lines.append(current_line)
            current_line = item
        else:
            current_line = candidate

    if current_line:
        lines.append(current_line)

    return secondary_sep.join(lines)


def is_valid_option_string(option_string):
    '''Check if `option_string` is a valid option string.'''

    if not _VALID_OPTION_STRING_RE.fullmatch(option_string):
        return False

    if option_string == '--':
        return False

    return True


def is_valid_variable_name(string):
    '''Check if string is a valid shell variable name.'''

    return _VALID_VARIABLE_RE.fullmatch(string)


def strip_comments(string):
    '''Strip shell comments from string.'''

    lines = []

    for line in string.split('\n'):
        if line.lstrip().startswith('#'):
            continue

        lines.append(line)

    return '\n'.join(lines)


def strip_double_empty_lines(string):
    '''Collapse triple newlines into double newlines.'''

    return string.replace('\n\n\n', '\n\n')
