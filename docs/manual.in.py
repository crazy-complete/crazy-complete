'''Built-int Manual.'''

from .errors import CrazyError
from .str_utils import indent, join_with_wrap


# flake8: noqa: E501
# pylint: disable=line-too-long
# pylint: disable=too-many-lines


%COMMANDS%


class TerminalFormatter:
    '''Format string for terminals.'''

    def __init__(self, use_colors, tab_width):
        self.use_colors = use_colors
        self.tab_width = tab_width
        self.tab = ' ' * tab_width

    def bold(self, s):
        '''Make bold string.'''

        if not self.use_colors:
            return s

        return f"\033[1m{s}\033[0m"

    def underline(self, s):
        '''Make underline string.'''

        if not self.use_colors:
            return s

        return f"\033[4m{s}\033[0m"


def _make_command_section(command, formatter):
    r = formatter.bold('COMMAND')
    r += f'\n{formatter.tab}{command["command"]}'
    return r


def _make_description_section(command, formatter):
    r = formatter.bold('DESCRIPTION')
    r += f'\n{formatter.tab}{command["short"]}'

    if command['long']:
        r += '\n\n'

        if formatter.use_colors:
            r += indent(command['long_colored'].strip(), formatter.tab_width)
        else:
            r += indent(command['long'].strip(), formatter.tab_width)

    return r


def _make_example_section(command, formatter):
    r = formatter.bold('EXAMPLE')
    r += '\n'

    if formatter.use_colors:
        r += indent(command['definition_colored'].strip(), formatter.tab_width)
    else:
        r += indent(command['definition'].strip(), formatter.tab_width)

    return r


def _make_output_section(command, formatter):
    r = formatter.bold('OUTPUT')
    r += '\n'
    r += indent(command['output'].strip(), formatter.tab_width)
    return r


def _make_notes_sectiong(notes, formatter):
    if not notes:
        return ''

    r = [formatter.bold('NOTES')]

    for note in notes:
        note = f'{formatter.tab}- {note}'
        r.append(note)

    return '\n'.join(r)


def _make_see_also_section(command, formatter):
    if not command['also']:
        return ''

    r = formatter.bold('SEE ALSO')
    r += '\n'

    for also_cmd, also_desc in command['also'].items():
        r += f'{formatter.tab}{formatter.bold(also_cmd)}: {also_desc}\n'

    return r.rstrip()


def print_help_for_command(name, use_colors):
    '''Print a manual like help for command `name`.'''

    command = None
    for cmd in COMMANDS:
        if cmd['command'] == name:
            command = cmd
            break

    if not command:
        raise CrazyError("Command not found: %s" % name)

    formatter = TerminalFormatter(use_colors, 4)

    notes = list(command['notes'])
    if command['implemented']:
        r = 'This completer is currently only implemented in '
        r += command['implemented'][0]
        if len(command['implemented']) > 1:
            r += ' and '
            r += command['implemented'][1]
        notes.append(r)

    r = [
        _make_command_section(command, formatter),
        _make_description_section(command, formatter),
        _make_example_section(command, formatter),
        _make_output_section(command, formatter),
        _make_notes_sectiong(notes, formatter),
        _make_see_also_section(command, formatter),
    ]

    print()
    print('\n\n'.join(l for l in r if l))
    print()


def print_help_topic(topic, use_colors):
    '''Print help for `topic`.'''

    try:
        print_help_for_command(topic, use_colors)
    except CrazyError:
        commands = [cmd['command'] for cmd in COMMANDS]
        print('Topic not found')
        print('')
        print('Available completers:')
        print(indent(join_with_wrap(' ', '\n', 40, commands), 4))
