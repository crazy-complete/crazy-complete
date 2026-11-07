# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2025-2026 Benjamin Abendroth <braph93@gmx.de>

'''Built-in manual.'''

from . import completers
from . import yaml_colorize
from .errors import CrazyError
from .str_utils import indent, join_with_wrap


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


def _make_command_section(name, formatter):
    r = formatter.bold('COMMAND')
    r += f'\n{formatter.tab}{name}'
    return r


def _make_description_section(module, formatter):
    r = formatter.bold('DESCRIPTION')
    r += f'\n{formatter.tab}{module.SHORT}'

    long = getattr(module, 'LONG', None)
    if long:
        r += '\n\n'
        r += indent(long.strip(), formatter.tab_width)

    return r


def _make_example_section(module, formatter):
    r = formatter.bold('EXAMPLE')
    r += '\n'

    definition = module.DEFINITION.strip()
    if formatter.use_colors:
        definition = yaml_colorize.colorize(definition)

    r += indent(definition, formatter.tab_width)
    return r


def _make_output_section(module, formatter):
    r = formatter.bold('OUTPUT')
    r += '\n'
    r += indent(module.OUTPUT.strip(), formatter.tab_width)
    return r


def _make_notes_section(notes, formatter):
    if not notes:
        return ''

    r = [formatter.bold('NOTES')]
    for note in notes:
        note = f'{formatter.tab}- {note}'
        r.append(note)

    return '\n'.join(r)


def _make_see_also_section(module, formatter):
    also = getattr(module, 'ALSO', None)
    if not also:
        return ''

    r = formatter.bold('SEE ALSO')
    r += '\n'

    for name, desc in also.items():
        r += f'{formatter.tab}{formatter.bold(name)}: {desc}\n'

    return r.rstrip()


def print_help_for_command(name, use_colors):
    '''Print a manual like help for command `name`.'''

    try:
        module = completers.load(name)
    except ModuleNotFoundError:
        raise CrazyError(f'Command not found: {name}')

    formatter = TerminalFormatter(use_colors, 4)

    notes = list(getattr(module, 'NOTES', None) or [])
    implemented = getattr(module, 'IMPLEMENTED', None)
    if implemented:
        r = 'This completer is currently only implemented in '
        r += implemented[0]
        if len(implemented) > 1:
            r += ' and '
            r += implemented[1]
        notes.append(r)

    r = [
        _make_command_section(name, formatter),
        _make_description_section(module, formatter),
        _make_example_section(module, formatter),
        _make_output_section(module, formatter),
        _make_notes_section(notes, formatter),
        _make_see_also_section(module, formatter),
    ]

    print()
    print('\n\n'.join(l for l in r if l))
    print()


def print_help_topic(topic, use_colors):
    '''Print help for `topic`.'''

    try:
        print_help_for_command(topic, use_colors)
    except CrazyError:
        print('Topic not found')
        print('')
        print('Available completers:')
        print(indent(join_with_wrap(' ', '\n', 40, list(completers.load_all())), 4))
