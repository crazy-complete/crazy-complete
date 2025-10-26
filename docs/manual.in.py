'''Built-int Manual.'''

from .errors import CrazyError
from .str_utils import indent, join_with_wrap


%COMMANDS%


class Output:
    def __init__(self, use_colors):
        self.use_colors = use_colors

    def bold(self, s):
        if not self.use_colors:
            print(s, end='')
        else:
            print(f"\033[1m{s}\033[0m", end='')

    def underline(self, s):
        if not self.use_colors:
            print(s, end='')
        else:
            print(f"\033[4m{s}\033[0m", end='')

    def println(self, *args, **kwargs):
        print(*args, **kwargs)

    def print(self, *args):
        print(*args, end='')


def print_help_for_command(name, use_colors):
    command = None
    for cmd in COMMANDS:
        if cmd['command'] == name:
            command = cmd
            break

    if not command:
        raise CrazyError("Command not found: %s" % name)

    tab_width = 4
    tab = ' ' * tab_width

    out = Output(use_colors)
    out.bold('COMMAND')
    out.println()
    out.print(tab)
    out.println(command['command'])
    out.println()

    out.bold('DESCRIPTION')
    out.println()
    out.print(tab)
    out.println(command['short'])
    out.println()

    if command['long']:
        if use_colors:
            out.println(indent(command['long_colored'].strip(), tab_width))
        else:
            out.println(indent(command['long'].strip(), tab_width))
        out.println()

    out.bold('EXAMPLE')
    out.println()
    if use_colors:
        out.println(indent(command['definition_colored'].strip(), tab_width))
    else:
        out.println(indent(command['definition'].strip(), tab_width))
    out.println()

    out.bold('OUTPUT')
    out.println()
    out.println(indent(command['output'].strip(), tab_width))
    out.println()

    if command['notes'] or command['implemented']:
        out.bold('NOTES')
        out.println()

        for note in command['notes']:
            out.print(tab)
            out.println(f'- {note}')

        if command['implemented']:
            out.print(tab)
            out.print('- This completer is currently only implemented in ')
            out.bold(command['implemented'][0])
            if len(command['implemented']) > 1:
                out.print(' and ')
                out.bold(command['implemented'][1])
            out.println('')

    if (command['notes'] or command['implemented']) and command['also']:
        out.println()

    if command['also']:
        out.bold('SEE ALSO')
        out.println()

        for also_cmd, also_desc in command['also'].items():
            out.print(tab)
            out.bold(also_cmd)
            out.println(f': {also_desc}')


def print_help_topic(topic, use_colors):
    try:
        print_help_for_command(topic, use_colors)
    except CrazyError as e:
        commands = [cmd['command'] for cmd in COMMANDS]
        print('Topic not found')
        print('')
        print('Available completers:')
        print(indent(join_with_wrap(' ', '\n', 40, commands), 4))
