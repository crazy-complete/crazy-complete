# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2025-2026 Benjamin Abendroth <braph93@gmx.de>

'''Built-int Manual.'''

from .errors import CrazyError
from .str_utils import indent, join_with_wrap


# flake8: noqa: E501
# pylint: disable=line-too-long
# pylint: disable=too-many-lines


COMMANDS = [{'also': {'alsa_device': 'For completing ALSA devices'},
  'category': 'bonus',
  'command': 'alsa_card',
  'definition': "prog: 'example'\n"
                'options:\n'
                "  - option_strings: ['--alsa-card']\n"
                "    complete: ['alsa_card']\n",
  'definition_colored': '\x1b[94mprog\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33mexample\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[94moptions\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33m--alsa-card\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33malsa_card\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n",
  'implemented': None,
  'long': None,
  'long_colored': None,
  'notes': [],
  'output': '~ > example --alsa-card=<TAB>\n0  1\n',
  'short': 'Complete ALSA cards'},
 {'also': {'alsa_card': 'For completing ALSA cards'},
  'category': 'bonus',
  'command': 'alsa_device',
  'definition': "prog: 'example'\n"
                'options:\n'
                "  - option_strings: ['--alsa-device']\n"
                "    complete: ['alsa_device']\n",
  'definition_colored': '\x1b[94mprog\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33mexample\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[94moptions\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33m--alsa-device\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33malsa_device\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n",
  'implemented': None,
  'long': None,
  'long_colored': None,
  'notes': [],
  'output': '~ > example --alsa-device=<TAB>\nhw:0  hw:1\n',
  'short': 'Complete ALSA devices'},
 {'also': None,
  'category': 'bonus',
  'command': 'charset',
  'definition': "prog: 'example'\n"
                'options:\n'
                "  - option_strings: ['--charset']\n"
                "    complete: ['charset']\n",
  'definition_colored': '\x1b[94mprog\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33mexample\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[94moptions\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33m--charset\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33mcharset\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n",
  'implemented': None,
  'long': None,
  'long_colored': None,
  'notes': [],
  'output': '~ > example --charset=A<TAB>\n'
            'ANSI_X3.110-1983  ANSI_X3.4-1968    ARMSCII-8         ASMO_449\n',
  'short': 'Complete character sets'},
 {'also': None,
  'category': 'basic',
  'command': 'choices',
  'definition': "prog: 'example'\n"
                'options:\n'
                "  - option_strings: ['--choices-1']\n"
                "    complete: ['choices', ['Item 1', 'Item 2']]\n"
                '\n'
                "  - option_strings: ['--choices-2']\n"
                "    complete: ['choices', {'Item 1': 'Description 1', 'Item "
                "2': 'Description 2'}]\n"
                '\n'
                "  - option_strings: ['--choices-keep-order']\n"
                "    complete: ['choices', ['zebra', 'cat', 'monkey']]\n"
                '    nosort: true\n',
  'definition_colored': '\x1b[94mprog\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33mexample\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[94moptions\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33m--choices-1\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33mchoices\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m,\x1b[37m "
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33mItem\x1b[39;49;00m\x1b[31m "
                        "\x1b[39;49;00m\x1b[33m1\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m,\x1b[37m "
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33mItem\x1b[39;49;00m\x1b[31m "
                        "\x1b[39;49;00m\x1b[33m2\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]]\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33m--choices-2\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33mchoices\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m,\x1b[37m "
                        "\x1b[39;49;00m{\x1b[33m'\x1b[39;49;00m\x1b[33mItem\x1b[39;49;00m\x1b[31m "
                        "\x1b[39;49;00m\x1b[33m1\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m:\x1b[37m "
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33mDescription\x1b[39;49;00m\x1b[31m "
                        "\x1b[39;49;00m\x1b[33m1\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m,\x1b[37m "
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33mItem\x1b[39;49;00m\x1b[31m "
                        "\x1b[39;49;00m\x1b[33m2\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m:\x1b[37m "
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33mDescription\x1b[39;49;00m\x1b[31m "
                        "\x1b[39;49;00m\x1b[33m2\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m}]\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33m--choices-keep-order\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33mchoices\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m,\x1b[37m "
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33mzebra\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m,\x1b[37m "
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33mcat\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m,\x1b[37m "
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33mmonkey\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]]\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mnosort\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00mtrue\x1b[37m\x1b[39;49;00m\n',
  'implemented': None,
  'long': '`ITEMS`:\n'
          '  A list or dictionary containing the values to offer for '
          'completion.\n'
          '\n'
          '  If a list is supplied, all items are offered without '
          'descriptions.\n'
          '\n'
          '  If a dictionary is supplied, the keys are used as completion '
          'values and the\n'
          '  values are used as descriptions.\n',
  'long_colored': '\x1b[33m`ITEMS`\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                  '  A list or dictionary containing the values to offer for '
                  'completion.\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m\x1b[39;49;00m\n'
                  '  If a list is supplied, all items are offered without '
                  'descriptions.\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m\x1b[39;49;00m\n'
                  '  If a dictionary is supplied, the keys are used as '
                  'completion values and the\x1b[37m\x1b[39;49;00m\n'
                  '  values are used as descriptions.\x1b[37m\x1b[39;49;00m\n',
  'notes': ['If the completion suggestions should appear in their original '
            'order, set `nosort` to `true`'],
  'output': '~ > example --choices-2=<TAB>\n'
            'Item 1  (Description 1)  Item 2  (Description 2)\n'
            '\n'
            '~ > example --choices-keep-order=<TAB>\n'
            'zebra    cat    monkey\n',
  'short': 'Complete from a predefined set of values'},
 {'also': None,
  'category': 'meta',
  'command': 'combine',
  'definition': "prog: 'example'\n"
                'options:\n'
                "  - option_strings: ['--combine']\n"
                "    complete: ['combine', [['user'], ['pid']]]\n",
  'definition_colored': '\x1b[94mprog\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33mexample\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[94moptions\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33m--combine\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33mcombine\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m,\x1b[37m "
                        "\x1b[39;49;00m[[\x1b[33m'\x1b[39;49;00m\x1b[33muser\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m],\x1b[37m "
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33mpid\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]]]\x1b[37m\x1b[39;49;00m\n",
  'implemented': None,
  'long': 'Combines multiple completers into a single completer.\n'
          '\n'
          '`COMPLETERS`:\n'
          '  A list of completers to combine.\n',
  'long_colored': 'Combines multiple completers into a single '
                  'completer.\x1b[37m\x1b[39;49;00m\n'
                  '\n'
                  '\x1b[33m`COMPLETERS`\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                  '  A list of completers to combine.\x1b[37m\x1b[39;49;00m\n',
  'notes': [],
  'output': '~ > example --combine=avahi,daemon,<TAB>\n'
            '1439404  3488332  3571716           3607235                 '
            '4134206\n'
            'alpm     avahi    bin               braph                   '
            'daemon\n'
            'root     rtkit    systemd-coredump  systemd-journal-remote  '
            'systemd-network\n'
            '[...]\n',
  'short': 'Combine multiple completers'},
 {'also': {'command_arg': 'For completing arguments of a command',
           'commandline_string': 'For completing command lines as strings'},
  'category': 'basic',
  'command': 'command',
  'definition': "prog: 'example'\n"
                'options:\n'
                "  - option_strings: ['--command']\n"
                "    complete: ['command']\n"
                '\n'
                "  - option_strings: ['--command-sbin']\n"
                "    complete: ['command', {'path_append': "
                "'/sbin:/usr/sbin'}]\n",
  'definition_colored': '\x1b[94mprog\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33mexample\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[94moptions\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33m--command\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33mcommand\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33m--command-sbin\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33mcommand\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m,\x1b[37m "
                        "\x1b[39;49;00m{\x1b[33m'\x1b[39;49;00m\x1b[33mpath_append\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m:\x1b[37m "
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33m/sbin:/usr/sbin\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m}]\x1b[37m\x1b[39;49;00m\n",
  'implemented': None,
  'long': 'This completer provides completion suggestions for executable '
          "commands available in the system's `$PATH`.\n"
          ' \n'
          '`OPTIONS`:\n'
          '  A dictionary containing additional options for configuring the '
          'completion.\n'
          '\n'
          '  - `path`:\n'
          '    Override the default `$PATH` used for searching executables.\n'
          '\n'
          '  - `path_append`:\n'
          '    Append directories to the default `$PATH`.\n'
          '\n'
          '  - `path_prepend`:\n'
          '    Prepend directories to the default `$PATH`.\n',
  'long_colored': 'This completer provides completion suggestions for '
                  "executable commands available in the system's "
                  '\x1b[33m`$PATH`\x1b[39;49;00m.\x1b[37m\x1b[39;49;00m\n'
                  ' \n'
                  '\x1b[33m`OPTIONS`\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                  '  A dictionary containing additional options for '
                  'configuring the completion.\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m  \x1b[39;49;00m\x1b[34m-\x1b[39;49;00m\x1b[37m '
                  '\x1b[39;49;00m\x1b[33m`path`\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                  '    Override the default \x1b[33m`$PATH`\x1b[39;49;00m used '
                  'for searching executables.\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m  \x1b[39;49;00m\x1b[34m-\x1b[39;49;00m\x1b[37m '
                  '\x1b[39;49;00m\x1b[33m`path_append`\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                  '    Append directories to the default '
                  '\x1b[33m`$PATH`\x1b[39;49;00m.\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m  \x1b[39;49;00m\x1b[34m-\x1b[39;49;00m\x1b[37m '
                  '\x1b[39;49;00m\x1b[33m`path_prepend`\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                  '    Prepend directories to the default '
                  '\x1b[33m`$PATH`\x1b[39;49;00m.\x1b[37m\x1b[39;49;00m\n',
  'notes': ['`path_append` and `path_prepend` can be used together, but both '
            'are mutually exclusive with `path`.'],
  'output': '~ > example --command=bas<TAB>\n'
            'base32    base64    basename  basenc    bash      bashbug\n',
  'short': 'Complete command names'},
 {'also': {'command': 'For completing command names',
           'commandline_string': 'For completing command lines as strings'},
  'category': 'basic',
  'command': 'command_arg',
  'definition': "prog: 'example'\n"
                'positionals:\n'
                '  - number: 1\n'
                "    complete: ['command']\n"
                '\n'
                '  - number: 2\n'
                "    complete: ['command_arg']\n"
                '    repeatable: true\n',
  'definition_colored': '\x1b[94mprog\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33mexample\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[94mpositionals\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94mnumber\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m1\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33mcommand\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94mnumber\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m2\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33mcommand_arg\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mrepeatable\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00mtrue\x1b[37m\x1b[39;49;00m\n',
  'implemented': None,
  'long': None,
  'long_colored': None,
  'notes': ['This completer can only be used in combination with a previously '
            'defined `command` completer.',
            'This completer requires `repeatable: true`.'],
  'output': '~ > example sudo bas<TAB>\n'
            'base32    base64    basename  basenc    bash      bashbug\n',
  'short': 'Complete command arguments'},
 {'also': {'command': 'For completing command names',
           'command_arg': 'For completing command arguments'},
  'category': 'basic',
  'command': 'commandline_string',
  'definition': "prog: 'example'\n"
                'options:\n'
                "  - option_strings: ['--commandline']\n"
                "    complete: ['commandline_string']\n",
  'definition_colored': '\x1b[94mprog\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33mexample\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[94moptions\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33m--commandline\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33mcommandline_string\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n",
  'implemented': None,
  'long': None,
  'long_colored': None,
  'notes': [],
  'output': "~ > example --commandline='sudo ba<TAB>\n"
            'base32    base64    basename  basenc    bash      bashbug\n',
  'short': 'Complete command lines as strings'},
 {'also': {'date_format': 'For completing date format strings'},
  'category': 'basic',
  'command': 'date',
  'definition': "prog: 'example'\n"
                'options:\n'
                "  - option_strings: ['--date']\n"
                "    complete: ['date', '%Y-%m-%d']\n",
  'definition_colored': '\x1b[94mprog\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33mexample\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[94moptions\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33m--date\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33mdate\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m,\x1b[37m "
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33m%Y-%m-%d\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n",
  'implemented': ['Zsh'],
  'long': '`FORMAT`:\n  The date format as described in `strftime(3)`.\n',
  'long_colored': '\x1b[33m`FORMAT`\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                  '  The date format as described in '
                  '\x1b[33m`strftime(3)`\x1b[39;49;00m.\x1b[37m\x1b[39;49;00m\n',
  'notes': [],
  'output': '~ > example --date=<TAB>\n'
            '\n'
            '         November\n'
            'Mo  Tu  We  Th  Fr  Sa  Su\n'
            '     1   2   3   4   5   6\n'
            ' 7   8   9  10  11  12  13\n'
            '14  15  16  17  18  19  20\n'
            '21  22  23  24  25  26  27\n'
            '28  29  30\n',
  'short': 'Complete date strings'},
 {'also': {'date': 'For completing dates'},
  'category': 'basic',
  'command': 'date_format',
  'definition': "prog: 'example'\n"
                'options:\n'
                "  - option_strings: ['--date-format']\n"
                "    complete: ['date_format']\n",
  'definition_colored': '\x1b[94mprog\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33mexample\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[94moptions\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33m--date-format\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33mdate_format\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n",
  'implemented': ['Fish', 'Zsh'],
  'long': None,
  'long_colored': None,
  'notes': [],
  'output': "~ > example --date-format '%<TAB>\n"
            'a     -- abbreviated day name\n'
            'A     -- full day name\n'
            'B     -- full month name\n'
            'c     -- preferred locale date and time\n'
            'C     -- 2-digit century\n'
            'd     -- day of month (01-31)\n'
            'D     -- American format month/day/year (%m/%d/%y)\n'
            'e     -- day of month ( 1-31)\n'
            '[...]\n',
  'short': 'Complete date format strings'},
 {'also': {'directory_list': 'For completing comma-separated lists of '
                             'directories'},
  'category': 'basic',
  'command': 'directory',
  'definition': "prog: 'example'\n"
                'options:\n'
                "  - option_strings: ['--directory']\n"
                "    complete: ['directory']\n"
                '\n'
                "  - option_strings: ['--directory-tmp']\n"
                "    complete: ['directory', {'directory': '/tmp'}]\n",
  'definition_colored': '\x1b[94mprog\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33mexample\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[94moptions\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33m--directory\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33mdirectory\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33m--directory-tmp\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33mdirectory\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m,\x1b[37m "
                        "\x1b[39;49;00m{\x1b[33m'\x1b[39;49;00m\x1b[33mdirectory\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m:\x1b[37m "
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33m/tmp\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m}]\x1b[37m\x1b[39;49;00m\n",
  'implemented': None,
  'long': '`OPTIONS`:\n'
          '  A dictionary containing additional options for configuring the '
          'completion.\n'
          '\n'
          '  - `directory`: Restrict completion to directories inside the '
          'specified directory.\n',
  'long_colored': '\x1b[33m`OPTIONS`\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                  '  A dictionary containing additional options for '
                  'configuring the completion.\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m  \x1b[39;49;00m\x1b[34m-\x1b[39;49;00m\x1b[37m '
                  '\x1b[39;49;00m\x1b[33m`directory`\x1b[39;49;00m: Restrict '
                  'completion to directories inside the specified '
                  'directory.\x1b[37m\x1b[39;49;00m\n',
  'notes': [],
  'output': '~ > example --directory=<TAB>\ndir1/  dir2/\n',
  'short': 'Complete directory names'},
 {'also': {'directory': 'For completing directory names',
           'file_list': 'For completing comma-separated lists of files',
           'list': 'For completion comma-separated lists using a completer'},
  'category': 'basic',
  'command': 'directory_list',
  'definition': "prog: 'example'\n"
                'options:\n'
                "  - option_strings: ['--directory-list']\n"
                "    complete: ['directory_list']\n",
  'definition_colored': '\x1b[94mprog\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33mexample\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[94moptions\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33m--directory-list\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33mdirectory_list\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n",
  'implemented': None,
  'long': "This is an alias for `['list', ['directory']]`.\n"
          '\n'
          '`OPTIONS`:\n'
          '  A dictionary containing additional options for configuring the '
          'completion.\n'
          '\n'
          '  - `directory`:\n'
          '    Restrict completion to directories inside the specified '
          'directory.\n'
          '\n'
          '  - `duplicates`:\n'
          '    Allow duplicate values to be offered for completion. Defaults '
          'to `false`.\n'
          '\n'
          '  - `separator`:\n'
          '    The separator used between list elements. Defaults to `,`.\n',
  'long_colored': "This is an alias for \x1b[33m`['list', "
                  "['directory']]`\x1b[39;49;00m.\x1b[37m\x1b[39;49;00m\n"
                  '\n'
                  '\x1b[33m`OPTIONS`\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                  '  A dictionary containing additional options for '
                  'configuring the completion.\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m  \x1b[39;49;00m\x1b[34m-\x1b[39;49;00m\x1b[37m '
                  '\x1b[39;49;00m\x1b[33m`directory`\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                  '    Restrict completion to directories inside the specified '
                  'directory.\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m  \x1b[39;49;00m\x1b[34m-\x1b[39;49;00m\x1b[37m '
                  '\x1b[39;49;00m\x1b[33m`duplicates`\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                  '    Allow duplicate values to be offered for completion. '
                  'Defaults to '
                  '\x1b[33m`false`\x1b[39;49;00m.\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m  \x1b[39;49;00m\x1b[34m-\x1b[39;49;00m\x1b[37m '
                  '\x1b[39;49;00m\x1b[33m`separator`\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                  '    The separator used between list elements. Defaults to '
                  '\x1b[33m`,`\x1b[39;49;00m.\x1b[37m\x1b[39;49;00m\n',
  'notes': [],
  'output': '~ > example --directory-list=directory1,directory2,<TAB>\n'
            'directory3  directory4\n',
  'short': 'Complete comma-separated lists of directories'},
 {'also': {'variable': 'For completing shell variable names'},
  'category': 'basic',
  'command': 'environment',
  'definition': "prog: 'example'\n"
                'options:\n'
                "  - option_strings: ['--environment']\n"
                "    complete: ['environment']\n",
  'definition_colored': '\x1b[94mprog\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33mexample\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[94moptions\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33m--environment\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33menvironment\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n",
  'implemented': None,
  'long': None,
  'long_colored': None,
  'notes': [],
  'output': '~ > example --environment=X<TAB>\n'
            'XDG_RUNTIME_DIR  XDG_SEAT  XDG_SESSION_CLASS  XDG_SESSION_ID\n'
            'XDG_SESSION_TYPE XDG_VTNR\n',
  'short': 'Complete environment variable names'},
 {'also': {'exec_fast': 'Faster implementation of exec',
           'exec_internal': "Use the shell's internal completion mechanisms"},
  'category': 'custom',
  'command': 'exec',
  'definition': "prog: 'example'\n"
                'options:\n'
                "  - option_strings: ['--exec']\n"
                '    complete: [\'exec\', "printf \'%s\\\\t%s\\\\n\' \'Item '
                '1\' \'Description 1\' \'Item 2\' \'Description 2\'"]\n',
  'definition_colored': '\x1b[94mprog\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33mexample\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[94moptions\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33m--exec\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33mexec\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m,\x1b[37m "
                        '\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[33mprintf\x1b[39;49;00m\x1b[31m '
                        "\x1b[39;49;00m\x1b[33m'%s\x1b[39;49;00m\x1b[33m\\\\\x1b[39;49;00m\x1b[33mt%s\x1b[39;49;00m\x1b[33m\\\\\x1b[39;49;00m\x1b[33mn'\x1b[39;49;00m\x1b[31m "
                        "\x1b[39;49;00m\x1b[33m'Item\x1b[39;49;00m\x1b[31m "
                        "\x1b[39;49;00m\x1b[33m1'\x1b[39;49;00m\x1b[31m "
                        "\x1b[39;49;00m\x1b[33m'Description\x1b[39;49;00m\x1b[31m "
                        "\x1b[39;49;00m\x1b[33m1'\x1b[39;49;00m\x1b[31m "
                        "\x1b[39;49;00m\x1b[33m'Item\x1b[39;49;00m\x1b[31m "
                        "\x1b[39;49;00m\x1b[33m2'\x1b[39;49;00m\x1b[31m "
                        "\x1b[39;49;00m\x1b[33m'Description\x1b[39;49;00m\x1b[31m "
                        '\x1b[39;49;00m\x1b[33m2\'\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n',
  'implemented': None,
  'long': '`COMMAND`:\n'
          '  The command or function to execute. Its output must be formatted '
          'as tab-separated values:\n'
          '\n'
          '```\n'
          '<ITEM_1>\\t<DESCRIPTION_1>\n'
          '<ITEM_2>\\t<DESCRIPTION_2>\n'
          '[...]\n'
          '```\n'
          '\n'
          'Each line represents one completion candidate. The item and its '
          'description are separated by a tab character.\n',
  'long_colored': '\x1b[33m`COMMAND`\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                  '  The command or function to execute. Its output must be '
                  'formatted as tab-separated values:\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[33m\x1b[39;49;00m\n'
                  '\x1b[33m```\x1b[39;49;00m\n'
                  '\x1b[33m<ITEM_1>\\t<DESCRIPTION_1>\x1b[39;49;00m\n'
                  '\x1b[33m<ITEM_2>\\t<DESCRIPTION_2>\x1b[39;49;00m\n'
                  '\x1b[33m[...]\x1b[39;49;00m\n'
                  '\x1b[33m```\x1b[39;49;00m\n'
                  '\x1b[37m\x1b[39;49;00m\n'
                  'Each line represents one completion candidate. The item and '
                  'its description are separated by a tab '
                  'character.\x1b[37m\x1b[39;49;00m\n',
  'notes': ['Functions can be put inside a file and included with '
            '`--include-file`'],
  'output': '~ > example --exec=<TAB>\n'
            'Item 1  (Description 1)  Item 2  (Description 2)\n',
  'short': 'Complete values from the output of a command or function'},
 {'also': None,
  'category': 'custom',
  'command': 'exec_fast',
  'definition': "prog: 'example'\n"
                'options:\n'
                "  - option_strings: ['--exec-fast']\n"
                '    complete: [\'exec_fast\', "printf \'%s\\\\t%s\\\\n\' 1 '
                'one 2 two"]\n',
  'definition_colored': '\x1b[94mprog\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33mexample\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[94moptions\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33m--exec-fast\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33mexec_fast\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m,\x1b[37m "
                        '\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[33mprintf\x1b[39;49;00m\x1b[31m '
                        "\x1b[39;49;00m\x1b[33m'%s\x1b[39;49;00m\x1b[33m\\\\\x1b[39;49;00m\x1b[33mt%s\x1b[39;49;00m\x1b[33m\\\\\x1b[39;49;00m\x1b[33mn'\x1b[39;49;00m\x1b[31m "
                        '\x1b[39;49;00m\x1b[33m1\x1b[39;49;00m\x1b[31m '
                        '\x1b[39;49;00m\x1b[33mone\x1b[39;49;00m\x1b[31m '
                        '\x1b[39;49;00m\x1b[33m2\x1b[39;49;00m\x1b[31m '
                        '\x1b[39;49;00m\x1b[33mtwo\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n',
  'implemented': None,
  'long': 'Faster version of `exec` for handling large amounts of data.\n'
          '\n'
          'Unlike `exec`, this implementation does not safely handle arbitrary '
          'output.\n'
          'Completion items must not contain whitespace or special shell '
          'characters.\n',
  'long_colored': 'Faster version of \x1b[33m`exec`\x1b[39;49;00m for handling '
                  'large amounts of data.\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m\x1b[39;49;00m\n'
                  'Unlike \x1b[33m`exec`\x1b[39;49;00m, this implementation '
                  'does not safely handle arbitrary '
                  'output.\x1b[37m\x1b[39;49;00m\n'
                  'Completion items must not contain whitespace or special '
                  'shell characters.\x1b[37m\x1b[39;49;00m\n',
  'notes': ['Functions can be put inside a file and included with '
            '`--include-file`'],
  'output': '~ > example --exec-fast=<TAB>\n1  -- one\n2  -- one\n',
  'short': 'Complete values from the output of a command or function (fast and '
           'unsafe)'},
 {'also': None,
  'category': 'custom',
  'command': 'exec_internal',
  'definition': "prog: 'example'\n"
                'options:\n'
                "  - option_strings: ['--exec-internal']\n"
                "    complete: ['exec_internal', 'my_completion_func']\n",
  'definition_colored': '\x1b[94mprog\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33mexample\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[94moptions\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33m--exec-internal\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33mexec_internal\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m,\x1b[37m "
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33mmy_completion_func\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n",
  'implemented': None,
  'long': 'Execute a function that internally modifies the completion state.\n'
          '\n'
          'This is useful if a more advanced completion is needed.\n'
          '\n'
          'For **Bash**, it might look like:\n'
          '\n'
          '```sh\n'
          'my_completion_func() {\n'
          "    COMPREPLY=( $(compgen -W 'read write append' -- '$cur') )\n"
          '}\n'
          '```\n'
          '\n'
          'For **Zsh**, it might look like:\n'
          '\n'
          '```sh\n'
          'my_completion_func() {\n'
          '    local items=(\n'
          "        read:'Read data from a file'\n"
          "        write:'Write data from a file'\n"
          "        append:'Append data to a file'\n"
          '    )\n'
          '\n'
          "    _describe 'my items' items\n"
          '}\n'
          '```\n'
          '\n'
          'For **Fish**, it might look like:\n'
          '\n'
          '```sh\n'
          'function my_completion_func\n'
          "    printf '%s\\t%s\\n' \\\n"
          "        read 'Read data from a file'  \\\n"
          "        write 'Write data from a file' \\\n"
          "        append 'Append data to a file'\n"
          'end\n'
          '```\n',
  'long_colored': 'Execute a function that internally modifies the completion '
                  'state.\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m\x1b[39;49;00m\n'
                  'This is useful if a more advanced completion is '
                  'needed.\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m\x1b[39;49;00m\n'
                  'For **Bash**, it might look like:\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[33m\x1b[39;49;00m\n'
                  '\x1b[33m```\x1b[39;49;00m\x1b[33msh\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n'
                  'my_completion_func()\x1b[37m '
                  '\x1b[39;49;00m{\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m    '
                  '\x1b[39;49;00m\x1b[31mCOMPREPLY\x1b[39;49;00m=(\x1b[37m '
                  '\x1b[39;49;00m\x1b[34m$(\x1b[39;49;00m\x1b[36mcompgen\x1b[39;49;00m\x1b[37m '
                  "\x1b[39;49;00m-W\x1b[37m \x1b[39;49;00m\x1b[33m'read write "
                  "append'\x1b[39;49;00m\x1b[37m \x1b[39;49;00m--\x1b[37m "
                  "\x1b[39;49;00m\x1b[33m'$cur'\x1b[39;49;00m\x1b[34m)\x1b[39;49;00m\x1b[37m "
                  '\x1b[39;49;00m)\x1b[37m\x1b[39;49;00m\n'
                  '}\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[33m```\x1b[39;49;00m\n'
                  '\x1b[37m\x1b[39;49;00m\n'
                  'For **Zsh**, it might look like:\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[33m\x1b[39;49;00m\n'
                  '\x1b[33m```\x1b[39;49;00m\x1b[33msh\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n'
                  'my_completion_func()\x1b[37m '
                  '\x1b[39;49;00m{\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m    '
                  '\x1b[39;49;00m\x1b[36mlocal\x1b[39;49;00m\x1b[37m '
                  '\x1b[39;49;00m\x1b[31mitems\x1b[39;49;00m=(\x1b[37m\x1b[39;49;00m\n'
                  "\x1b[37m        \x1b[39;49;00mread:\x1b[33m'Read data from "
                  "a file'\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n"
                  "\x1b[37m        \x1b[39;49;00mwrite:\x1b[33m'Write data "
                  "from a file'\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n"
                  "\x1b[37m        \x1b[39;49;00mappend:\x1b[33m'Append data "
                  "to a file'\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n"
                  '\x1b[37m    \x1b[39;49;00m)\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m    \x1b[39;49;00m_describe\x1b[37m '
                  "\x1b[39;49;00m\x1b[33m'my items'\x1b[39;49;00m\x1b[37m "
                  '\x1b[39;49;00mitems\x1b[37m\x1b[39;49;00m\n'
                  '}\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[33m```\x1b[39;49;00m\n'
                  '\x1b[37m\x1b[39;49;00m\n'
                  'For **Fish**, it might look like:\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[33m\x1b[39;49;00m\n'
                  '\x1b[33m```\x1b[39;49;00m\x1b[33msh\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[34mfunction\x1b[39;49;00m\x1b[37m '
                  '\x1b[39;49;00mmy_completion_func\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m    '
                  '\x1b[39;49;00m\x1b[36mprintf\x1b[39;49;00m\x1b[37m '
                  "\x1b[39;49;00m\x1b[33m'%s\\t%s\\n'\x1b[39;49;00m\x1b[37m "
                  '\x1b[39;49;00m\x1b[33m\\\x1b[39;49;00m\n'
                  '\x1b[37m        '
                  '\x1b[39;49;00m\x1b[36mread\x1b[39;49;00m\x1b[37m '
                  "\x1b[39;49;00m\x1b[33m'Read data from a "
                  "file'\x1b[39;49;00m\x1b[37m  "
                  '\x1b[39;49;00m\x1b[33m\\\x1b[39;49;00m\n'
                  '\x1b[37m        \x1b[39;49;00mwrite\x1b[37m '
                  "\x1b[39;49;00m\x1b[33m'Write data from a "
                  "file'\x1b[39;49;00m\x1b[37m "
                  '\x1b[39;49;00m\x1b[33m\\\x1b[39;49;00m\n'
                  '\x1b[37m        \x1b[39;49;00mappend\x1b[37m '
                  "\x1b[39;49;00m\x1b[33m'Append data to a "
                  "file'\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n"
                  'end\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[33m```\x1b[39;49;00m\n',
  'notes': ['Functions can be put inside a file and included with '
            '`--include-file`'],
  'output': '~ > example --exec-internal=<TAB>\n'
            'append  -- Append data to a file\n'
            'read    -- Read data from a file\n'
            'write   -- Write data from a file\n',
  'short': "Use the shell's internal completion mechanisms"},
 {'also': {'file_list': 'For completing comma-separated lists of files',
           'mime_file': 'For completing files by MIME type'},
  'category': 'basic',
  'command': 'file',
  'definition': "prog: 'example'\n"
                'options:\n'
                "  - option_strings: ['--file']\n"
                "    complete: ['file']\n"
                '\n'
                "  - option_strings: ['--file-tmp']\n"
                "    complete: ['file', {'directory': '/tmp'}]\n"
                '\n'
                "  - option_strings: ['--file-ext']\n"
                "    complete: ['file', {'extensions': ['c', 'cpp']}]\n"
                '\n'
                "  - option_strings: ['--file-ignore']\n"
                "    complete: ['file', {'ignore_globs': ['*.[tT][xX][tT]', "
                "'*.c++']}]\n",
  'definition_colored': '\x1b[94mprog\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33mexample\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[94moptions\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33m--file\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33mfile\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33m--file-tmp\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33mfile\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m,\x1b[37m "
                        "\x1b[39;49;00m{\x1b[33m'\x1b[39;49;00m\x1b[33mdirectory\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m:\x1b[37m "
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33m/tmp\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m}]\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33m--file-ext\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33mfile\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m,\x1b[37m "
                        "\x1b[39;49;00m{\x1b[33m'\x1b[39;49;00m\x1b[33mextensions\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m:\x1b[37m "
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33mc\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m,\x1b[37m "
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33mcpp\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]}]\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33m--file-ignore\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33mfile\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m,\x1b[37m "
                        "\x1b[39;49;00m{\x1b[33m'\x1b[39;49;00m\x1b[33mignore_globs\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m:\x1b[37m "
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33m*.[tT][xX][tT]\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m,\x1b[37m "
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33m*.c++\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]}]\x1b[37m\x1b[39;49;00m\n",
  'implemented': None,
  'long': '`OPTIONS`:\n'
          '  A dictionary containing additional options for configuring the '
          'completion.\n'
          '\n'
          '  - `directory`: Restrict completion to files inside the specified '
          'directory.\n'
          '\n'
          '  - `extensions`: A list of file extensions to offer for '
          'completion.\n'
          '\n'
          '  - `fuzzy`:\n'
          '    Enable fuzzy extension matching.\n'
          '    By default, files must end with one of the specified '
          'extensions.\n'
          '    With fuzzy matching enabled, files with additional suffixes are '
          'also matched, for example `foo.txt.1`.\n'
          '  \n'
          '  - `ignore_globs`:\n'
          '    A list of Bash globs for files that should not be offered for '
          'completion.\n'
          '\n'
          '**NOTE:** Restricting completion to specific file extensions only '
          'makes sense\n'
          'if the program being completed actually expects files of those '
          'types. On\n'
          'Unix-like systems, file extensions generally have no inherent '
          'meaning and are\n'
          'only conventions.\n',
  'long_colored': '\x1b[33m`OPTIONS`\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                  '  A dictionary containing additional options for '
                  'configuring the completion.\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m  \x1b[39;49;00m\x1b[34m-\x1b[39;49;00m\x1b[37m '
                  '\x1b[39;49;00m\x1b[33m`directory`\x1b[39;49;00m: Restrict '
                  'completion to files inside the specified '
                  'directory.\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m  \x1b[39;49;00m\x1b[34m-\x1b[39;49;00m\x1b[37m '
                  '\x1b[39;49;00m\x1b[33m`extensions`\x1b[39;49;00m: A list of '
                  'file extensions to offer for '
                  'completion.\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m  \x1b[39;49;00m\x1b[34m-\x1b[39;49;00m\x1b[37m '
                  '\x1b[39;49;00m\x1b[33m`fuzzy`\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                  '    Enable fuzzy extension matching.\x1b[37m\x1b[39;49;00m\n'
                  '    By default, files must end with one of the specified '
                  'extensions.\x1b[37m\x1b[39;49;00m\n'
                  '    With fuzzy matching enabled, files with additional '
                  'suffixes are also matched, for example '
                  '\x1b[33m`foo.txt.1`\x1b[39;49;00m.\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m  \x1b[39;49;00m\n'
                  '\x1b[37m  \x1b[39;49;00m\x1b[34m-\x1b[39;49;00m\x1b[37m '
                  '\x1b[39;49;00m\x1b[33m`ignore_globs`\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                  '    A list of Bash globs for files that should not be '
                  'offered for completion.\x1b[37m\x1b[39;49;00m\n'
                  '\n'
                  '**NOTE:** Restricting completion to specific file '
                  'extensions only makes sense\x1b[37m\x1b[39;49;00m\n'
                  'if the program being completed actually expects files of '
                  'those types. On\x1b[37m\x1b[39;49;00m\n'
                  'Unix-like systems, file extensions generally have no '
                  'inherent meaning and are\x1b[37m\x1b[39;49;00m\n'
                  'only conventions.\x1b[37m\x1b[39;49;00m\n',
  'notes': [],
  'output': '~ > example --file=<TAB>\n'
            'dir1/  dir2/  file1  file2\n'
            '\n'
            '~ > example --file-ext=<TAB>\n'
            'dir1/  dir2/  file.c  file.cpp\n',
  'short': 'Complete file names'},
 {'also': {'directory_list': 'For completing comma-separated lists of '
                             'directories',
           'file': 'For completing file names',
           'list': 'For completing comma-separted lists using a completer'},
  'category': 'basic',
  'command': 'file_list',
  'definition': "prog: 'example'\n"
                'options:\n'
                "  - option_strings: ['--file-list']\n"
                "    complete: ['file_list']\n",
  'definition_colored': '\x1b[94mprog\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33mexample\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[94moptions\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33m--file-list\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33mfile_list\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n",
  'implemented': None,
  'long': "This is an alias for `['list', ['file']]`.\n"
          '\n'
          '`OPTIONS`:\n'
          '  A dictionary containing additional options for configuring the '
          'completion.\n'
          '\n'
          '  - `directory`:\n'
          '    Restrict completion to files inside the specified directory.\n'
          '\n'
          '  - `extensions`:\n'
          '    A list of file extensions to offer for completion.\n'
          '\n'
          '  - `fuzzy`:\n'
          '    Enable fuzzy extension matching. By default, files must end '
          'with one of\n'
          '    the specified extensions. With fuzzy matching enabled, files '
          'with\n'
          '    additional suffixes are also matched, for example `foo.txt.1`.\n'
          '\n'
          '  - `ignore_globs`:\n'
          '    A list of Bash globs for files that should not be offered for '
          'completion.\n'
          '\n'
          '  - `duplicates`:\n'
          '    Allow duplicate values to be offered for completion. Defaults '
          'to `false`.\n'
          '\n'
          '  - `separator`:\n'
          '    The separator used between list elements. Defaults to `,`.\n',
  'long_colored': "This is an alias for \x1b[33m`['list', "
                  "['file']]`\x1b[39;49;00m.\x1b[37m\x1b[39;49;00m\n"
                  '\n'
                  '\x1b[33m`OPTIONS`\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                  '  A dictionary containing additional options for '
                  'configuring the completion.\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m  \x1b[39;49;00m\x1b[34m-\x1b[39;49;00m\x1b[37m '
                  '\x1b[39;49;00m\x1b[33m`directory`\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                  '    Restrict completion to files inside the specified '
                  'directory.\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m  \x1b[39;49;00m\x1b[34m-\x1b[39;49;00m\x1b[37m '
                  '\x1b[39;49;00m\x1b[33m`extensions`\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                  '    A list of file extensions to offer for '
                  'completion.\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m  \x1b[39;49;00m\x1b[34m-\x1b[39;49;00m\x1b[37m '
                  '\x1b[39;49;00m\x1b[33m`fuzzy`\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                  '    Enable fuzzy extension matching. By default, files must '
                  'end with one of\x1b[37m\x1b[39;49;00m\n'
                  '    the specified extensions. With fuzzy matching enabled, '
                  'files with\x1b[37m\x1b[39;49;00m\n'
                  '    additional suffixes are also matched, for example '
                  '\x1b[33m`foo.txt.1`\x1b[39;49;00m.\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m  \x1b[39;49;00m\x1b[34m-\x1b[39;49;00m\x1b[37m '
                  '\x1b[39;49;00m\x1b[33m`ignore_globs`\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                  '    A list of Bash globs for files that should not be '
                  'offered for completion.\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m  \x1b[39;49;00m\x1b[34m-\x1b[39;49;00m\x1b[37m '
                  '\x1b[39;49;00m\x1b[33m`duplicates`\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                  '    Allow duplicate values to be offered for completion. '
                  'Defaults to '
                  '\x1b[33m`false`\x1b[39;49;00m.\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m  \x1b[39;49;00m\x1b[34m-\x1b[39;49;00m\x1b[37m '
                  '\x1b[39;49;00m\x1b[33m`separator`\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                  '    The separator used between list elements. Defaults to '
                  '\x1b[33m`,`\x1b[39;49;00m.\x1b[37m\x1b[39;49;00m\n',
  'notes': [],
  'output': '~ > example --file-list=file1,file2,<TAB>\nfile3  file4\n',
  'short': 'Complete comma-separated lists of files'},
 {'also': None,
  'category': 'basic',
  'command': 'filesystem_type',
  'definition': "prog: 'example'\n"
                'options:\n'
                "  - option_strings: ['--filesystem-type']\n"
                "    complete: ['filesystem_type']\n",
  'definition_colored': '\x1b[94mprog\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33mexample\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[94moptions\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33m--filesystem-type\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33mfilesystem_type\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n",
  'implemented': None,
  'long': None,
  'long_colored': None,
  'notes': [],
  'output': '~ > example --filesystem-type=<TAB>\n'
            'adfs     autofs   bdev      bfs     binder     binfmt_misc  bpf\n'
            'cgroup   cgroup2  configfs  cramfs  debugfs    devpts       '
            'devtmpfs\n'
            '[...]\n',
  'short': 'Complete filesystem types'},
 {'also': {'integer': 'For completing integer values'},
  'category': 'basic',
  'command': 'float',
  'definition': "prog: 'example'\n"
                'options:\n'
                "  - option_strings: ['--time']\n"
                "    complete: ['float', {'suffixes': {'s': 'seconds', 'm': "
                "'minutes', 'h': 'hours'}}]\n",
  'definition_colored': '\x1b[94mprog\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33mexample\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[94moptions\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33m--time\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33mfloat\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m,\x1b[37m "
                        "\x1b[39;49;00m{\x1b[33m'\x1b[39;49;00m\x1b[33msuffixes\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m:\x1b[37m "
                        "\x1b[39;49;00m{\x1b[33m'\x1b[39;49;00m\x1b[33ms\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m:\x1b[37m "
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33mseconds\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m,\x1b[37m "
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33mm\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m:\x1b[37m "
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33mminutes\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m,\x1b[37m "
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33mh\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m:\x1b[37m "
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33mhours\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m}}]\x1b[37m\x1b[39;49;00m\n",
  'implemented': None,
  'long': '`OPTIONS`:\n'
          '  A dictionary containing additional options for configuring the '
          'completion.\n'
          '\n'
          '  - `min`: The minimum allowed value.\n'
          '\n'
          '  - `max`: The maximum allowed value.\n'
          '\n'
          '  - `suffixes`: A dictionary of suffixes and their descriptions. '
          'The suffix is appended to the completed value.\n'
          '\n'
          '  - `help`: The help text shown during completion. If not '
          'specified, the `help` attribute of the option is used.\n',
  'long_colored': '\x1b[33m`OPTIONS`\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                  '  A dictionary containing additional options for '
                  'configuring the completion.\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m  \x1b[39;49;00m\x1b[34m-\x1b[39;49;00m\x1b[37m '
                  '\x1b[39;49;00m\x1b[33m`min`\x1b[39;49;00m: The minimum '
                  'allowed value.\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m  \x1b[39;49;00m\x1b[34m-\x1b[39;49;00m\x1b[37m '
                  '\x1b[39;49;00m\x1b[33m`max`\x1b[39;49;00m: The maximum '
                  'allowed value.\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m  \x1b[39;49;00m\x1b[34m-\x1b[39;49;00m\x1b[37m '
                  '\x1b[39;49;00m\x1b[33m`suffixes`\x1b[39;49;00m: A '
                  'dictionary of suffixes and their descriptions. The suffix '
                  'is appended to the completed value.\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m  \x1b[39;49;00m\x1b[34m-\x1b[39;49;00m\x1b[37m '
                  '\x1b[39;49;00m\x1b[33m`help`\x1b[39;49;00m: The help text '
                  'shown during completion. If not specified, the '
                  '\x1b[33m`help`\x1b[39;49;00m attribute of the option is '
                  'used.\x1b[37m\x1b[39;49;00m\n',
  'notes': [],
  'output': '~ > example --time=3.0<TAB>\n'
            's -- seconds  m -- minutes  h -- hours\n',
  'short': 'Complete floating-point values'},
 {'also': {'group': 'For completing group names'},
  'category': 'basic',
  'command': 'gid',
  'definition': "prog: 'example'\n"
                'options:\n'
                "  - option_strings: ['--gid']\n"
                "    complete: ['gid']\n",
  'definition_colored': '\x1b[94mprog\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33mexample\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[94moptions\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33m--gid\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33mgid\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n",
  'implemented': None,
  'long': None,
  'long_colored': None,
  'notes': [],
  'output': '~ > example --gid=<TAB>\n'
            '0      -- root\n'
            '1000   -- braph\n'
            '102    -- polkitd\n'
            '108    -- vboxusers\n'
            '11     -- ftp\n'
            '12     -- mail\n'
            '133    -- rtkit\n'
            '19     -- log\n'
            '[...]\n',
  'short': 'Complete group IDs'},
 {'also': {'gid': 'For completing group IDs'},
  'category': 'basic',
  'command': 'group',
  'definition': "prog: 'example'\n"
                'options:\n'
                "  - option_strings: ['--group']\n"
                "    complete: ['group']\n",
  'definition_colored': '\x1b[94mprog\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33mexample\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[94moptions\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33m--group\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33mgroup\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n",
  'implemented': None,
  'long': None,
  'long_colored': None,
  'notes': [],
  'output': '~ > example --group=<TAB>\n'
            'adm           audio        avahi\n'
            'bin           braph        colord\n'
            'daemon        dbus         dhcpcd\n'
            'disk          floppy       ftp\n'
            'games         git          groups\n'
            '[...]\n',
  'short': 'Complete group names'},
 {'also': None,
  'category': 'basic',
  'command': 'history',
  'definition': "prog: 'example'\n"
                'options:\n'
                "  - option_strings: ['--history']\n"
                "    complete: ['history', '[a-zA-Z0-9]+@[a-zA-Z0-9]+']\n",
  'definition_colored': '\x1b[94mprog\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33mexample\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[94moptions\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33m--history\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33mhistory\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m,\x1b[37m "
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33m[a-zA-Z0-9]+@[a-zA-Z0-9]+\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n",
  'implemented': None,
  'long': '`REGEX`:\n'
          '  An extended regular expression used to filter history entries.\n'
          '  The regular expression is passed to `grep -E`.\n',
  'long_colored': '\x1b[33m`REGEX`\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                  '  An extended regular expression used to filter history '
                  'entries.\x1b[37m\x1b[39;49;00m\n'
                  '  The regular expression is passed to \x1b[33m`grep '
                  '-E`\x1b[39;49;00m.\x1b[37m\x1b[39;49;00m\n',
  'notes': [],
  'output': '~ > example --history=<TAB>\nfoo@bar  mymail@myprovider\n',
  'short': "Complete based on a shell's history"},
 {'also': {'ip_address': 'For completing local IP addresses'},
  'category': 'basic',
  'command': 'hostname',
  'definition': "prog: 'example'\n"
                'options:\n'
                "  - option_strings: ['--hostname']\n"
                "    complete: ['hostname']\n",
  'definition_colored': '\x1b[94mprog\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33mexample\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[94moptions\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33m--hostname\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33mhostname\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n",
  'implemented': None,
  'long': None,
  'long_colored': None,
  'notes': [],
  'output': '~ > example --hostname=<TAB>\nlocalhost\n',
  'short': 'Complete hostnames'},
 {'also': {'float': 'For completing floating-point values',
           'range': 'For completing sequences of integers'},
  'category': 'basic',
  'command': 'integer',
  'definition': "prog: 'example'\n"
                'options:\n'
                "  - option_strings: ['--time']\n"
                "    complete: ['integer', {'suffixes': {'s': 'seconds', 'm': "
                "'minutes', 'h': 'hours'}}]\n",
  'definition_colored': '\x1b[94mprog\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33mexample\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[94moptions\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33m--time\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33minteger\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m,\x1b[37m "
                        "\x1b[39;49;00m{\x1b[33m'\x1b[39;49;00m\x1b[33msuffixes\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m:\x1b[37m "
                        "\x1b[39;49;00m{\x1b[33m'\x1b[39;49;00m\x1b[33ms\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m:\x1b[37m "
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33mseconds\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m,\x1b[37m "
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33mm\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m:\x1b[37m "
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33mminutes\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m,\x1b[37m "
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33mh\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m:\x1b[37m "
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33mhours\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m}}]\x1b[37m\x1b[39;49;00m\n",
  'implemented': None,
  'long': '`OPTIONS`:\n'
          '  A dictionary containing additional options for configuring the '
          'completion.\n'
          '\n'
          '  - `min`: The minimum allowed value.\n'
          '\n'
          '  - `max`: The maximum allowed value.\n'
          '\n'
          '  - `suffixes`: A dictionary of suffixes and their descriptions. '
          'The suffix is appended to the completed value.\n'
          '\n'
          '  - `help`: The help text shown during completion. If not '
          'specified, the `help` attribute of the option is used.\n',
  'long_colored': '\x1b[33m`OPTIONS`\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                  '  A dictionary containing additional options for '
                  'configuring the completion.\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m  \x1b[39;49;00m\x1b[34m-\x1b[39;49;00m\x1b[37m '
                  '\x1b[39;49;00m\x1b[33m`min`\x1b[39;49;00m: The minimum '
                  'allowed value.\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m  \x1b[39;49;00m\x1b[34m-\x1b[39;49;00m\x1b[37m '
                  '\x1b[39;49;00m\x1b[33m`max`\x1b[39;49;00m: The maximum '
                  'allowed value.\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m  \x1b[39;49;00m\x1b[34m-\x1b[39;49;00m\x1b[37m '
                  '\x1b[39;49;00m\x1b[33m`suffixes`\x1b[39;49;00m: A '
                  'dictionary of suffixes and their descriptions. The suffix '
                  'is appended to the completed value.\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m  \x1b[39;49;00m\x1b[34m-\x1b[39;49;00m\x1b[37m '
                  '\x1b[39;49;00m\x1b[33m`help`\x1b[39;49;00m: The help text '
                  'shown during completion. If not specified, the '
                  '\x1b[33m`help`\x1b[39;49;00m attribute of the option is '
                  'used.\x1b[37m\x1b[39;49;00m\n',
  'notes': [],
  'output': '~ > example --integer=3<TAB>\n'
            's -- seconds  m -- minutes  h -- hours\n',
  'short': 'Complete integer values'},
 {'also': {'hostname': 'For completing hostnames',
           'net_interface': 'For completing network interfaces'},
  'category': 'basic',
  'command': 'ip_address',
  'definition': "prog: 'example'\n"
                'options:\n'
                "  - option_strings: ['--ip-address']\n"
                "    complete: ['ip_address']\n"
                '\n'
                "  - option_strings: ['--ip-address-v4']\n"
                "    complete: ['ip_address', 'ipv4']\n"
                '\n'
                "  - option_strings: ['--ip-address-v6']\n"
                "    complete: ['ip_address', 'ipv6']\n",
  'definition_colored': '\x1b[94mprog\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33mexample\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[94moptions\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33m--ip-address\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33mip_address\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33m--ip-address-v4\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33mip_address\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m,\x1b[37m "
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33mipv4\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33m--ip-address-v6\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33mip_address\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m,\x1b[37m "
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33mipv6\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n",
  'implemented': None,
  'long': '`TYPE`:\n'
          '  The type of ip addresses to complete:\n'
          '\n'
          '  - `ipv4`: IPv4 addresses\n'
          '  - `ipv6`: IPv6 addresses\n'
          '  - `all`:  Both IPv4 and IPv6 addresses\n'
          '\n'
          '  Append `+` to include the unspecified address of the selected '
          'family:\n'
          '\n'
          '  - `ipv4+`: Includes `0.0.0.0`\n'
          '  - `ipv6+`: Includes `::`\n'
          '  - `all+`:  Includes both 0.0.0.0 and `::`\n',
  'long_colored': '\x1b[33m`TYPE`\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                  '  The type of ip addresses to '
                  'complete:\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m  \x1b[39;49;00m\x1b[34m-\x1b[39;49;00m\x1b[37m '
                  '\x1b[39;49;00m\x1b[33m`ipv4`\x1b[39;49;00m: IPv4 '
                  'addresses\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m  \x1b[39;49;00m\x1b[34m-\x1b[39;49;00m\x1b[37m '
                  '\x1b[39;49;00m\x1b[33m`ipv6`\x1b[39;49;00m: IPv6 '
                  'addresses\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m  \x1b[39;49;00m\x1b[34m-\x1b[39;49;00m\x1b[37m '
                  '\x1b[39;49;00m\x1b[33m`all`\x1b[39;49;00m:  Both IPv4 and '
                  'IPv6 addresses\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m\x1b[39;49;00m\n'
                  '  Append \x1b[33m`+`\x1b[39;49;00m to include the '
                  'unspecified address of the selected '
                  'family:\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m  \x1b[39;49;00m\x1b[34m-\x1b[39;49;00m\x1b[37m '
                  '\x1b[39;49;00m\x1b[33m`ipv4+`\x1b[39;49;00m: Includes '
                  '\x1b[33m`0.0.0.0`\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m  \x1b[39;49;00m\x1b[34m-\x1b[39;49;00m\x1b[37m '
                  '\x1b[39;49;00m\x1b[33m`ipv6+`\x1b[39;49;00m: Includes '
                  '\x1b[33m`::`\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m  \x1b[39;49;00m\x1b[34m-\x1b[39;49;00m\x1b[37m '
                  '\x1b[39;49;00m\x1b[33m`all+`\x1b[39;49;00m:  Includes both '
                  '0.0.0.0 and '
                  '\x1b[33m`::`\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n',
  'notes': [],
  'output': '~ > example --ip-address=<TAB>\n'
            '::1    10.0.0.71   127.0.0.1   fe80::f567:7a1a:3c98:808d\n'
            '\n'
            '~ > example --ip-address-v4=<TAB>\n'
            '10.0.0.71   127.0.0.1\n'
            '\n'
            '~ > example --ip-address-v6=<TAB>\n'
            '::1   fe80::f567:7a1a:3c98:808d\n',
  'short': 'Complete local IP addresses'},
 {'also': {'key_value_list_exec': 'For completing comma-separated lists of '
                                  'key=value pairs (dynamically generated by a '
                                  'function)',
           'key_value_pair': 'For completing single key=value pairs',
           'list': 'For completing comma-separated lists using a completer',
           'value_list': 'For completing comma-separated lists of values'},
  'category': 'meta',
  'command': 'key_value_list',
  'definition': "prog: 'example'\n"
                'options:\n'
                "  - option_strings: ['--key-value-list']\n"
                "    complete: ['key_value_list', ',', '=', [\n"
                "      ['flag',        'An option flag', null],\n"
                "      ['nodesc',      null, null],\n"
                "      ['nocomp',      'An option with arg but without "
                "completer', ['none']],\n"
                "      ['user',        'Takes a username', ['user']],\n"
                "      ['*repeatable', 'This option is repeatable', null],\n"
                "      ['exclusive',   'This option disables other options', "
                "null, ['flag', 'nodesc', 'nocomp']],\n"
                "      ['check',       'Specify file name conversions', "
                "['choices', {\n"
                "        'relaxed': 'convert to lowercase before lookup',\n"
                "        'strict': 'no conversion'\n"
                '      }]]\n'
                '    ]]\n',
  'definition_colored': '\x1b[94mprog\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33mexample\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[94moptions\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33m--key-value-list\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33mkey_value_list\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m,\x1b[37m "
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33m,\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m,\x1b[37m "
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33m=\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m,\x1b[37m "
                        '\x1b[39;49;00m[\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m      '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33mflag\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m,\x1b[37m        "
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33mAn\x1b[39;49;00m\x1b[31m "
                        '\x1b[39;49;00m\x1b[33moption\x1b[39;49;00m\x1b[31m '
                        "\x1b[39;49;00m\x1b[33mflag\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m,\x1b[37m "
                        '\x1b[39;49;00m\x1b[31mnull\x1b[39;49;00m],\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m      '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33mnodesc\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m,\x1b[37m      "
                        '\x1b[39;49;00m\x1b[31mnull\x1b[39;49;00m,\x1b[37m '
                        '\x1b[39;49;00m\x1b[31mnull\x1b[39;49;00m],\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m      '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33mnocomp\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m,\x1b[37m      "
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33mAn\x1b[39;49;00m\x1b[31m "
                        '\x1b[39;49;00m\x1b[33moption\x1b[39;49;00m\x1b[31m '
                        '\x1b[39;49;00m\x1b[33mwith\x1b[39;49;00m\x1b[31m '
                        '\x1b[39;49;00m\x1b[33marg\x1b[39;49;00m\x1b[31m '
                        '\x1b[39;49;00m\x1b[33mbut\x1b[39;49;00m\x1b[31m '
                        '\x1b[39;49;00m\x1b[33mwithout\x1b[39;49;00m\x1b[31m '
                        "\x1b[39;49;00m\x1b[33mcompleter\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m,\x1b[37m "
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33mnone\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]],\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[37m      '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33muser\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m,\x1b[37m        "
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33mTakes\x1b[39;49;00m\x1b[31m "
                        '\x1b[39;49;00m\x1b[33ma\x1b[39;49;00m\x1b[31m '
                        "\x1b[39;49;00m\x1b[33musername\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m,\x1b[37m "
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33muser\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]],\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[37m      '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33m*repeatable\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m,\x1b[37m "
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33mThis\x1b[39;49;00m\x1b[31m "
                        '\x1b[39;49;00m\x1b[33moption\x1b[39;49;00m\x1b[31m '
                        '\x1b[39;49;00m\x1b[33mis\x1b[39;49;00m\x1b[31m '
                        "\x1b[39;49;00m\x1b[33mrepeatable\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m,\x1b[37m "
                        '\x1b[39;49;00m\x1b[31mnull\x1b[39;49;00m],\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m      '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33mexclusive\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m,\x1b[37m   "
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33mThis\x1b[39;49;00m\x1b[31m "
                        '\x1b[39;49;00m\x1b[33moption\x1b[39;49;00m\x1b[31m '
                        '\x1b[39;49;00m\x1b[33mdisables\x1b[39;49;00m\x1b[31m '
                        '\x1b[39;49;00m\x1b[33mother\x1b[39;49;00m\x1b[31m '
                        "\x1b[39;49;00m\x1b[33moptions\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m,\x1b[37m "
                        '\x1b[39;49;00m\x1b[31mnull\x1b[39;49;00m,\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33mflag\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m,\x1b[37m "
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33mnodesc\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m,\x1b[37m "
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33mnocomp\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]],\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[37m      '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33mcheck\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m,\x1b[37m       "
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33mSpecify\x1b[39;49;00m\x1b[31m "
                        '\x1b[39;49;00m\x1b[33mfile\x1b[39;49;00m\x1b[31m '
                        '\x1b[39;49;00m\x1b[33mname\x1b[39;49;00m\x1b[31m '
                        "\x1b[39;49;00m\x1b[33mconversions\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m,\x1b[37m "
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33mchoices\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m,\x1b[37m "
                        '\x1b[39;49;00m{\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m        '
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33mrelaxed\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m:\x1b[37m "
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33mconvert\x1b[39;49;00m\x1b[31m "
                        '\x1b[39;49;00m\x1b[33mto\x1b[39;49;00m\x1b[31m '
                        '\x1b[39;49;00m\x1b[33mlowercase\x1b[39;49;00m\x1b[31m '
                        '\x1b[39;49;00m\x1b[33mbefore\x1b[39;49;00m\x1b[31m '
                        "\x1b[39;49;00m\x1b[33mlookup\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m,\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[37m        '
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33mstrict\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m:\x1b[37m "
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33mno\x1b[39;49;00m\x1b[31m "
                        "\x1b[39;49;00m\x1b[33mconversion\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[37m      '
                        '\x1b[39;49;00m}]]\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m    \x1b[39;49;00m]]\x1b[37m\x1b[39;49;00m\n',
  'implemented': None,
  'long': '`PAIR_SEPARATOR`:\n'
          '  The separator used to separate individual key-value pairs.\n'
          '\n'
          '`VALUE_SEPARATOR`:\n'
          '  The separator used to separate a key from its value.\n'
          '\n'
          '`DEFINITIONS`:\n'
          '  A list of key definitions.\n'
          '\n'
          '  Each definition has one of the following forms:\n'
          '\n'
          '  `[<KEY>, <DESCRIPTION>, <COMPLETER>]`\n'
          '  \n'
          '  -- OR --\n'
          '  \n'
          '  `[<KEY>, <DESCRIPTION>, <COMPLETER>, <EXCLUDES>]`\n'
          '  \n'
          '  `KEY`:\n'
          '    The name of the key.\n'
          '    Prefix the name with `*` to allow the key to be completed '
          'multiple times.\n'
          '\n'
          '  `DESCRIPTION`:\n'
          '    A description shown during completion.\n'
          '    Use `null` to omit the description.\n'
          '\n'
          '  `COMPLETER`:\n'
          '    The completer used for the value of the key.\n'
          '    Use `null` if the key does not take an argument.\n'
          "    Use `['none']` if the key takes an argument but cannot be "
          'completed.\n'
          '\n'
          '  `EXCLUDES`:\n'
          '    A list of keys that should no longer be offered for completion '
          'once this key has been used.\n'
          '\n'
          '`CONDITION_FUNCTION`:\n'
          '  A command or function that determines whether a key should be '
          'offered for\n'
          '  completion.\n'
          '\n'
          '  It is invoked with the key as its first argument. If it exits '
          'with status `0`,\n'
          '  the key is offered for completion. Any non-zero exit status '
          'suppresses the\n'
          '  key.\n'
          '\n'
          'By default, each key is offered for completion only once.\n'
          'To allow a key to be completed multiple times, prefix its name with '
          '`*`.\n',
  'long_colored': '\x1b[33m`PAIR_SEPARATOR`\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                  '  The separator used to separate individual key-value '
                  'pairs.\x1b[37m\x1b[39;49;00m\n'
                  '\n'
                  '\x1b[33m`VALUE_SEPARATOR`\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                  '  The separator used to separate a key from its '
                  'value.\x1b[37m\x1b[39;49;00m\n'
                  '\n'
                  '\x1b[33m`DEFINITIONS`\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                  '  A list of key definitions.\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m\x1b[39;49;00m\n'
                  '  Each definition has one of the following '
                  'forms:\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m\x1b[39;49;00m\n'
                  '  \x1b[33m`[<KEY>, <DESCRIPTION>, '
                  '<COMPLETER>]`\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n'
                  '  \x1b[37m\x1b[39;49;00m\n'
                  '  -- OR --\x1b[37m\x1b[39;49;00m\n'
                  '  \x1b[37m\x1b[39;49;00m\n'
                  '  \x1b[33m`[<KEY>, <DESCRIPTION>, <COMPLETER>, '
                  '<EXCLUDES>]`\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n'
                  '  \x1b[37m\x1b[39;49;00m\n'
                  '  \x1b[33m`KEY`\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                  '    The name of the key.\x1b[37m\x1b[39;49;00m\n'
                  '    Prefix the name with \x1b[33m`*`\x1b[39;49;00m to allow '
                  'the key to be completed multiple '
                  'times.\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m\x1b[39;49;00m\n'
                  '  '
                  '\x1b[33m`DESCRIPTION`\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                  '    A description shown during '
                  'completion.\x1b[37m\x1b[39;49;00m\n'
                  '    Use \x1b[33m`null`\x1b[39;49;00m to omit the '
                  'description.\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m\x1b[39;49;00m\n'
                  '  \x1b[33m`COMPLETER`\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                  '    The completer used for the value of the '
                  'key.\x1b[37m\x1b[39;49;00m\n'
                  '    Use \x1b[33m`null`\x1b[39;49;00m if the key does not '
                  'take an argument.\x1b[37m\x1b[39;49;00m\n'
                  "    Use \x1b[33m`['none']`\x1b[39;49;00m if the key takes "
                  'an argument but cannot be completed.\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m\x1b[39;49;00m\n'
                  '  \x1b[33m`EXCLUDES`\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                  '    A list of keys that should no longer be offered for '
                  'completion once this key has been '
                  'used.\x1b[37m\x1b[39;49;00m\n'
                  '\n'
                  '\x1b[33m`CONDITION_FUNCTION`\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                  '  A command or function that determines whether a key '
                  'should be offered for\x1b[37m\x1b[39;49;00m\n'
                  '  completion.\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m\x1b[39;49;00m\n'
                  '  It is invoked with the key as its first argument. If it '
                  'exits with status '
                  '\x1b[33m`0`\x1b[39;49;00m,\x1b[37m\x1b[39;49;00m\n'
                  '  the key is offered for completion. Any non-zero exit '
                  'status suppresses the\x1b[37m\x1b[39;49;00m\n'
                  '  key.\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m\x1b[39;49;00m\n'
                  'By default, each key is offered for completion only '
                  'once.\x1b[37m\x1b[39;49;00m\n'
                  'To allow a key to be completed multiple times, prefix its '
                  'name with '
                  '\x1b[33m`*`\x1b[39;49;00m.\x1b[37m\x1b[39;49;00m\n',
  'notes': [],
  'output': '~ > example --key-value-list flag,user=<TAB>\n'
            'bin                     braph\n'
            'colord                  dbus\n'
            'dhcpcd                  git\n'
            '[...]\n',
  'short': 'Complete comma-separated lists of key=value pairs'},
 {'also': {'key_value_list': 'For completing comma-separated lists of '
                             'key=value pairs'},
  'category': 'custom',
  'command': 'key_value_list_exec',
  'definition': "prog: 'example'\n"
                'options:\n'
                "  - option_strings: ['-o']\n"
                "    complete: ['key_value_list_exec', ',', '=', "
                "'_complete_key_value_list']\n",
  'definition_colored': '\x1b[94mprog\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33mexample\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[94moptions\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33m-o\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33mkey_value_list_exec\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m,\x1b[37m "
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33m,\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m,\x1b[37m "
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33m=\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m,\x1b[37m "
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33m_complete_key_value_list\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n",
  'implemented': None,
  'long': '`PAIR_SEPARATOR`:\n'
          '  The separator used to separate individual key-value pairs.\n'
          '\n'
          '`VALUE_SEPARATOR`:\n'
          '  The separator used to separate a key from its value.\n'
          '\n'
          '`COMMAND`:\n'
          '  The command or function used to generate the available keys and '
          'values.\n'
          '\n'
          '  If invoked without arguments, it must output the available keys '
          'in the\n'
          '  following format:\n'
          '\n'
          '  ```\n'
          '  [*]<KEY_1>[=][?]\\t<DESCRIPTION_1>\\t<EXCLUDES>\n'
          '  [*]<KEY_2>[=][?]\\t<DESCRIPTION_2>\\t<EXCLUDES>\n'
          '  [...]\n'
          '  ```\n'
          '\n'
          '  Prefixing a key with `*` marks it as repeatable.\n'
          '\n'
          '  Appending `=` to a key indicates that it requires a value.\n'
          '\n'
          '  Appending `=?` to a key indicates that it requires an optional '
          'value.\n'
          '\n'
          '  `EXCLUDES` is a space-separated list of keys that should no '
          'longer be\n'
          '  offered once the current key has been used.\n'
          '\n'
          '  If invoked with a single argument, the argument is the selected '
          'key.\n'
          '  The command must output the possible values for that key in the '
          'following\n'
          '  format:\n'
          '\n'
          '  ```\n'
          '  <ITEM_1>\\t<DESCRIPTION_1>\n'
          '  <ITEM_2>\\t<DESCRIPTION_2>\n'
          '  [...]\n'
          '  ```\n'
          '\n'
          '  Each line represents one completion candidate. The item and its '
          'description\n'
          '  are separated by a tab character.\n'
          '\n'
          'Example function:\n'
          '\n'
          '```sh\n'
          '_complete_key_value_list() {\n'
          '  if (( $# == 0 )); then\n'
          "    printf '%s\\t%s\\t%s\\n'                                 \\\n"
          "      'flag'        'option without an argument'       '' \\\n"
          "      'argument='   'option with an argument'          '' \\\n"
          "      'optional=?'  'option with an optional argument' '' \\\n"
          "      '*repeatable' 'a repeatable option'              '' \\\n"
          "      'excludes'    'disable options'                  'flag "
          "argument'\n"
          '  else\n'
          "    case '$1' in\n"
          '      argument|optional)\n'
          "        printf '%s\\t%s\\n'     \\\n"
          "          'foo' 'a foo value' \\\n"
          "          'bar' 'a bar value';;\n"
          '      esac\n'
          '  fi\n'
          '}\n'
          '```\n',
  'long_colored': '\x1b[33m`PAIR_SEPARATOR`\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                  '  The separator used to separate individual key-value '
                  'pairs.\x1b[37m\x1b[39;49;00m\n'
                  '\n'
                  '\x1b[33m`VALUE_SEPARATOR`\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                  '  The separator used to separate a key from its '
                  'value.\x1b[37m\x1b[39;49;00m\n'
                  '\n'
                  '\x1b[33m`COMMAND`\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                  '  The command or function used to generate the available '
                  'keys and values.\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m\x1b[39;49;00m\n'
                  '  If invoked without arguments, it must output the '
                  'available keys in the\x1b[37m\x1b[39;49;00m\n'
                  '  following format:\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[33m\x1b[39;49;00m\n'
                  '\x1b[33m  ```\x1b[39;49;00m\n'
                  '\x1b[33m  '
                  '[*]<KEY_1>[=][?]\\t<DESCRIPTION_1>\\t<EXCLUDES>\x1b[39;49;00m\n'
                  '\x1b[33m  '
                  '[*]<KEY_2>[=][?]\\t<DESCRIPTION_2>\\t<EXCLUDES>\x1b[39;49;00m\n'
                  '\x1b[33m  [...]\x1b[39;49;00m\n'
                  '\x1b[33m  ```\x1b[39;49;00m\n'
                  '\x1b[37m\x1b[39;49;00m\n'
                  '  Prefixing a key with \x1b[33m`*`\x1b[39;49;00m marks it '
                  'as repeatable.\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m\x1b[39;49;00m\n'
                  '  Appending \x1b[33m`=`\x1b[39;49;00m to a key indicates '
                  'that it requires a value.\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m\x1b[39;49;00m\n'
                  '  Appending \x1b[33m`=?`\x1b[39;49;00m to a key indicates '
                  'that it requires an optional value.\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m\x1b[39;49;00m\n'
                  '  \x1b[33m`EXCLUDES`\x1b[39;49;00m is a space-separated '
                  'list of keys that should no longer '
                  'be\x1b[37m\x1b[39;49;00m\n'
                  '  offered once the current key has been '
                  'used.\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m\x1b[39;49;00m\n'
                  '  If invoked with a single argument, the argument is the '
                  'selected key.\x1b[37m\x1b[39;49;00m\n'
                  '  The command must output the possible values for that key '
                  'in the following\x1b[37m\x1b[39;49;00m\n'
                  '  format:\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[33m\x1b[39;49;00m\n'
                  '\x1b[33m  ```\x1b[39;49;00m\n'
                  '\x1b[33m  <ITEM_1>\\t<DESCRIPTION_1>\x1b[39;49;00m\n'
                  '\x1b[33m  <ITEM_2>\\t<DESCRIPTION_2>\x1b[39;49;00m\n'
                  '\x1b[33m  [...]\x1b[39;49;00m\n'
                  '\x1b[33m  ```\x1b[39;49;00m\n'
                  '\x1b[37m\x1b[39;49;00m\n'
                  '  Each line represents one completion candidate. The item '
                  'and its description\x1b[37m\x1b[39;49;00m\n'
                  '  are separated by a tab character.\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m\x1b[39;49;00m\n'
                  'Example function:\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[33m\x1b[39;49;00m\n'
                  '\x1b[33m```\x1b[39;49;00m\x1b[33msh\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n'
                  '_complete_key_value_list()\x1b[37m '
                  '\x1b[39;49;00m{\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m  \x1b[39;49;00m\x1b[34mif\x1b[39;49;00m\x1b[37m '
                  '\x1b[39;49;00m((\x1b[37m '
                  '\x1b[39;49;00m\x1b[31m$#\x1b[39;49;00m\x1b[37m '
                  '\x1b[39;49;00m==\x1b[37m '
                  '\x1b[39;49;00m\x1b[34m0\x1b[39;49;00m\x1b[37m '
                  '\x1b[39;49;00m));\x1b[37m '
                  '\x1b[39;49;00m\x1b[34mthen\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m    '
                  '\x1b[39;49;00m\x1b[36mprintf\x1b[39;49;00m\x1b[37m '
                  "\x1b[39;49;00m\x1b[33m'%s\\t%s\\t%s\\n'\x1b[39;49;00m\x1b[37m                                 "
                  '\x1b[39;49;00m\x1b[33m\\\x1b[39;49;00m\n'
                  '\x1b[37m      '
                  "\x1b[39;49;00m\x1b[33m'flag'\x1b[39;49;00m\x1b[37m        "
                  "\x1b[39;49;00m\x1b[33m'option without an "
                  "argument'\x1b[39;49;00m\x1b[37m       "
                  "\x1b[39;49;00m\x1b[33m''\x1b[39;49;00m\x1b[37m "
                  '\x1b[39;49;00m\x1b[33m\\\x1b[39;49;00m\n'
                  '\x1b[37m      '
                  "\x1b[39;49;00m\x1b[33m'argument='\x1b[39;49;00m\x1b[37m   "
                  "\x1b[39;49;00m\x1b[33m'option with an "
                  "argument'\x1b[39;49;00m\x1b[37m          "
                  "\x1b[39;49;00m\x1b[33m''\x1b[39;49;00m\x1b[37m "
                  '\x1b[39;49;00m\x1b[33m\\\x1b[39;49;00m\n'
                  '\x1b[37m      '
                  "\x1b[39;49;00m\x1b[33m'optional=?'\x1b[39;49;00m\x1b[37m  "
                  "\x1b[39;49;00m\x1b[33m'option with an optional "
                  "argument'\x1b[39;49;00m\x1b[37m "
                  "\x1b[39;49;00m\x1b[33m''\x1b[39;49;00m\x1b[37m "
                  '\x1b[39;49;00m\x1b[33m\\\x1b[39;49;00m\n'
                  '\x1b[37m      '
                  "\x1b[39;49;00m\x1b[33m'*repeatable'\x1b[39;49;00m\x1b[37m "
                  "\x1b[39;49;00m\x1b[33m'a repeatable "
                  "option'\x1b[39;49;00m\x1b[37m              "
                  "\x1b[39;49;00m\x1b[33m''\x1b[39;49;00m\x1b[37m "
                  '\x1b[39;49;00m\x1b[33m\\\x1b[39;49;00m\n'
                  '\x1b[37m      '
                  "\x1b[39;49;00m\x1b[33m'excludes'\x1b[39;49;00m\x1b[37m    "
                  "\x1b[39;49;00m\x1b[33m'disable "
                  "options'\x1b[39;49;00m\x1b[37m                  "
                  "\x1b[39;49;00m\x1b[33m'flag "
                  "argument'\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n"
                  '\x1b[37m  '
                  '\x1b[39;49;00m\x1b[34melse\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m    '
                  '\x1b[39;49;00m\x1b[34mcase\x1b[39;49;00m\x1b[37m '
                  "\x1b[39;49;00m\x1b[33m'$1'\x1b[39;49;00m\x1b[37m "
                  '\x1b[39;49;00m\x1b[34min\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m      '
                  '\x1b[39;49;00margument|optional)\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m        '
                  '\x1b[39;49;00m\x1b[36mprintf\x1b[39;49;00m\x1b[37m '
                  "\x1b[39;49;00m\x1b[33m'%s\\t%s\\n'\x1b[39;49;00m\x1b[37m     "
                  '\x1b[39;49;00m\x1b[33m\\\x1b[39;49;00m\n'
                  '\x1b[37m          '
                  "\x1b[39;49;00m\x1b[33m'foo'\x1b[39;49;00m\x1b[37m "
                  "\x1b[39;49;00m\x1b[33m'a foo value'\x1b[39;49;00m\x1b[37m "
                  '\x1b[39;49;00m\x1b[33m\\\x1b[39;49;00m\n'
                  '\x1b[37m          '
                  "\x1b[39;49;00m\x1b[33m'bar'\x1b[39;49;00m\x1b[37m "
                  "\x1b[39;49;00m\x1b[33m'a bar "
                  "value'\x1b[39;49;00m;;\x1b[37m\x1b[39;49;00m\n"
                  '\x1b[37m      '
                  '\x1b[39;49;00m\x1b[34mesac\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m  '
                  '\x1b[39;49;00m\x1b[34mfi\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n'
                  '}\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[33m```\x1b[39;49;00m\n',
  'notes': ['Functions can be put inside a file and included with '
            '`--include-file`'],
  'output': '~ > example -o <TAB>\n'
            'argument      -- option with an argument\n'
            'excludes      -- disable options\n'
            'flag          -- option without an argument\n'
            'optional      -- option with an optional argument\n'
            'repeatable    -- a repeatable option\n'
            '\n'
            '~ > example -o argument=<TAB>\n'
            'foo    -- a foo value\n'
            'bar    -- a bar value\n'
            '\n'
            '~ > example -o excludes,<TAB>\n'
            'optional    -- option with an optional argument\n'
            'repeatable  -- a repeatable option\n',
  'short': 'Complete dynamically generated comma-separted lists of key=value '
           'pairs'},
 {'also': {'key_value_list': 'For completing comma-separated lists of '
                             'key=value pairs',
           'key_value_pair_exec': 'For completing single key=value pairs '
                                  '(dynamically generated by a function)'},
  'category': 'meta',
  'command': 'key_value_pair',
  'definition': "prog: 'example'\n"
                'options:\n'
                "  - option_strings: ['--key-value-pair']\n"
                "    complete: ['key_value_pair', '=', [\n"
                "      ['flag',   'An option flag', null],\n"
                "      ['nodesc', null, null],\n"
                "      ['nocomp', 'An option with arg but without completer', "
                "['none']],\n"
                "      ['user',   'Takes a username',  ['user']],\n"
                "      ['check',  'Specify file name conversions', ['choices', "
                '{\n'
                "        'relaxed': 'convert to lowercase before lookup',\n"
                "        'strict': 'no conversion'\n"
                '      }]]\n'
                '    ]]\n',
  'definition_colored': '\x1b[94mprog\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33mexample\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[94moptions\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33m--key-value-pair\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33mkey_value_pair\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m,\x1b[37m "
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33m=\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m,\x1b[37m "
                        '\x1b[39;49;00m[\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m      '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33mflag\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m,\x1b[37m   "
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33mAn\x1b[39;49;00m\x1b[31m "
                        '\x1b[39;49;00m\x1b[33moption\x1b[39;49;00m\x1b[31m '
                        "\x1b[39;49;00m\x1b[33mflag\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m,\x1b[37m "
                        '\x1b[39;49;00m\x1b[31mnull\x1b[39;49;00m],\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m      '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33mnodesc\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m,\x1b[37m "
                        '\x1b[39;49;00m\x1b[31mnull\x1b[39;49;00m,\x1b[37m '
                        '\x1b[39;49;00m\x1b[31mnull\x1b[39;49;00m],\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m      '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33mnocomp\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m,\x1b[37m "
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33mAn\x1b[39;49;00m\x1b[31m "
                        '\x1b[39;49;00m\x1b[33moption\x1b[39;49;00m\x1b[31m '
                        '\x1b[39;49;00m\x1b[33mwith\x1b[39;49;00m\x1b[31m '
                        '\x1b[39;49;00m\x1b[33marg\x1b[39;49;00m\x1b[31m '
                        '\x1b[39;49;00m\x1b[33mbut\x1b[39;49;00m\x1b[31m '
                        '\x1b[39;49;00m\x1b[33mwithout\x1b[39;49;00m\x1b[31m '
                        "\x1b[39;49;00m\x1b[33mcompleter\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m,\x1b[37m "
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33mnone\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]],\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[37m      '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33muser\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m,\x1b[37m   "
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33mTakes\x1b[39;49;00m\x1b[31m "
                        '\x1b[39;49;00m\x1b[33ma\x1b[39;49;00m\x1b[31m '
                        "\x1b[39;49;00m\x1b[33musername\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m,\x1b[37m  "
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33muser\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]],\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[37m      '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33mcheck\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m,\x1b[37m  "
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33mSpecify\x1b[39;49;00m\x1b[31m "
                        '\x1b[39;49;00m\x1b[33mfile\x1b[39;49;00m\x1b[31m '
                        '\x1b[39;49;00m\x1b[33mname\x1b[39;49;00m\x1b[31m '
                        "\x1b[39;49;00m\x1b[33mconversions\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m,\x1b[37m "
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33mchoices\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m,\x1b[37m "
                        '\x1b[39;49;00m{\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m        '
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33mrelaxed\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m:\x1b[37m "
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33mconvert\x1b[39;49;00m\x1b[31m "
                        '\x1b[39;49;00m\x1b[33mto\x1b[39;49;00m\x1b[31m '
                        '\x1b[39;49;00m\x1b[33mlowercase\x1b[39;49;00m\x1b[31m '
                        '\x1b[39;49;00m\x1b[33mbefore\x1b[39;49;00m\x1b[31m '
                        "\x1b[39;49;00m\x1b[33mlookup\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m,\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[37m        '
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33mstrict\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m:\x1b[37m "
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33mno\x1b[39;49;00m\x1b[31m "
                        "\x1b[39;49;00m\x1b[33mconversion\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[37m      '
                        '\x1b[39;49;00m}]]\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m    \x1b[39;49;00m]]\x1b[37m\x1b[39;49;00m\n',
  'implemented': None,
  'long': '`VALUE_SEPARATOR`:\n'
          '  The separator used to separate a key from its value.\n'
          '\n'
          '`DEFINITIONS`:\n'
          '  A list of key definitions.\n'
          '\n'
          '  Each definition has the following form:\n'
          '\n'
          '  `[<KEY>, <DESCRIPTION>, <COMPLETER>]`\n'
          '\n'
          '  `KEY`:\n'
          '    The name of the key.\n'
          '    Prefix the name with `*` to allow the key to be completed '
          'multiple times.\n'
          '\n'
          '  `DESCRIPTION`:\n'
          '    A description shown during completion.\n'
          '    Use `null` to omit the description.\n'
          '\n'
          '  `COMPLETER`:\n'
          '    The completer used for the value of the key.\n'
          '    Use `null` if the key does not take an argument.\n'
          "    Use `['none']` if the key takes an argument but cannot be "
          'completed.\n'
          '\n'
          '`CONDITION_FUNCTION`:\n'
          '  A command or function that determines whether a key should be '
          'offered for\n'
          '  completion.\n'
          '\n'
          '  It is invoked with the key as its first argument. If it exits '
          'with status `0`,\n'
          '  the key is offered for completion. Any non-zero exit status '
          'suppresses the\n'
          '  key.\n',
  'long_colored': '\x1b[33m`VALUE_SEPARATOR`\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                  '  The separator used to separate a key from its '
                  'value.\x1b[37m\x1b[39;49;00m\n'
                  '\n'
                  '\x1b[33m`DEFINITIONS`\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                  '  A list of key definitions.\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m\x1b[39;49;00m\n'
                  '  Each definition has the following '
                  'form:\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m\x1b[39;49;00m\n'
                  '  \x1b[33m`[<KEY>, <DESCRIPTION>, '
                  '<COMPLETER>]`\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m\x1b[39;49;00m\n'
                  '  \x1b[33m`KEY`\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                  '    The name of the key.\x1b[37m\x1b[39;49;00m\n'
                  '    Prefix the name with \x1b[33m`*`\x1b[39;49;00m to allow '
                  'the key to be completed multiple '
                  'times.\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m\x1b[39;49;00m\n'
                  '  '
                  '\x1b[33m`DESCRIPTION`\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                  '    A description shown during '
                  'completion.\x1b[37m\x1b[39;49;00m\n'
                  '    Use \x1b[33m`null`\x1b[39;49;00m to omit the '
                  'description.\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m\x1b[39;49;00m\n'
                  '  \x1b[33m`COMPLETER`\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                  '    The completer used for the value of the '
                  'key.\x1b[37m\x1b[39;49;00m\n'
                  '    Use \x1b[33m`null`\x1b[39;49;00m if the key does not '
                  'take an argument.\x1b[37m\x1b[39;49;00m\n'
                  "    Use \x1b[33m`['none']`\x1b[39;49;00m if the key takes "
                  'an argument but cannot be completed.\x1b[37m\x1b[39;49;00m\n'
                  '\n'
                  '\x1b[33m`CONDITION_FUNCTION`\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                  '  A command or function that determines whether a key '
                  'should be offered for\x1b[37m\x1b[39;49;00m\n'
                  '  completion.\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m\x1b[39;49;00m\n'
                  '  It is invoked with the key as its first argument. If it '
                  'exits with status '
                  '\x1b[33m`0`\x1b[39;49;00m,\x1b[37m\x1b[39;49;00m\n'
                  '  the key is offered for completion. Any non-zero exit '
                  'status suppresses the\x1b[37m\x1b[39;49;00m\n'
                  '  key.\x1b[37m\x1b[39;49;00m\n',
  'notes': [],
  'output': '~ > example --key-value-pair <TAB>\n'
            'check     -- Specify file name conversions\n'
            'flag      -- An option flag\n'
            'nocomp    -- An option with arg but without completer\n'
            'user      -- Takes a username\n'
            'nodesc\n'
            '\n'
            '~ > example --key-value-pair user=<TAB>\n'
            'bin        braph\n'
            'colord     dbus\n'
            'dhcpcd     git\n'
            '[...]\n',
  'short': 'Complete single key=value pairs'},
 {'also': {'key_value_pair': 'For completing single key=value pairs'},
  'category': 'custom',
  'command': 'key_value_pair_exec',
  'definition': "prog: 'example'\n"
                'options:\n'
                "  - option_strings: ['-o']\n"
                "    complete: ['key_value_pair_exec', '=', "
                "'_complete_key_value_pair']\n",
  'definition_colored': '\x1b[94mprog\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33mexample\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[94moptions\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33m-o\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33mkey_value_pair_exec\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m,\x1b[37m "
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33m=\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m,\x1b[37m "
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33m_complete_key_value_pair\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n",
  'implemented': None,
  'long': '`VALUE_SEPARATOR`:\n'
          '  The separator used to separate a key from its value.\n'
          '\n'
          '`COMMAND`:\n'
          '  The command or function used to generate the available keys and '
          'values.\n'
          '\n'
          '  If invoked without arguments, it must output the available keys '
          'in the\n'
          '  following format:\n'
          '\n'
          '  ```\n'
          '  <KEY_1>[=]\\t<DESCRIPTION_1>\n'
          '  <KEY_2>[=]\\t<DESCRIPTION_2>\n'
          '  [...]\n'
          '  ```\n'
          '\n'
          '  Appending `=` to a key indicates that it requires a value.\n'
          '\n'
          '  If invoked with a single argument, the argument is the selected '
          'key. The\n'
          '  command must output the possible values for that key in the '
          'following\n'
          '  format:\n'
          '\n'
          '  ```\n'
          '  <ITEM_1>\\t<DESCRIPTION_1>\n'
          '  <ITEM_2>\\t<DESCRIPTION_2>\n'
          '  [...]\n'
          '  ```\n'
          '\n'
          '  Each line represents one completion candidate. The item and its '
          'description\n'
          '  are separated by a tab character.\n'
          '\n'
          'Example function:\n'
          '\n'
          '```sh\n'
          '_complete_key_value_pair() {\n'
          '  if (( $# == 0 )); then\n'
          "    printf '%s\\t%s\\n'    \\\n"
          "      'flag'    'a flag' \\\n"
          "      'option=' 'option with value'\n"
          '  else\n'
          "    case '$1' in\n"
          '      option)\n'
          "        printf '%s\\t%s\\n'     \\\n"
          "          'foo' 'a foo value' \\\n"
          "          'bar' 'a bar value';;\n"
          '      esac\n'
          '  fi\n'
          '}\n'
          '```\n',
  'long_colored': '\x1b[33m`VALUE_SEPARATOR`\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                  '  The separator used to separate a key from its '
                  'value.\x1b[37m\x1b[39;49;00m\n'
                  '\n'
                  '\x1b[33m`COMMAND`\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                  '  The command or function used to generate the available '
                  'keys and values.\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m\x1b[39;49;00m\n'
                  '  If invoked without arguments, it must output the '
                  'available keys in the\x1b[37m\x1b[39;49;00m\n'
                  '  following format:\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[33m\x1b[39;49;00m\n'
                  '\x1b[33m  ```\x1b[39;49;00m\n'
                  '\x1b[33m  <KEY_1>[=]\\t<DESCRIPTION_1>\x1b[39;49;00m\n'
                  '\x1b[33m  <KEY_2>[=]\\t<DESCRIPTION_2>\x1b[39;49;00m\n'
                  '\x1b[33m  [...]\x1b[39;49;00m\n'
                  '\x1b[33m  ```\x1b[39;49;00m\n'
                  '\x1b[37m\x1b[39;49;00m\n'
                  '  Appending \x1b[33m`=`\x1b[39;49;00m to a key indicates '
                  'that it requires a value.\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m\x1b[39;49;00m\n'
                  '  If invoked with a single argument, the argument is the '
                  'selected key. The\x1b[37m\x1b[39;49;00m\n'
                  '  command must output the possible values for that key in '
                  'the following\x1b[37m\x1b[39;49;00m\n'
                  '  format:\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[33m\x1b[39;49;00m\n'
                  '\x1b[33m  ```\x1b[39;49;00m\n'
                  '\x1b[33m  <ITEM_1>\\t<DESCRIPTION_1>\x1b[39;49;00m\n'
                  '\x1b[33m  <ITEM_2>\\t<DESCRIPTION_2>\x1b[39;49;00m\n'
                  '\x1b[33m  [...]\x1b[39;49;00m\n'
                  '\x1b[33m  ```\x1b[39;49;00m\n'
                  '\x1b[37m\x1b[39;49;00m\n'
                  '  Each line represents one completion candidate. The item '
                  'and its description\x1b[37m\x1b[39;49;00m\n'
                  '  are separated by a tab character.\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m\x1b[39;49;00m\n'
                  'Example function:\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[33m\x1b[39;49;00m\n'
                  '\x1b[33m```\x1b[39;49;00m\x1b[33msh\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n'
                  '_complete_key_value_pair()\x1b[37m '
                  '\x1b[39;49;00m{\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m  \x1b[39;49;00m\x1b[34mif\x1b[39;49;00m\x1b[37m '
                  '\x1b[39;49;00m((\x1b[37m '
                  '\x1b[39;49;00m\x1b[31m$#\x1b[39;49;00m\x1b[37m '
                  '\x1b[39;49;00m==\x1b[37m '
                  '\x1b[39;49;00m\x1b[34m0\x1b[39;49;00m\x1b[37m '
                  '\x1b[39;49;00m));\x1b[37m '
                  '\x1b[39;49;00m\x1b[34mthen\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m    '
                  '\x1b[39;49;00m\x1b[36mprintf\x1b[39;49;00m\x1b[37m '
                  "\x1b[39;49;00m\x1b[33m'%s\\t%s\\n'\x1b[39;49;00m\x1b[37m    "
                  '\x1b[39;49;00m\x1b[33m\\\x1b[39;49;00m\n'
                  '\x1b[37m      '
                  "\x1b[39;49;00m\x1b[33m'flag'\x1b[39;49;00m\x1b[37m    "
                  "\x1b[39;49;00m\x1b[33m'a flag'\x1b[39;49;00m\x1b[37m "
                  '\x1b[39;49;00m\x1b[33m\\\x1b[39;49;00m\n'
                  '\x1b[37m      '
                  "\x1b[39;49;00m\x1b[33m'option='\x1b[39;49;00m\x1b[37m "
                  "\x1b[39;49;00m\x1b[33m'option with "
                  "value'\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n"
                  '\x1b[37m  '
                  '\x1b[39;49;00m\x1b[34melse\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m    '
                  '\x1b[39;49;00m\x1b[34mcase\x1b[39;49;00m\x1b[37m '
                  "\x1b[39;49;00m\x1b[33m'$1'\x1b[39;49;00m\x1b[37m "
                  '\x1b[39;49;00m\x1b[34min\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m      \x1b[39;49;00moption)\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m        '
                  '\x1b[39;49;00m\x1b[36mprintf\x1b[39;49;00m\x1b[37m '
                  "\x1b[39;49;00m\x1b[33m'%s\\t%s\\n'\x1b[39;49;00m\x1b[37m     "
                  '\x1b[39;49;00m\x1b[33m\\\x1b[39;49;00m\n'
                  '\x1b[37m          '
                  "\x1b[39;49;00m\x1b[33m'foo'\x1b[39;49;00m\x1b[37m "
                  "\x1b[39;49;00m\x1b[33m'a foo value'\x1b[39;49;00m\x1b[37m "
                  '\x1b[39;49;00m\x1b[33m\\\x1b[39;49;00m\n'
                  '\x1b[37m          '
                  "\x1b[39;49;00m\x1b[33m'bar'\x1b[39;49;00m\x1b[37m "
                  "\x1b[39;49;00m\x1b[33m'a bar "
                  "value'\x1b[39;49;00m;;\x1b[37m\x1b[39;49;00m\n"
                  '\x1b[37m      '
                  '\x1b[39;49;00m\x1b[34mesac\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m  '
                  '\x1b[39;49;00m\x1b[34mfi\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n'
                  '}\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[33m```\x1b[39;49;00m\n',
  'notes': ['Functions can be put inside a file and included with '
            '`--include-file`'],
  'output': '~ > example -o <TAB>\n'
            'flag    -- a flag\n'
            'option  -- option with value\n'
            '\n'
            '~ > example -o option=<TAB>\n'
            'foo     -- a foo value\n'
            'bar     -- a bar value\n',
  'short': 'Complete dynamically generated a key=value pairs'},
 {'also': {'directory_list': 'For completing comma-separated lists of '
                             'directories',
           'file_list': 'For completing comma-separated lists of files',
           'key_value_list': 'For completing comma-separated lists of '
                             'key=value pairs',
           'value_list': 'For completing comma-separated lists of values'},
  'category': 'meta',
  'command': 'list',
  'definition': "prog: 'example'\n"
                'options:\n'
                "  - option_strings: ['--user-list']\n"
                "    complete: ['list', ['user']]\n"
                '\n'
                "  - option_strings: ['--option-list']\n"
                "    complete: ['list', ['choices', ['setuid', 'async', "
                "'block']], {'separator': ':', 'duplicates': true}]\n",
  'definition_colored': '\x1b[94mprog\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33mexample\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[94moptions\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33m--user-list\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33mlist\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m,\x1b[37m "
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33muser\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]]\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33m--option-list\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33mlist\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m,\x1b[37m "
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33mchoices\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m,\x1b[37m "
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33msetuid\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m,\x1b[37m "
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33masync\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m,\x1b[37m "
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33mblock\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]],\x1b[37m "
                        "\x1b[39;49;00m{\x1b[33m'\x1b[39;49;00m\x1b[33mseparator\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m:\x1b[37m "
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33m:\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m,\x1b[37m "
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33mduplicates\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m:\x1b[37m "
                        '\x1b[39;49;00m\x1b[31mtrue\x1b[39;49;00m}]\x1b[37m\x1b[39;49;00m\n',
  'implemented': None,
  'long': '`COMPLETER`:\n'
          '  The completer used to generate the list elements.\n'
          '\n'
          '`OPTIONS`:\n'
          '  A dictionary containing additional options for configuring the '
          'list completion.\n'
          '\n'
          '  - `separator`: The separator used between list elements. Defaults '
          'to `,`\n'
          '\n'
          '  - `duplicates`: Allow duplicate values to be offered for '
          'completion. Defaults to `false`\n',
  'long_colored': '\x1b[33m`COMPLETER`\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                  '  The completer used to generate the list '
                  'elements.\x1b[37m\x1b[39;49;00m\n'
                  '\n'
                  '\x1b[33m`OPTIONS`\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                  '  A dictionary containing additional options for '
                  'configuring the list completion.\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m  \x1b[39;49;00m\x1b[34m-\x1b[39;49;00m\x1b[37m '
                  '\x1b[39;49;00m\x1b[33m`separator`\x1b[39;49;00m: The '
                  'separator used between list elements. Defaults to '
                  '\x1b[33m`,`\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m  \x1b[39;49;00m\x1b[34m-\x1b[39;49;00m\x1b[37m '
                  '\x1b[39;49;00m\x1b[33m`duplicates`\x1b[39;49;00m: Allow '
                  'duplicate values to be offered for completion. Defaults to '
                  '\x1b[33m`false`\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n',
  'notes': [],
  'output': '~ > example --user-list=avahi,daemon,<TAB>\n'
            'bin       braph\n'
            'colord    dbus\n'
            'dhcpcd    git\n'
            '[...]\n'
            '\n'
            '~ > example --option-list=setuid:<TAB>\n'
            'setuid     async    block\n',
  'short': 'Complete comma-separated lists using a completer'},
 {'also': None,
  'category': 'bonus',
  'command': 'locale',
  'definition': "prog: 'example'\n"
                'options:\n'
                "  - option_strings: ['--locale']\n"
                "    complete: ['locale']\n",
  'definition_colored': '\x1b[94mprog\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33mexample\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[94moptions\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33m--locale\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33mlocale\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n",
  'implemented': None,
  'long': None,
  'long_colored': None,
  'notes': [],
  'output': '~ > example --locale=<TAB>\n'
            'C  C.UTF-8  de_DE  de_DE@euro  de_DE.iso88591  '
            'de_DE.iso885915@euro\n'
            'de_DE.UTF-8  deutsch  en_US  en_US.iso88591  en_US.UTF-8  german  '
            'POSIX\n',
  'short': 'Complete locales'},
 {'also': None,
  'category': 'bonus',
  'command': 'login_shell',
  'definition': "prog: 'example'\n"
                'options:\n'
                "  - option_strings: ['--login-shell']\n"
                "    complete: ['login_shell']\n",
  'definition_colored': '\x1b[94mprog\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33mexample\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[94moptions\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33m--login-shell\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33mlogin_shell\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n",
  'implemented': None,
  'long': None,
  'long_colored': None,
  'notes': [],
  'output': '~ > example --login-shell=<TAB>\n'
            '/bin/bash   /bin/sh         /usr/bin/fish       /usr/bin/sh\n'
            '[...]\n',
  'short': 'Complete login shells'},
 {'also': None,
  'category': 'basic',
  'command': 'mime_file',
  'definition': "prog: 'example'\n"
                'options:\n'
                "  - option_strings: ['--image']\n"
                "    complete: ['mime_file', 'image/']\n",
  'definition_colored': '\x1b[94mprog\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33mexample\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[94moptions\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33m--image\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33mmime_file\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m,\x1b[37m "
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33mimage/\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n",
  'implemented': None,
  'long': '`MIME_REGEX`:\n'
          '  An extended regular expression used to match MIME types.\n'
          '  The expression is passed to `grep -E` to filter the results.\n',
  'long_colored': '\x1b[33m`MIME_REGEX`\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                  '  An extended regular expression used to match MIME '
                  'types.\x1b[37m\x1b[39;49;00m\n'
                  '  The expression is passed to \x1b[33m`grep '
                  '-E`\x1b[39;49;00m to filter the '
                  'results.\x1b[37m\x1b[39;49;00m\n',
  'notes': [],
  'output': '~ > example --image=<TAB>\ndir1/  dir2/  img.png  img.jpg\n',
  'short': 'Complete files by MIME type'},
 {'also': None,
  'category': 'bonus',
  'command': 'mountpoint',
  'definition': "prog: 'example'\n"
                'options:\n'
                "  - option_strings: ['--mountpoint']\n"
                "    complete: ['mountpoint']\n",
  'definition_colored': '\x1b[94mprog\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33mexample\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[94moptions\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33m--mountpoint\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33mmountpoint\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n",
  'implemented': None,
  'long': None,
  'long_colored': None,
  'notes': [],
  'output': '~ > example --mountpoint=<TAB>\n'
            '/  /boot  /home  /proc  /run  /sys  /tmp\n'
            '[...]\n',
  'short': 'Complete mount points'},
 {'also': {'ip_address': 'For completing IP addresses'},
  'category': 'bonus',
  'command': 'net_interface',
  'definition': "prog: 'example'\n"
                'options:\n'
                "  - option_strings: ['--net-interface']\n"
                "    complete: ['net_interface']\n",
  'definition_colored': '\x1b[94mprog\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33mexample\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[94moptions\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33m--net-interface\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33mnet_interface\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n",
  'implemented': None,
  'long': None,
  'long_colored': None,
  'notes': [],
  'output': '~ > example --net-interface=<TAB>\n'
            'eno1  enp1s0  lo  wlo1  wlp2s0\n'
            '[...]\n',
  'short': 'Complete network interfaces'},
 {'also': None,
  'category': 'meta',
  'command': 'none',
  'definition': "prog: 'example'\n"
                'options:\n'
                "  - option_strings: ['--none']\n"
                "    complete: ['none']\n",
  'definition_colored': '\x1b[94mprog\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33mexample\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[94moptions\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33m--none\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33mnone\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n",
  'implemented': None,
  'long': 'Disables autocompletion for an option but still marks it as '
          'requiring an argument.\n'
          '\n'
          'Without specifying `complete`, the option would not take an '
          'argument.\n',
  'long_colored': 'Disables autocompletion for an option but still marks it as '
                  'requiring an argument.\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m\x1b[39;49;00m\n'
                  'Without specifying \x1b[33m`complete`\x1b[39;49;00m, the '
                  'option would not take an argument.\x1b[37m\x1b[39;49;00m\n',
  'notes': [],
  'output': '~ > example --none=<TAB>\n<NO OUTPUT>\n',
  'short': 'No completion, but specify that an argument is required'},
 {'also': {'process': 'For completing process names'},
  'category': 'basic',
  'command': 'pid',
  'definition': "prog: 'example'\n"
                'options:\n'
                "  - option_strings: ['--pid']\n"
                "    complete: ['pid']\n",
  'definition_colored': '\x1b[94mprog\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33mexample\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[94moptions\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33m--pid\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33mpid\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n",
  'implemented': None,
  'long': None,
  'long_colored': None,
  'notes': [],
  'output': '~ > example --pid=<TAB>\n'
            '1       13      166     19      254     31      45\n'
            '1006    133315  166441  19042   26      32      46\n'
            '10150   1392    166442  195962  27      33      4609\n',
  'short': 'Complete process IDs'},
 {'also': None,
  'category': 'meta',
  'command': 'prefix',
  'definition': "prog: 'example'\n"
                'options:\n'
                "  - option_strings: ['--prefix']\n"
                "    complete: ['prefix', 'input:', ['file']]\n",
  'definition_colored': '\x1b[94mprog\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33mexample\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[94moptions\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33m--prefix\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33mprefix\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m,\x1b[37m "
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33minput:\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m,\x1b[37m "
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33mfile\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]]\x1b[37m\x1b[39;49;00m\n",
  'implemented': None,
  'long': '`PREFIX`:\n'
          '  The string to prepend to each completion candidate.\n'
          '\n'
          '`COMPLETER`:\n'
          '  The completer used to generate the completion candidates.\n',
  'long_colored': '\x1b[33m`PREFIX`\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                  '  The string to prepend to each completion '
                  'candidate.\x1b[37m\x1b[39;49;00m\n'
                  '\n'
                  '\x1b[33m`COMPLETER`\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                  '  The completer used to generate the completion '
                  'candidates.\x1b[37m\x1b[39;49;00m\n',
  'notes': [],
  'output': '~ > example --prefix=<TAB>\n'
            '~ > example --prefix=input:\n'
            '\n'
            '~ > example --prefix=input:<TAB>\n'
            '~ > example --prefix=input:file1.txt\n',
  'short': 'Prefix completions with a string'},
 {'also': {'pid': 'For completing process IDs'},
  'category': 'basic',
  'command': 'process',
  'definition': "prog: 'example'\n"
                'options:\n'
                "  - option_strings: ['--process']\n"
                "    complete: ['process']\n",
  'definition_colored': '\x1b[94mprog\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33mexample\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[94moptions\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33m--process\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33mprocess\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n",
  'implemented': None,
  'long': None,
  'long_colored': None,
  'notes': [],
  'output': '~ > example --process=s<TAB>\n'
            'scsi_eh_0         scsi_eh_1       scsi_eh_2      scsi_eh_3  '
            'scsi_eh_4\n'
            'scsi_eh_5         sh              sudo           syndaemon  '
            'systemd\n'
            'systemd-journald  systemd-logind  systemd-udevd\n',
  'short': 'Complete process names'},
 {'also': None,
  'category': 'basic',
  'command': 'range',
  'definition': "prog: 'example'\n"
                'options:\n'
                "  - option_strings: ['--range-1']\n"
                "    complete: ['range', 1, 9]\n"
                '\n'
                "  - option_strings: ['--range-2']\n"
                "    complete: ['range', 1, 9, 2]\n",
  'definition_colored': '\x1b[94mprog\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33mexample\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[94moptions\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33m--range-1\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33mrange\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m,\x1b[37m "
                        '\x1b[39;49;00m\x1b[31m1\x1b[39;49;00m,\x1b[37m '
                        '\x1b[39;49;00m\x1b[31m9\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33m--range-2\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33mrange\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m,\x1b[37m "
                        '\x1b[39;49;00m\x1b[31m1\x1b[39;49;00m,\x1b[37m '
                        '\x1b[39;49;00m\x1b[31m9\x1b[39;49;00m,\x1b[37m '
                        '\x1b[39;49;00m\x1b[31m2\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n',
  'implemented': None,
  'long': '`START`:\n'
          '  The first value of the range.\n'
          '\n'
          '`STOP`:\n'
          '  The last value of the range.\n'
          '\n'
          '`STEP`:\n'
          '  The increment between values. Defaults to `1`.\n',
  'long_colored': '\x1b[33m`START`\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                  '  The first value of the range.\x1b[37m\x1b[39;49;00m\n'
                  '\n'
                  '\x1b[33m`STOP`\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                  '  The last value of the range.\x1b[37m\x1b[39;49;00m\n'
                  '\n'
                  '\x1b[33m`STEP`\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                  '  The increment between values. Defaults to '
                  '\x1b[33m`1`\x1b[39;49;00m.\x1b[37m\x1b[39;49;00m\n',
  'notes': [],
  'output': '~ > example --range-1=<TAB>\n'
            '1  2  3  4  5  6  7  8  9\n'
            '\n'
            '~ > example --range-2=<TAB>\n'
            '1  3  5  7  9\n',
  'short': 'Complete sequences of integers'},
 {'also': None,
  'category': 'basic',
  'command': 'service',
  'definition': "prog: 'example'\n"
                'options:\n'
                "  - option_strings: ['--service']\n"
                "    complete: ['service']\n",
  'definition_colored': '\x1b[94mprog\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33mexample\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[94moptions\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33m--service\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33mservice\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n",
  'implemented': None,
  'long': None,
  'long_colored': None,
  'notes': [],
  'output': '~ > example --service=<TAB>\nTODO\n[...]\n',
  'short': 'Complete systemd service names'},
 {'also': None,
  'category': 'basic',
  'command': 'signal',
  'definition': "prog: 'example'\n"
                'options:\n'
                "  - option_strings: ['--signal']\n"
                "    complete: ['signal']\n",
  'definition_colored': '\x1b[94mprog\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33mexample\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[94moptions\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33m--signal\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33msignal\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n",
  'implemented': None,
  'long': None,
  'long_colored': None,
  'notes': [],
  'output': '~ > example --signal=<TAB>\n'
            'ABRT    -- Process abort signal\n'
            'ALRM    -- Alarm clock\n'
            'BUS     -- Access to an undefined portion of a memory object\n'
            'CHLD    -- Child process terminated, stopped, or continued\n'
            'CONT    -- Continue executing, if stopped\n'
            'FPE     -- Erroneous arithmetic operation\n'
            'HUP     -- Hangup\n'
            'ILL     -- Illegal instruction\n'
            'INT     -- Terminal interrupt signal\n'
            '[...]\n',
  'short': 'Complete signal names'},
 {'also': None,
  'category': 'bonus',
  'command': 'timezone',
  'definition': "prog: 'example'\n"
                'options:\n'
                "  - option_strings: ['--timezone']\n"
                "    complete: ['timezone']\n",
  'definition_colored': '\x1b[94mprog\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33mexample\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[94moptions\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33m--timezone\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33mtimezone\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n",
  'implemented': None,
  'long': None,
  'long_colored': None,
  'notes': [],
  'output': '~ > example --timezone=Europe/B<TAB>\n'
            'Belfast     Belgrade    Berlin      Bratislava\n'
            'Brussels    Bucharest   Budapest    Busingen\n',
  'short': 'Complete timezones'},
 {'also': {'user': 'For completing user names'},
  'category': 'basic',
  'command': 'uid',
  'definition': "prog: 'example'\n"
                'options:\n'
                "  - option_strings: ['--uid']\n"
                "    complete: ['uid']\n",
  'definition_colored': '\x1b[94mprog\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33mexample\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[94moptions\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33m--uid\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33muid\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n",
  'implemented': None,
  'long': None,
  'long_colored': None,
  'notes': [],
  'output': '~ > example --uid=<TAB>\n'
            '0      -- root\n'
            '1000   -- braph\n'
            '102    -- polkitd\n'
            '133    -- rtkit\n'
            '14     -- ftp\n'
            '1      -- bin\n'
            '2      -- daemon\n'
            '33     -- http\n'
            '65534  -- nobody\n'
            '[...]\n',
  'short': 'Complete user IDs'},
 {'also': {'uid': 'For completing user IDs'},
  'category': 'basic',
  'command': 'user',
  'definition': "prog: 'example'\n"
                'options:\n'
                "  - option_strings: ['--user']\n"
                "    complete: ['user']\n",
  'definition_colored': '\x1b[94mprog\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33mexample\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[94moptions\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33m--user\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33muser\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n",
  'implemented': None,
  'long': None,
  'long_colored': None,
  'notes': [],
  'output': '~ > example --user=<TAB>\n'
            'avahi         bin          braph\n'
            'colord        daemon       dbus\n'
            'dhcpcd        ftp          git\n'
            '[...]\n',
  'short': 'Complete user names'},
 {'also': {'key_value_list': 'For completing comma-separated lists of '
                             'key=value pairs',
           'list': 'For completing comma-separated lists using a completer'},
  'category': 'basic',
  'command': 'value_list',
  'definition': "prog: 'example'\n"
                'options:\n'
                "  - option_strings: ['--value-list-1']\n"
                "    complete: ['value_list', {'values': ['exec', 'noexec']}]\n"
                '\n'
                "  - option_strings: ['--value-list-2']\n"
                "    complete: ['value_list', {'values': {'one': 'Description "
                "1', 'two': 'Description 2'}}]\n",
  'definition_colored': '\x1b[94mprog\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33mexample\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[94moptions\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33m--value-list-1\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33mvalue_list\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m,\x1b[37m "
                        "\x1b[39;49;00m{\x1b[33m'\x1b[39;49;00m\x1b[33mvalues\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m:\x1b[37m "
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33mexec\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m,\x1b[37m "
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33mnoexec\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]}]\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33m--value-list-2\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33mvalue_list\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m,\x1b[37m "
                        "\x1b[39;49;00m{\x1b[33m'\x1b[39;49;00m\x1b[33mvalues\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m:\x1b[37m "
                        "\x1b[39;49;00m{\x1b[33m'\x1b[39;49;00m\x1b[33mone\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m:\x1b[37m "
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33mDescription\x1b[39;49;00m\x1b[31m "
                        "\x1b[39;49;00m\x1b[33m1\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m,\x1b[37m "
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33mtwo\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m:\x1b[37m "
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33mDescription\x1b[39;49;00m\x1b[31m "
                        "\x1b[39;49;00m\x1b[33m2\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m}}]\x1b[37m\x1b[39;49;00m\n",
  'implemented': None,
  'long': '`OPTIONS`:\n'
          '  A dictionary containing additional options for configuring the '
          'completion.\n'
          '\n'
          '  - `values`:\n'
          '    A list or dictionary containing the values to offer for '
          'completion.\n'
          '\n'
          '    If a list is supplied, all values are offered without '
          'descriptions.\n'
          '\n'
          '    If a dictionary is supplied, the keys are used as completion '
          'values and\n'
          '    the values are used as descriptions.\n'
          '\n'
          '  - `separator`:\n'
          '    The separator used between list elements. Defaults to `,`.\n'
          '\n'
          '  - `duplicates`:\n'
          '    Allow duplicate values to be offered for completion. Defaults '
          'to `false`.\n',
  'long_colored': '\x1b[33m`OPTIONS`\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                  '  A dictionary containing additional options for '
                  'configuring the completion.\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m  \x1b[39;49;00m\x1b[34m-\x1b[39;49;00m\x1b[37m '
                  '\x1b[39;49;00m\x1b[33m`values`\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                  '    A list or dictionary containing the values to offer for '
                  'completion.\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m\x1b[39;49;00m\n'
                  '    If a list is supplied, all values are offered without '
                  'descriptions.\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m\x1b[39;49;00m\n'
                  '    If a dictionary is supplied, the keys are used as '
                  'completion values and\x1b[37m\x1b[39;49;00m\n'
                  '    the values are used as '
                  'descriptions.\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m  \x1b[39;49;00m\x1b[34m-\x1b[39;49;00m\x1b[37m '
                  '\x1b[39;49;00m\x1b[33m`separator`\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                  '    The separator used between list elements. Defaults to '
                  '\x1b[33m`,`\x1b[39;49;00m.\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m  \x1b[39;49;00m\x1b[34m-\x1b[39;49;00m\x1b[37m '
                  '\x1b[39;49;00m\x1b[33m`duplicates`\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                  '    Allow duplicate values to be offered for completion. '
                  'Defaults to '
                  '\x1b[33m`false`\x1b[39;49;00m.\x1b[37m\x1b[39;49;00m\n',
  'notes': [],
  'output': '~ > example --value-list-1=<TAB>\n'
            'exec    noexec\n'
            '\n'
            '~ > example --value-list-1=exec,<TAB>\n'
            'noexec\n'
            '\n'
            '~ > example --value-list-2=<TAB>\n'
            'one  -- Description 1\n'
            'two  -- Description 2\n',
  'short': 'Complete comma-separated lists of values'},
 {'also': {'environment': 'For completing environment variable names'},
  'category': 'basic',
  'command': 'variable',
  'definition': "prog: 'example'\n"
                'options:\n'
                "  - option_strings: ['--variable']\n"
                "    complete: ['variable']\n",
  'definition_colored': '\x1b[94mprog\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33mexample\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[94moptions\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33m--variable\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33mvariable\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n",
  'implemented': None,
  'long': None,
  'long_colored': None,
  'notes': [],
  'output': '~ > example --variable=HO<TAB>\nHOME      HOSTNAME  HOSTTYPE\n',
  'short': 'Complete shell variable names'}]


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
