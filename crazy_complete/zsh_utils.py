'''Utility functions for Zsh.'''

from . import algo
from . import shell

# pylint: disable=too-many-branches
# pylint: disable=too-many-arguments
# pylint: disable=too-many-positional-arguments


def escape_colon(s):
    '''Escape colons in a string with backslash.'''

    return s.replace(':', '\\:')


def escape_square_brackets(s):
    '''Escape square brackets with backslash.'''

    return s.replace('[', '\\[').replace(']', '\\]')


def make_option_spec(
        option_strings,
        conflicting_options = None,
        description         = None,
        complete            = None,
        optional_arg        = False,
        repeatable          = False,
        final               = False,
        metavar             = None,
        action              = None
    ):

    '''
    Make a Zsh option spec.

    Returns something like this:
        (--option -o){--option=,-o+}[Option description]:Metavar:Action
    '''

    result = []

    if conflicting_options is None:
        conflicting_options = []

    # Not options =============================================================
    not_options = []

    for o in sorted(conflicting_options):
        not_options.append(escape_colon(o))

    if not repeatable:
        for o in sorted(option_strings):
            not_options.append(escape_colon(o))

    if final:
        not_options = ['- *']

    if not_options:
        result.append(shell.escape('(%s)' % ' '.join(algo.uniq(not_options))))

    # Repeatable option =======================================================
    if repeatable:
        result.append("'*'")

    # Option strings ==========================================================
    if complete and optional_arg is True:
        opts = [o+'-' if len(o) == 2 else o+'=-' for o in option_strings]
    elif complete:
        opts = [o+'+' if len(o) == 2 else o+'=' for o in option_strings]
    else:
        opts = option_strings

    if len(opts) == 1:
        result.append(opts[0])
    else:
        result.append('{%s}' % ','.join(opts))

    # Description =============================================================
    if description is not None:
        result.append(shell.escape('[%s]' % escape_colon(escape_square_brackets(description))))

    # Complete ================================================================
    if complete:
        if metavar is None:
            metavar = ' '

        result.append(':%s:%s' % (shell.escape(escape_colon(metavar)), action))

    return ''.join(result)


def make_positional_spec(
        number,
        repeatable,
        description,
        action
    ):

    '''
    Make a Zsh positional spec.

    Returns something like this:
        Number:Description:Action
    '''

    if repeatable is True:
        num_spec = "'*'"
    else:
        num_spec = str(number)

    desc_spec = shell.escape(escape_colon(description))

    if action == '_normal':
        return f'{num_spec}::{desc_spec}:{action}'

    return f'{num_spec}:{desc_spec}:{action}'


def make_file_extension_pattern(extensions, fuzzy):
    '''Make a case-insensitive glob pattern matching `extensions`.

    Takes a list of extensions (e.g. ['txt', 'jpg']) and returns a Zsh-style
    pattern that matches all of them, ignoring case.

    Example output:
        '*.(#i)(txt|jpg)'
    '''

    if len(extensions) == 1:
        pattern = '*.(#i)%s' % extensions[0]
    else:
        pattern = '*.(#i)(%s)' % '|'.join(extensions)

    if fuzzy:
        pattern += '*'

    return pattern
