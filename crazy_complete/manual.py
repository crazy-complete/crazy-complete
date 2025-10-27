'''Built-int Manual.'''

from .errors import CrazyError
from .str_utils import indent, join_with_wrap


# pylint: disable=line-too-long


COMMANDS = [{'also': {'alsa_device': 'For completing an ALSA device'},
  'category': 'bonus',
  'command': 'alsa_card',
  'definition': 'prog: "example"\n'
                'options:\n'
                '  - option_strings: ["--alsa-card"]\n'
                '    complete: ["alsa_card"]\n',
  'definition_colored': '\x1b[94mprog\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[33mexample\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[94moptions\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33m--alsa-card\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33malsa_card\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n',
  'implemented': None,
  'long': None,
  'long_colored': None,
  'notes': [],
  'output': '~ > example --alsa-card=<TAB>\n0  1\n',
  'short': 'Complete an ALSA card'},
 {'also': {'alsa_card': 'For completing an ALSA card'},
  'category': 'bonus',
  'command': 'alsa_device',
  'definition': 'prog: "example"\n'
                'options:\n'
                '  - option_strings: ["--alsa-device"]\n'
                '    complete: ["alsa_device"]\n',
  'definition_colored': '\x1b[94mprog\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[33mexample\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[94moptions\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33m--alsa-device\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33malsa_device\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n',
  'implemented': None,
  'long': None,
  'long_colored': None,
  'notes': [],
  'output': '~ > example --alsa-device=<TAB>\nhw:0  hw:1\n',
  'short': 'Complete an ALSA device'},
 {'also': None,
  'category': 'bonus',
  'command': 'charset',
  'definition': 'prog: "example"\n'
                'options:\n'
                '  - option_strings: ["--charset"]\n'
                '    complete: ["charset"]\n',
  'definition_colored': '\x1b[94mprog\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[33mexample\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[94moptions\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33m--charset\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33mcharset\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n',
  'implemented': None,
  'long': None,
  'long_colored': None,
  'notes': [],
  'output': '~ > example --charset=A<TAB>\n'
            'ANSI_X3.110-1983  ANSI_X3.4-1968    ARMSCII-8         ASMO_449\n',
  'short': 'Complete a charset'},
 {'also': None,
  'category': 'basic',
  'command': 'choices',
  'definition': 'prog: "example"\n'
                'options:\n'
                '  - option_strings: ["--choices-1"]\n'
                '    complete: ["choices", ["Item 1", "Item 2"]]\n'
                '  - option_strings: ["--choices-2"]\n'
                '    complete: ["choices", {"Item 1": "Description 1", "Item '
                '2": "Description 2"}]\n',
  'definition_colored': '\x1b[94mprog\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[33mexample\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[94moptions\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33m--choices-1\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33mchoices\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m,\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33mItem\x1b[39;49;00m\x1b[31m '
                        '\x1b[39;49;00m\x1b[33m1\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m,\x1b[37m '
                        '\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[33mItem\x1b[39;49;00m\x1b[31m '
                        '\x1b[39;49;00m\x1b[33m2\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m]]\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33m--choices-2\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33mchoices\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m,\x1b[37m '
                        '\x1b[39;49;00m{\x1b[33m"\x1b[39;49;00m\x1b[33mItem\x1b[39;49;00m\x1b[31m '
                        '\x1b[39;49;00m\x1b[33m1\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[33mDescription\x1b[39;49;00m\x1b[31m '
                        '\x1b[39;49;00m\x1b[33m1\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m,\x1b[37m '
                        '\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[33mItem\x1b[39;49;00m\x1b[31m '
                        '\x1b[39;49;00m\x1b[33m2\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[33mDescription\x1b[39;49;00m\x1b[31m '
                        '\x1b[39;49;00m\x1b[33m2\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m}]\x1b[37m\x1b[39;49;00m\n',
  'implemented': None,
  'long': 'Items can be a list or a dictionary.\n'
          ' \n'
          'If a dictionary is supplied, the keys are used as items and the '
          'values are used\n'
          'as description.\n',
  'long_colored': 'Items can be a list or a dictionary.\x1b[37m\x1b[39;49;00m\n'
                  ' \x1b[37m\x1b[39;49;00m\n'
                  'If a dictionary is supplied, the keys are used as items and '
                  'the values are used\x1b[37m\x1b[39;49;00m\n'
                  'as description.\x1b[37m\x1b[39;49;00m\n',
  'notes': [],
  'output': '~ > example --choices-2=<TAB>\n'
            'Item 1  (Description 1)  Item 2  (Description 2)\n',
  'short': 'Complete from a set of words'},
 {'also': None,
  'category': 'meta',
  'command': 'combine',
  'definition': 'prog: "example"\n'
                'options:\n'
                '  - option_strings: ["--combine"]\n'
                '    complete: ["combine", [["user"], ["pid"]]]\n',
  'definition_colored': '\x1b[94mprog\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[33mexample\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[94moptions\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33m--combine\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33mcombine\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m,\x1b[37m '
                        '\x1b[39;49;00m[[\x1b[33m"\x1b[39;49;00m\x1b[33muser\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m],\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33mpid\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m]]]\x1b[37m\x1b[39;49;00m\n',
  'implemented': None,
  'long': 'With `combine` multiple completers can be combined into one.\n'
          '\n'
          'It takes a list of completers as its argument.\n',
  'long_colored': 'With \x1b[33m`combine`\x1b[39;49;00m multiple completers '
                  'can be combined into one.\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m\x1b[39;49;00m\n'
                  'It takes a list of completers as its '
                  'argument.\x1b[37m\x1b[39;49;00m\n',
  'notes': [],
  'output': '~ > example --user-list=avahi,daemon,<TAB>\n'
            '1439404  3488332  3571716           3607235                 '
            '4134206\n'
            'alpm     avahi    bin               braph                   '
            'daemon\n'
            'root     rtkit    systemd-coredump  systemd-journal-remote  '
            'systemd-network\n'
            '[...]\n',
  'short': 'Combine multiple completers'},
 {'also': {'command_arg': 'For completing arguments of a command',
           'commandline_string': 'For completing a command line as a string'},
  'category': 'basic',
  'command': 'command',
  'definition': 'prog: "example"\n'
                'options:\n'
                '  - option_strings: ["--command"]\n'
                '    complete: ["command"]\n'
                '  - option_strings: ["--command-sbin"]\n'
                '    complete: ["command", {"path_append": '
                '"/sbin:/usr/sbin"}]\n',
  'definition_colored': '\x1b[94mprog\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[33mexample\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[94moptions\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33m--command\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33mcommand\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33m--command-sbin\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33mcommand\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m,\x1b[37m '
                        '\x1b[39;49;00m{\x1b[33m"\x1b[39;49;00m\x1b[33mpath_append\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[33m/sbin:/usr/sbin\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m}]\x1b[37m\x1b[39;49;00m\n',
  'implemented': None,
  'long': 'This completer provides completion suggestions for executable '
          "commands available in the system's `$PATH`.\n"
          ' \n'
          '`$PATH` can be modified using these options:\n'
          ' \n'
          '`{"path": "<directory>:..."}`: Overrides the default `$PATH` '
          'entirely.\n'
          ' \n'
          '`{"path_append": "<directory>:..."}`: Appends to the default '
          '`$PATH`.\n'
          ' \n'
          '`{"path_prepend": "<directory>:..."}`: Prepends to the default '
          '`$PATH`.\n',
  'long_colored': 'This completer provides completion suggestions for '
                  "executable commands available in the system's "
                  '\x1b[33m`$PATH`\x1b[39;49;00m.\x1b[37m\x1b[39;49;00m\n'
                  ' \n'
                  '\x1b[33m`$PATH`\x1b[39;49;00m can be modified using these '
                  'options:\x1b[37m\x1b[39;49;00m\n'
                  ' \n'
                  '\x1b[33m`{"path": "<directory>:..."}`\x1b[39;49;00m: '
                  'Overrides the default \x1b[33m`$PATH`\x1b[39;49;00m '
                  'entirely.\x1b[37m\x1b[39;49;00m\n'
                  ' \n'
                  '\x1b[33m`{"path_append": "<directory>:..."}`\x1b[39;49;00m: '
                  'Appends to the default '
                  '\x1b[33m`$PATH`\x1b[39;49;00m.\x1b[37m\x1b[39;49;00m\n'
                  ' \n'
                  '\x1b[33m`{"path_prepend": '
                  '"<directory>:..."}`\x1b[39;49;00m: Prepends to the default '
                  '\x1b[33m`$PATH`\x1b[39;49;00m.\x1b[37m\x1b[39;49;00m\n',
  'notes': ['`path_append` and `path_prepend` can be used together, but both '
            'are mutually exclusive with `path`.'],
  'output': '~ > example --command=bas<TAB>\n'
            'base32    base64    basename  basenc    bash      bashbug\n',
  'short': 'Complete a command'},
 {'also': {'command': 'For completing a command',
           'commandline_string': 'For completing a command line as a string'},
  'category': 'basic',
  'command': 'command_arg',
  'definition': 'prog: "example"\n'
                'positionals:\n'
                '  - number: 1\n'
                '    complete: ["command"]\n'
                '\n'
                '  - number: 2\n'
                '    complete: ["command_arg"]\n'
                '    repeatable: true\n',
  'definition_colored': '\x1b[94mprog\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[33mexample\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[94mpositionals\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94mnumber\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m1\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33mcommand\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94mnumber\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m2\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33mcommand_arg\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n'
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
  'short': 'Complete arguments of a command'},
 {'also': None,
  'category': 'basic',
  'command': 'commandline_string',
  'definition': 'prog: "example"\n'
                'options:\n'
                '  - option_strings: ["--commandline"]\n'
                '    complete: ["commandline_string"]\n',
  'definition_colored': '\x1b[94mprog\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[33mexample\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[94moptions\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33m--commandline\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33mcommandline_string\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n',
  'implemented': None,
  'long': None,
  'long_colored': None,
  'notes': [],
  'output': "~ > example --commandline='sudo ba<TAB>\n"
            'base32    base64    basename  basenc    bash      bashbug\n',
  'short': 'Complete a command line as a string'},
 {'also': {'date_format': 'For completing a date format string'},
  'category': 'basic',
  'command': 'date',
  'definition': 'prog: "example"\n'
                'options:\n'
                '  - option_strings: ["--date"]\n'
                '    complete: ["date", \'%Y-%m-%d\']\n',
  'definition_colored': '\x1b[94mprog\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[33mexample\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[94moptions\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33m--date\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33mdate\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m,\x1b[37m '
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33m%Y-%m-%d\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n",
  'implemented': ['Zsh'],
  'long': 'The argument is the date format as described in `strftime(3)`.\n',
  'long_colored': 'The argument is the date format as described in '
                  '\x1b[33m`strftime(3)`\x1b[39;49;00m.\x1b[37m\x1b[39;49;00m\n',
  'notes': [],
  'output': '~ > example --date=<TAB>\n'
            '\n'
            '         November                        \n'
            'Mo  Tu  We  Th  Fr  Sa  Su     \n'
            '     1   2   3   4   5   6    \n'
            ' 7   8   9  10  11  12  13\n'
            '14  15  16  17  18  19  20\n'
            '21  22  23  24  25  26  27\n'
            '28  29  30                 \n',
  'short': 'Complete a date string'},
 {'also': {'date': 'For completing a date'},
  'category': 'basic',
  'command': 'date_format',
  'definition': 'prog: "example"\n'
                'options:\n'
                '  - option_strings: ["--date-format"]\n'
                '    complete: ["date_format"]\n',
  'definition_colored': '\x1b[94mprog\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[33mexample\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[94moptions\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33m--date-format\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33mdate_format\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n',
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
  'short': 'Complete a date format string'},
 {'also': {'directory_list': 'For completing a comma-separated list of '
                             'directories'},
  'category': 'basic',
  'command': 'directory',
  'definition': 'prog: "example"\n'
                'options:\n'
                '  - option_strings: ["--directory"]\n'
                '    complete: ["directory"]\n'
                '  - option_strings: ["--directory-tmp"]\n'
                '    complete: ["directory", {"directory": "/tmp"}]\n',
  'definition_colored': '\x1b[94mprog\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[33mexample\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[94moptions\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33m--directory\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33mdirectory\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33m--directory-tmp\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33mdirectory\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m,\x1b[37m '
                        '\x1b[39;49;00m{\x1b[33m"\x1b[39;49;00m\x1b[33mdirectory\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[33m/tmp\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m}]\x1b[37m\x1b[39;49;00m\n',
  'implemented': None,
  'long': 'You can restrict completion to a specific directory by adding '
          '`{"directory": ...}`.\n',
  'long_colored': 'You can restrict completion to a specific directory by '
                  'adding \x1b[33m`{"directory": '
                  '...}`\x1b[39;49;00m.\x1b[37m\x1b[39;49;00m\n',
  'notes': [],
  'output': '~ > example --directory=<TAB>\ndir1/  dir2/\n',
  'short': 'Complete a directory'},
 {'also': {'file_list': 'For completing a comma-separated list of files'},
  'category': 'basic',
  'command': 'directory_list',
  'definition': 'prog: "example"\n'
                'options:\n'
                '  - option_strings: ["--directory-list"]\n'
                '    complete: ["directory_list"]\n',
  'definition_colored': '\x1b[94mprog\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[33mexample\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[94moptions\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33m--directory-list\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33mdirectory_list\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n',
  'implemented': None,
  'long': "This is an alias for `['list', ['directory']]`.\n"
          '\n'
          'You can restrict completion to a specific directory by adding '
          '`{"directory": ...}`. Directory has to be an absolute path.\n'
          ' \n'
          'The separator can be changed by adding `{"separator": ...}`\n'
          ' \n'
          'By default, duplicate values are not offered for completion. This '
          'can be changed by adding `{"duplicates": true}`.\n',
  'long_colored': "This is an alias for \x1b[33m`['list', "
                  "['directory']]`\x1b[39;49;00m.\x1b[37m\x1b[39;49;00m\n"
                  '\x1b[37m\x1b[39;49;00m\n'
                  'You can restrict completion to a specific directory by '
                  'adding \x1b[33m`{"directory": ...}`\x1b[39;49;00m. '
                  'Directory has to be an absolute '
                  'path.\x1b[37m\x1b[39;49;00m\n'
                  ' \x1b[37m\x1b[39;49;00m\n'
                  'The separator can be changed by adding '
                  '\x1b[33m`{"separator": '
                  '...}`\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n'
                  ' \x1b[37m\x1b[39;49;00m\n'
                  'By default, duplicate values are not offered for '
                  'completion. This can be changed by adding '
                  '\x1b[33m`{"duplicates": '
                  'true}`\x1b[39;49;00m.\x1b[37m\x1b[39;49;00m\n',
  'notes': [],
  'output': '~ > example --directory-list=directory1,directory2,<TAB>\n'
            'directory3  directory4\n',
  'short': 'Complete a comma-separated list of directories'},
 {'also': None,
  'category': 'basic',
  'command': 'environment',
  'definition': 'prog: "example"\n'
                'options:\n'
                '  - option_strings: ["--environment"]\n'
                '    complete: ["environment"]\n',
  'definition_colored': '\x1b[94mprog\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[33mexample\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[94moptions\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33m--environment\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33menvironment\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n',
  'implemented': None,
  'long': None,
  'long_colored': None,
  'notes': [],
  'output': '~ > example --environment=X<TAB>\n'
            'XDG_RUNTIME_DIR  XDG_SEAT  XDG_SESSION_CLASS  XDG_SESSION_ID\n'
            'XDG_SESSION_TYPE XDG_VTNR\n',
  'short': 'Complete a shell environment variable name'},
 {'also': {'exec_fast': 'Faster implementation of exec'},
  'category': 'custom',
  'command': 'exec',
  'definition': 'prog: "example"\n'
                'options:\n'
                '  - option_strings: ["--exec"]\n'
                '    complete: ["exec", "printf \'%s\\\\t%s\\\\n\' \'Item 1\' '
                '\'Description 1\' \'Item 2\' \'Description 2\'"]\n',
  'definition_colored': '\x1b[94mprog\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[33mexample\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[94moptions\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33m--exec\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33mexec\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m,\x1b[37m '
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
  'long': 'The output must be in form of:\n'
          '\n'
          '```\n'
          '<item_1>\\t<description_1>\\n\n'
          '<item_2>\\t<description_2>\\n\n'
          '[...]\n'
          '```\n'
          '\n'
          'An item and its description are delimited by a tabulator.\n'
          ' \n'
          'These pairs are delimited by a newline.\n',
  'long_colored': 'The output must be in form of:\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[33m\x1b[39;49;00m\n'
                  '\x1b[33m```\x1b[39;49;00m\n'
                  '\x1b[33m<item_1>\\t<description_1>\\n\x1b[39;49;00m\n'
                  '\x1b[33m<item_2>\\t<description_2>\\n\x1b[39;49;00m\n'
                  '\x1b[33m[...]\x1b[39;49;00m\n'
                  '\x1b[33m```\x1b[39;49;00m\n'
                  '\x1b[37m\x1b[39;49;00m\n'
                  'An item and its description are delimited by a '
                  'tabulator.\x1b[37m\x1b[39;49;00m\n'
                  ' \x1b[37m\x1b[39;49;00m\n'
                  'These pairs are delimited by a '
                  'newline.\x1b[37m\x1b[39;49;00m\n',
  'notes': ['Functions can be put inside a file and included with '
            '`--include-file`'],
  'output': '~ > example --exec=<TAB>\n'
            'Item 1  (Description 1)  Item 2  (Description 2)\n',
  'short': 'Complete by the output of a command or function'},
 {'also': None,
  'category': 'custom',
  'command': 'exec_fast',
  'definition': 'prog: "example"\n'
                'options:\n'
                '  - option_strings: ["--exec-fast"]\n'
                '    complete: ["exec_fast", "printf \'%s\\\\t%s\\\\n\' 1 one '
                '2 two"]\n',
  'definition_colored': '\x1b[94mprog\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[33mexample\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[94moptions\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33m--exec-fast\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33mexec_fast\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m,\x1b[37m '
                        '\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[33mprintf\x1b[39;49;00m\x1b[31m '
                        "\x1b[39;49;00m\x1b[33m'%s\x1b[39;49;00m\x1b[33m\\\\\x1b[39;49;00m\x1b[33mt%s\x1b[39;49;00m\x1b[33m\\\\\x1b[39;49;00m\x1b[33mn'\x1b[39;49;00m\x1b[31m "
                        '\x1b[39;49;00m\x1b[33m1\x1b[39;49;00m\x1b[31m '
                        '\x1b[39;49;00m\x1b[33mone\x1b[39;49;00m\x1b[31m '
                        '\x1b[39;49;00m\x1b[33m2\x1b[39;49;00m\x1b[31m '
                        '\x1b[39;49;00m\x1b[33mtwo\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n',
  'implemented': None,
  'long': 'Faster version of exec for handling large amounts of data.\n'
          ' \n'
          'This implementation requires that the items of the parsed output do '
          'not include\n'
          'special shell characters or whitespace.\n',
  'long_colored': 'Faster version of exec for handling large amounts of '
                  'data.\x1b[37m\x1b[39;49;00m\n'
                  ' \x1b[37m\x1b[39;49;00m\n'
                  'This implementation requires that the items of the parsed '
                  'output do not include\x1b[37m\x1b[39;49;00m\n'
                  'special shell characters or '
                  'whitespace.\x1b[37m\x1b[39;49;00m\n',
  'notes': ['Functions can be put inside a file and included with '
            '`--include-file`'],
  'output': '~ > example --exec-internal=<TAB>\n1  -- one\n2  -- one\n',
  'short': 'Complete by the output of a command or function (fast and unsafe)'},
 {'also': None,
  'category': 'custom',
  'command': 'exec_internal',
  'definition': 'prog: "example"\n'
                'options:\n'
                '  - option_strings: ["--exec-internal"]\n'
                '    complete: ["exec_internal", "my_completion_func"]\n',
  'definition_colored': '\x1b[94mprog\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[33mexample\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[94moptions\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33m--exec-internal\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33mexec_internal\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m,\x1b[37m '
                        '\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[33mmy_completion_func\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n',
  'implemented': None,
  'long': 'Execute a function that internally modifies the completion state.\n'
          '\n'
          'This is useful if a more advanced completion is needed.\n'
          '\n'
          'For **Bash**, it might look like:\n'
          '\n'
          '```sh\n'
          'my_completion_func() {\n'
          '    COMPREPLY=( $(compgen -W "read write append" -- "$cur") )\n'
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
                  '\x1b[39;49;00m-W\x1b[37m \x1b[39;49;00m\x1b[33m"read write '
                  'append"\x1b[39;49;00m\x1b[37m \x1b[39;49;00m--\x1b[37m '
                  '\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[31m$cur\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[34m)\x1b[39;49;00m\x1b[37m '
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
  'short': "Complete by a function that uses the shell's internal completion "
           'mechanisms'},
 {'also': {'file_list': 'For completing a comma-separated list of files',
           'mime_file': "For completing a file based on it's MIME-type"},
  'category': 'basic',
  'command': 'file',
  'definition': 'prog: "example"\n'
                'options:\n'
                '  - option_strings: ["--file"]\n'
                '    complete: ["file"]\n'
                '  - option_strings: ["--file-tmp"]\n'
                '    complete: ["file", {"directory": "/tmp"}]\n'
                '  - option_strings: ["--file-ext"]\n'
                '    complete: ["file", {"extensions": ["c", "cpp"]}]\n',
  'definition_colored': '\x1b[94mprog\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[33mexample\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[94moptions\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33m--file\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33mfile\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33m--file-tmp\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33mfile\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m,\x1b[37m '
                        '\x1b[39;49;00m{\x1b[33m"\x1b[39;49;00m\x1b[33mdirectory\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[33m/tmp\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m}]\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33m--file-ext\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33mfile\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m,\x1b[37m '
                        '\x1b[39;49;00m{\x1b[33m"\x1b[39;49;00m\x1b[33mextensions\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33mc\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m,\x1b[37m '
                        '\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[33mcpp\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m]}]\x1b[37m\x1b[39;49;00m\n',
  'implemented': None,
  'long': 'You can restrict completion to a specific directory by adding '
          '`{"directory": ...}`. Directory has to be an absolute path.\n'
          ' \n'
          'You can restrict completion to specific extensions by adding '
          '`{"extensions": [...]}`.\n'
          ' \n'
          'You can make matching extensions *fuzzy* by adding `{"fuzzy": '
          'true}`.\n'
          'Fuzzy means that the files do not have to end with the exact '
          'extension. For example `foo.txt.1`.\n'
          ' \n'
          '**NOTE:** Restricting completion to specific file extensions only '
          'makes sense if the program being completed actually expects files '
          'of those types.\n'
          'On Unix-like systems, file extensions generally have no inherent '
          'meaning -- they are purely conventional and not required for '
          'determining file types.\n',
  'long_colored': 'You can restrict completion to a specific directory by '
                  'adding \x1b[33m`{"directory": ...}`\x1b[39;49;00m. '
                  'Directory has to be an absolute '
                  'path.\x1b[37m\x1b[39;49;00m\n'
                  ' \x1b[37m\x1b[39;49;00m\n'
                  'You can restrict completion to specific extensions by '
                  'adding \x1b[33m`{"extensions": '
                  '[...]}`\x1b[39;49;00m.\x1b[37m\x1b[39;49;00m\n'
                  ' \x1b[37m\x1b[39;49;00m\n'
                  'You can make matching extensions *fuzzy* by adding '
                  '\x1b[33m`{"fuzzy": '
                  'true}`\x1b[39;49;00m.\x1b[37m\x1b[39;49;00m\n'
                  'Fuzzy means that the files do not have to end with the '
                  'exact extension. For example '
                  '\x1b[33m`foo.txt.1`\x1b[39;49;00m.\x1b[37m\x1b[39;49;00m\n'
                  ' \n'
                  '**NOTE:** Restricting completion to specific file '
                  'extensions only makes sense if the program being completed '
                  'actually expects files of those '
                  'types.\x1b[37m\x1b[39;49;00m\n'
                  'On Unix-like systems, file extensions generally have no '
                  'inherent meaning -- they are purely conventional and not '
                  'required for determining file '
                  'types.\x1b[37m\x1b[39;49;00m\n',
  'notes': [],
  'output': '~ > example --file=<TAB>\n'
            'dir1/  dir2/  file1  file2\n'
            '~ > example --file-ext=<TAB>\n'
            'dir1/  dir2/  file.c  file.cpp\n',
  'short': 'Complete a file'},
 {'also': {'directory_list': 'For completing a comma-separated list of '
                             'directories'},
  'category': 'basic',
  'command': 'file_list',
  'definition': 'prog: "example"\n'
                'options:\n'
                '  - option_strings: ["--file-list"]\n'
                '    complete: ["file_list"]\n',
  'definition_colored': '\x1b[94mprog\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[33mexample\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[94moptions\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33m--file-list\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33mfile_list\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n',
  'implemented': None,
  'long': "This is an alias for `['list', ['file']]`.\n"
          '\n'
          'You can restrict completion to a specific directory by adding '
          '`{"directory": ...}`.\n'
          ' \n'
          'You can restrict completion to specific extensions by adding '
          '`{"extensions": [...]}`.\n'
          ' \n'
          'You can make matching extensions *fuzzy* by adding `{"fuzzy": '
          'true}`.\n'
          'Fuzzy means that the files do not have to end with the exact '
          'extension. For example `foo.txt.1`.\n'
          ' \n'
          'By default, duplicate values are not offered for completion. This '
          'can be changed by adding `{"duplicates": true}`.\n'
          '\n'
          'The separator can be changed by adding `{"separator": ...}`\n',
  'long_colored': "This is an alias for \x1b[33m`['list', "
                  "['file']]`\x1b[39;49;00m.\x1b[37m\x1b[39;49;00m\n"
                  '\x1b[37m\x1b[39;49;00m\n'
                  'You can restrict completion to a specific directory by '
                  'adding \x1b[33m`{"directory": '
                  '...}`\x1b[39;49;00m.\x1b[37m\x1b[39;49;00m\n'
                  ' \x1b[37m\x1b[39;49;00m\n'
                  'You can restrict completion to specific extensions by '
                  'adding \x1b[33m`{"extensions": '
                  '[...]}`\x1b[39;49;00m.\x1b[37m\x1b[39;49;00m\n'
                  ' \x1b[37m\x1b[39;49;00m\n'
                  'You can make matching extensions *fuzzy* by adding '
                  '\x1b[33m`{"fuzzy": '
                  'true}`\x1b[39;49;00m.\x1b[37m\x1b[39;49;00m\n'
                  'Fuzzy means that the files do not have to end with the '
                  'exact extension. For example '
                  '\x1b[33m`foo.txt.1`\x1b[39;49;00m.\x1b[37m\x1b[39;49;00m\n'
                  ' \x1b[37m\x1b[39;49;00m\n'
                  'By default, duplicate values are not offered for '
                  'completion. This can be changed by adding '
                  '\x1b[33m`{"duplicates": '
                  'true}`\x1b[39;49;00m.\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m\x1b[39;49;00m\n'
                  'The separator can be changed by adding '
                  '\x1b[33m`{"separator": '
                  '...}`\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n',
  'notes': [],
  'output': '~ > example --file-list=file1,file2,<TAB>\nfile3  file4\n',
  'short': 'Complete a comma-separated list of files'},
 {'also': None,
  'category': 'basic',
  'command': 'filesystem_type',
  'definition': 'prog: "example"\n'
                'options:\n'
                '  - option_strings: ["--filesystem-type"]\n'
                '    complete: ["filesystem_type"]\n',
  'definition_colored': '\x1b[94mprog\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[33mexample\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[94moptions\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33m--filesystem-type\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33mfilesystem_type\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n',
  'implemented': None,
  'long': None,
  'long_colored': None,
  'notes': [],
  'output': '~ > example --filesystem-type=<TAB>\n'
            'adfs     autofs   bdev      bfs     binder     binfmt_misc  bpf\n'
            'cgroup   cgroup2  configfs  cramfs  debugfs    devpts       '
            'devtmpfs\n'
            '[...]\n',
  'short': 'Complete a filesystem type'},
 {'also': None,
  'category': 'basic',
  'command': 'float',
  'definition': 'prog: "example"\n'
                'options:\n'
                '  - option_strings: ["--float"]\n'
                '    complete: ["float"]\n',
  'definition_colored': '\x1b[94mprog\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[33mexample\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[94moptions\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33m--float\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33mfloat\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n',
  'implemented': None,
  'long': None,
  'long_colored': None,
  'notes': ['This completer currently serves as documentation and does not '
            'provide actual functionality.'],
  'output': '~ > example --float=<TAB>\n<NO OUTPUT>\n',
  'short': 'Complete floating point number'},
 {'also': {'group': 'For completing a group name'},
  'category': 'basic',
  'command': 'gid',
  'definition': 'prog: "example"\n'
                'options:\n'
                '  - option_strings: ["--gid"]\n'
                '    complete: ["gid"]\n',
  'definition_colored': '\x1b[94mprog\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[33mexample\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[94moptions\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33m--gid\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33mgid\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n',
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
  'short': 'Complete a group id'},
 {'also': {'gid': 'For completing a group id'},
  'category': 'basic',
  'command': 'group',
  'definition': 'prog: "example"\n'
                'options:\n'
                '  - option_strings: ["--group"]\n'
                '    complete: ["group"]\n',
  'definition_colored': '\x1b[94mprog\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[33mexample\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[94moptions\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33m--group\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33mgroup\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n',
  'implemented': None,
  'long': None,
  'long_colored': None,
  'notes': [],
  'output': '~ > example --group=<TAB>\n'
            'adm                     audio                   avahi\n'
            'bin                     braph                   colord\n'
            'daemon                  dbus                    dhcpcd\n'
            'disk                    floppy                  ftp\n'
            'games                   git                     groups\n'
            '[...]\n',
  'short': 'Complete a group'},
 {'also': None,
  'category': 'basic',
  'command': 'history',
  'definition': 'prog: "example"\n'
                'options:\n'
                '  - option_strings: ["--history"]\n'
                '    complete: ["history", \'[a-zA-Z0-9]+@[a-zA-Z0-9]+\']\n',
  'definition_colored': '\x1b[94mprog\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[33mexample\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[94moptions\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33m--history\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33mhistory\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m,\x1b[37m '
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33m[a-zA-Z0-9]+@[a-zA-Z0-9]+\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n",
  'implemented': None,
  'long': 'The argument is an extended regular expression passed to `grep '
          '-E`.\n',
  'long_colored': 'The argument is an extended regular expression passed to '
                  '\x1b[33m`grep -E`\x1b[39;49;00m.\x1b[37m\x1b[39;49;00m\n',
  'notes': [],
  'output': '~ > example --history=<TAB>\nfoo@bar mymail@myprovider\n',
  'short': "Complete based on a shell's history"},
 {'also': None,
  'category': 'basic',
  'command': 'hostname',
  'definition': 'prog: "example"\n'
                'options:\n'
                '  - option_strings: ["--hostname"]\n'
                '    complete: ["hostname"]\n',
  'definition_colored': '\x1b[94mprog\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[33mexample\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[94moptions\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33m--hostname\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33mhostname\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n',
  'implemented': None,
  'long': None,
  'long_colored': None,
  'notes': [],
  'output': '~ > example --hostname=<TAB>\nlocalhost\n',
  'short': 'Complete a hostname'},
 {'also': {'range': 'For completing a range of integers'},
  'category': 'basic',
  'command': 'integer',
  'definition': 'prog: "example"\n'
                'options:\n'
                '  - option_strings: ["--integer"]\n'
                '    complete: ["integer"]\n',
  'definition_colored': '\x1b[94mprog\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[33mexample\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[94moptions\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33m--integer\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33minteger\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n',
  'implemented': None,
  'long': None,
  'long_colored': None,
  'notes': ['This completer currently serves as documentation and does not '
            'provide actual functionality.'],
  'output': '~ > example --integer=<TAB>\n<NO OUTPUT>\n',
  'short': 'Complete an integer'},
 {'also': None,
  'category': 'meta',
  'command': 'key_value_list',
  'definition': 'prog: "example"\n'
                'options:\n'
                '  - option_strings: ["--key-value-list"]\n'
                '    complete: ["key_value_list", ",", "=", {\n'
                "      'flag':   null,\n"
                "      'nocomp': ['none'],\n"
                "      'user':   ['user'],\n"
                "      'check':  ['choices', {\n"
                '        \'relaxed\': "convert to lowercase before lookup",\n'
                '        \'strict\': "no conversion"\n'
                '      }]\n'
                '    }]\n'
                '\n'
                '  - option_strings: ["--key-value-list-with-desc"]\n'
                '    complete: ["key_value_list", ",", "=", [\n'
                "      ['flag',   'An option flag', null],\n"
                "      ['nodesc', null, null],\n"
                "      ['nocomp', 'An option with arg but without completer', "
                "['none']],\n"
                "      ['user',   'Takes a username',  ['user']],\n"
                "      ['check',  'Specify file name conversions', ['choices', "
                '{\n'
                '        \'relaxed\': "convert to lowercase before lookup",\n'
                '        \'strict\': "no conversion"\n'
                '      }]]\n'
                '    ]]\n',
  'definition_colored': '\x1b[94mprog\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[33mexample\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[94moptions\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33m--key-value-list\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33mkey_value_list\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m,\x1b[37m '
                        '\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[33m,\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m,\x1b[37m '
                        '\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[33m=\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m,\x1b[37m '
                        '\x1b[39;49;00m{\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m      '
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33mflag\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m:\x1b[37m   "
                        '\x1b[39;49;00m\x1b[31mnull\x1b[39;49;00m,\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m      '
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33mnocomp\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m:\x1b[37m "
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33mnone\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m],\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[37m      '
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33muser\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m:\x1b[37m   "
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33muser\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m],\x1b[37m\x1b[39;49;00m\n"
                        '\x1b[37m      '
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33mcheck\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m:\x1b[37m  "
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33mchoices\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m,\x1b[37m "
                        '\x1b[39;49;00m{\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m        '
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33mrelaxed\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m:\x1b[37m "
                        '\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[33mconvert\x1b[39;49;00m\x1b[31m '
                        '\x1b[39;49;00m\x1b[33mto\x1b[39;49;00m\x1b[31m '
                        '\x1b[39;49;00m\x1b[33mlowercase\x1b[39;49;00m\x1b[31m '
                        '\x1b[39;49;00m\x1b[33mbefore\x1b[39;49;00m\x1b[31m '
                        '\x1b[39;49;00m\x1b[33mlookup\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m,\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m        '
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33mstrict\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m:\x1b[37m "
                        '\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[33mno\x1b[39;49;00m\x1b[31m '
                        '\x1b[39;49;00m\x1b[33mconversion\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m      \x1b[39;49;00m}]\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m    \x1b[39;49;00m}]\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33m--key-value-list-with-desc\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33mkey_value_list\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m,\x1b[37m '
                        '\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[33m,\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m,\x1b[37m '
                        '\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[33m=\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m,\x1b[37m '
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
                        '\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[33mconvert\x1b[39;49;00m\x1b[31m '
                        '\x1b[39;49;00m\x1b[33mto\x1b[39;49;00m\x1b[31m '
                        '\x1b[39;49;00m\x1b[33mlowercase\x1b[39;49;00m\x1b[31m '
                        '\x1b[39;49;00m\x1b[33mbefore\x1b[39;49;00m\x1b[31m '
                        '\x1b[39;49;00m\x1b[33mlookup\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m,\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m        '
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33mstrict\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m:\x1b[37m "
                        '\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[33mno\x1b[39;49;00m\x1b[31m '
                        '\x1b[39;49;00m\x1b[33mconversion\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m      '
                        '\x1b[39;49;00m}]]\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m    \x1b[39;49;00m]]\x1b[37m\x1b[39;49;00m\n',
  'implemented': None,
  'long': 'The first argument is the separator used for delimiting the '
          'key-value pairs.\n'
          '\n'
          'The second argument is the separator used for delimiting the value '
          'from the key.\n'
          '\n'
          'The third argument is either a dictionary or a list.\n'
          '\n'
          'The dictionary has to be in the form of:\n'
          '\n'
          '  `{<key>: <completer>, ...}`\n'
          '\n'
          'The list has to be in the form of:\n'
          '\n'
          '  `[ [<key>, <description>, <completer>], ... ]`\n'
          '\n'
          'If a key does not take an argument, use `null` as completer.\n'
          '\n'
          'If a key does take an argument but cannot be completed, use '
          "`['none']` as completer.\n",
  'long_colored': 'The first argument is the separator used for delimiting the '
                  'key-value pairs.\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m\x1b[39;49;00m\n'
                  'The second argument is the separator used for delimiting '
                  'the value from the key.\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m\x1b[39;49;00m\n'
                  'The third argument is either a dictionary or a '
                  'list.\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m\x1b[39;49;00m\n'
                  'The dictionary has to be in the form '
                  'of:\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m\x1b[39;49;00m\n'
                  '  \x1b[33m`{<key>: <completer>, '
                  '...}`\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m\x1b[39;49;00m\n'
                  'The list has to be in the form of:\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m\x1b[39;49;00m\n'
                  '  \x1b[33m`[ [<key>, <description>, <completer>], ... '
                  ']`\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m\x1b[39;49;00m\n'
                  'If a key does not take an argument, use '
                  '\x1b[33m`null`\x1b[39;49;00m as '
                  'completer.\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m\x1b[39;49;00m\n'
                  'If a key does take an argument but cannot be completed, use '
                  "\x1b[33m`['none']`\x1b[39;49;00m as "
                  'completer.\x1b[37m\x1b[39;49;00m\n',
  'notes': [],
  'output': '~ > example --key-value-list flag,user=<TAB>\n'
            'bin                     braph\n'
            'colord                  dbus\n'
            'dhcpcd                  git\n',
  'short': 'Complete a comma-separated list of key=value pairs'},
 {'also': {'directory_list': 'For completing a comma-separated list of '
                             'directories',
           'file_list': 'For completing a comma-separated list of files',
           'key_value_list': 'For completing a comma-separated list of '
                             'key=value pairs'},
  'category': 'meta',
  'command': 'list',
  'definition': 'prog: "example"\n'
                'options:\n'
                '  - option_strings: ["--user-list"]\n'
                '    complete: ["list", ["user"]]\n'
                '  - option_strings: ["--option-list"]\n'
                '    complete: ["list", ["choices", ["setuid", "async", '
                '"block"]], {"separator": ":"}]\n',
  'definition_colored': '\x1b[94mprog\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[33mexample\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[94moptions\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33m--user-list\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33mlist\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m,\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33muser\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m]]\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33m--option-list\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33mlist\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m,\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33mchoices\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m,\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33msetuid\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m,\x1b[37m '
                        '\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[33masync\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m,\x1b[37m '
                        '\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[33mblock\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m]],\x1b[37m '
                        '\x1b[39;49;00m{\x1b[33m"\x1b[39;49;00m\x1b[33mseparator\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[33m:\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m}]\x1b[37m\x1b[39;49;00m\n',
  'implemented': None,
  'long': 'The separator can be changed by adding `{"separator": ...}`.\n'
          '\n'
          'By default, duplicate values are not offered for completion. This '
          'can be changed by adding `{"duplicates": true}`.\n',
  'long_colored': 'The separator can be changed by adding '
                  '\x1b[33m`{"separator": '
                  '...}`\x1b[39;49;00m.\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m\x1b[39;49;00m\n'
                  'By default, duplicate values are not offered for '
                  'completion. This can be changed by adding '
                  '\x1b[33m`{"duplicates": '
                  'true}`\x1b[39;49;00m.\x1b[37m\x1b[39;49;00m\n',
  'notes': [],
  'output': '~ > example --user-list=avahi,daemon,<TAB>\n'
            'bin                     braph\n'
            'colord                  dbus\n'
            'dhcpcd                  git\n',
  'short': 'Complete a comma-separated list of any completer'},
 {'also': None,
  'category': 'bonus',
  'command': 'locale',
  'definition': 'prog: "example"\n'
                'options:\n'
                '  - option_strings: ["--locale"]\n'
                '    complete: ["locale"]\n',
  'definition_colored': '\x1b[94mprog\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[33mexample\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[94moptions\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33m--locale\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33mlocale\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n',
  'implemented': None,
  'long': None,
  'long_colored': None,
  'notes': [],
  'output': '~ > example --locale=<TAB>\n'
            'C  C.UTF-8  de_DE  de_DE@euro  de_DE.iso88591  '
            'de_DE.iso885915@euro\n'
            'de_DE.UTF-8  deutsch  en_US  en_US.iso88591  en_US.UTF-8  german  '
            'POSIX\n',
  'short': 'Complete a locale'},
 {'also': None,
  'category': 'bonus',
  'command': 'login_shell',
  'definition': 'prog: "example"\n'
                'options:\n'
                '  - option_strings: ["--login-shell"]\n'
                '    complete: ["login_shell"]\n',
  'definition_colored': '\x1b[94mprog\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[33mexample\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[94moptions\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33m--login-shell\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33mlogin_shell\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n',
  'implemented': None,
  'long': None,
  'long_colored': None,
  'notes': [],
  'output': '~ > example --login-shell=<TAB>\n'
            '/bin/bash   /bin/sh         /usr/bin/fish       /usr/bin/sh\n'
            '[...]\n',
  'short': 'Complete a login shell'},
 {'also': None,
  'category': 'basic',
  'command': 'mime_file',
  'definition': 'prog: "example"\n'
                'options:\n'
                '  - option_strings: ["--image"]\n'
                '    complete: ["mime_file", \'image/\']\n',
  'definition_colored': '\x1b[94mprog\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[33mexample\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[94moptions\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33m--image\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33mmime_file\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m,\x1b[37m '
                        "\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m\x1b[33mimage/\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n",
  'implemented': None,
  'long': 'This completer takes an extended regex passed to `grep -E` to '
          'filter the results.\n',
  'long_colored': 'This completer takes an extended regex passed to '
                  '\x1b[33m`grep -E`\x1b[39;49;00m to filter the '
                  'results.\x1b[37m\x1b[39;49;00m\n',
  'notes': [],
  'output': '~ > example --image=<TAB>\ndir1/  dir2/  img.png  img.jpg\n',
  'short': "Complete a file based on it's MIME-type"},
 {'also': None,
  'category': 'bonus',
  'command': 'mountpoint',
  'definition': 'prog: "example"\n'
                'options:\n'
                '  - option_strings: ["--mountpoint"]\n'
                '    complete: ["mountpoint"]\n',
  'definition_colored': '\x1b[94mprog\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[33mexample\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[94moptions\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33m--mountpoint\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33mmountpoint\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n',
  'implemented': None,
  'long': None,
  'long_colored': None,
  'notes': [],
  'output': '~ > example --mountpoint=<TAB>\n'
            '/  /boot  /home  /proc  /run  /sys  /tmp\n'
            '[...]\n',
  'short': 'Complete a mountpoint'},
 {'also': None,
  'category': 'bonus',
  'command': 'net_interface',
  'definition': 'prog: "example"\n'
                'options:\n'
                '  - option_strings: ["--net-interface"]\n'
                '    complete: ["net_interface"]\n',
  'definition_colored': '\x1b[94mprog\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[33mexample\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[94moptions\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33m--net-interface\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33mnet_interface\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n',
  'implemented': None,
  'long': None,
  'long_colored': None,
  'notes': [],
  'output': '~ > example --net-interface=<TAB>\n'
            'eno1  enp1s0  lo  wlo1  wlp2s0\n'
            '[...]\n',
  'short': 'Complete a network interface'},
 {'also': None,
  'category': 'meta',
  'command': 'none',
  'definition': 'prog: "example"\n'
                'options:\n'
                '  - option_strings: ["--none"]\n'
                '    complete: ["none"]\n',
  'definition_colored': '\x1b[94mprog\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[33mexample\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[94moptions\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33m--none\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33mnone\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n',
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
  'short': 'No completion, but specifies that an argument is required'},
 {'also': {'process': 'For completing a process name'},
  'category': 'basic',
  'command': 'pid',
  'definition': 'prog: "example"\n'
                'options:\n'
                '  - option_strings: ["--pid"]\n'
                '    complete: ["pid"]\n',
  'definition_colored': '\x1b[94mprog\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[33mexample\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[94moptions\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33m--pid\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33mpid\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n',
  'implemented': None,
  'long': None,
  'long_colored': None,
  'notes': [],
  'output': '~ > example --pid=<TAB>\n'
            '1       13      166     19      254     31      45\n'
            '1006    133315  166441  19042   26      32      46\n'
            '10150   1392    166442  195962  27      33      4609\n',
  'short': 'Complete a PID'},
 {'also': None,
  'category': 'meta',
  'command': 'prefix',
  'definition': 'prog: "example"\n'
                'options:\n'
                '  - option_strings: ["--prefix"]\n'
                '    complete: ["prefix", "input:", [\'file\']]\n',
  'definition_colored': '\x1b[94mprog\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[33mexample\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[94moptions\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33m--prefix\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33mprefix\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m,\x1b[37m '
                        '\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[33minput:\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m,\x1b[37m '
                        "\x1b[39;49;00m[\x1b[33m'\x1b[39;49;00m\x1b[33mfile\x1b[39;49;00m\x1b[33m'\x1b[39;49;00m]]\x1b[37m\x1b[39;49;00m\n",
  'implemented': None,
  'long': 'The first argument is the prefix that should be used.\n'
          '\n'
          'The second argument is a completer.\n',
  'long_colored': 'The first argument is the prefix that should be '
                  'used.\x1b[37m\x1b[39;49;00m\n'
                  '\x1b[37m\x1b[39;49;00m\n'
                  'The second argument is a completer.\x1b[37m\x1b[39;49;00m\n',
  'notes': [],
  'output': '~ > example --prefix=<TAB>\n'
            '~ > example --prefix=input:\n'
            '\n'
            '~ > example --prefix=input:<TAB>\n'
            '~ > example --prefix=input:file1.txt\n',
  'short': 'Prefix completion by a string'},
 {'also': {'pid': 'For completing a PID'},
  'category': 'basic',
  'command': 'process',
  'definition': 'prog: "example"\n'
                'options:\n'
                '  - option_strings: ["--process"]\n'
                '    complete: ["process"]\n',
  'definition_colored': '\x1b[94mprog\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[33mexample\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[94moptions\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33m--process\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33mprocess\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n',
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
  'short': 'Complete a process name'},
 {'also': None,
  'category': 'basic',
  'command': 'range',
  'definition': 'prog: "example"\n'
                'options:\n'
                '  - option_strings: ["--range-1"]\n'
                '    complete: ["range", 1, 9]\n'
                '  - option_strings: ["--range-2"]\n'
                '    complete: ["range", 1, 9, 2]\n',
  'definition_colored': '\x1b[94mprog\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[33mexample\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[94moptions\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33m--range-1\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33mrange\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m,\x1b[37m '
                        '\x1b[39;49;00m\x1b[31m1\x1b[39;49;00m,\x1b[37m '
                        '\x1b[39;49;00m\x1b[31m9\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33m--range-2\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33mrange\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m,\x1b[37m '
                        '\x1b[39;49;00m\x1b[31m1\x1b[39;49;00m,\x1b[37m '
                        '\x1b[39;49;00m\x1b[31m9\x1b[39;49;00m,\x1b[37m '
                        '\x1b[39;49;00m\x1b[31m2\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n',
  'implemented': None,
  'long': None,
  'long_colored': None,
  'notes': [],
  'output': '~ > example --range-1=<TAB>\n'
            '1  2  3  4  5  6  7  8  9\n'
            '~ > example --range-2=<TAB>\n'
            '1  3  5  7  9\n',
  'short': 'Complete a range of integers'},
 {'also': None,
  'category': 'basic',
  'command': 'service',
  'definition': 'prog: "example"\n'
                'options:\n'
                '  - option_strings: ["--service"]\n'
                '    complete: ["service"]\n',
  'definition_colored': '\x1b[94mprog\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[33mexample\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[94moptions\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33m--service\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33mservice\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n',
  'implemented': None,
  'long': None,
  'long_colored': None,
  'notes': [],
  'output': '~ > example --service=<TAB>\nTODO\n[...]\n',
  'short': 'Complete a SystemD service'},
 {'also': None,
  'category': 'basic',
  'command': 'signal',
  'definition': 'prog: "example"\n'
                'options:\n'
                '  - option_strings: ["--signal"]\n'
                '    complete: ["signal"]\n',
  'definition_colored': '\x1b[94mprog\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[33mexample\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[94moptions\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33m--signal\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33msignal\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n',
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
  'definition': 'prog: "example"\n'
                'options:\n'
                '  - option_strings: ["--timezone"]\n'
                '    complete: ["timezone"]\n',
  'definition_colored': '\x1b[94mprog\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[33mexample\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[94moptions\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33m--timezone\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33mtimezone\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n',
  'implemented': None,
  'long': None,
  'long_colored': None,
  'notes': [],
  'output': '~ > example --timezone=Europe/B<TAB>\n'
            'Belfast     Belgrade    Berlin      Bratislava\n'
            'Brussels    Bucharest   Budapest    Busingen\n',
  'short': 'Complete a timezone'},
 {'also': {'user': 'For completing a user name'},
  'category': 'basic',
  'command': 'uid',
  'definition': 'prog: "example"\n'
                'options:\n'
                '  - option_strings: ["--uid"]\n'
                '    complete: ["uid"]\n',
  'definition_colored': '\x1b[94mprog\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[33mexample\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[94moptions\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33m--uid\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33muid\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n',
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
  'short': 'Complete a user id'},
 {'also': {'uid': 'For completing a user id'},
  'category': 'basic',
  'command': 'user',
  'definition': 'prog: "example"\n'
                'options:\n'
                '  - option_strings: ["--user"]\n'
                '    complete: ["user"]\n',
  'definition_colored': '\x1b[94mprog\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[33mexample\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[94moptions\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33m--user\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33muser\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n',
  'implemented': None,
  'long': None,
  'long_colored': None,
  'notes': [],
  'output': '~ > example --user=<TAB>\n'
            'avahi                   bin                     braph\n'
            'colord                  daemon                  dbus\n'
            'dhcpcd                  ftp                     git\n'
            '[...]\n',
  'short': 'Complete a username'},
 {'also': {'key_value_list': 'For completing a comma-separated list of '
                             'key=value pairs'},
  'category': 'basic',
  'command': 'value_list',
  'definition': 'prog: "example"\n'
                'options:\n'
                '  - option_strings: ["--value-list-1"]\n'
                '    complete: ["value_list", {"values": ["exec", "noexec"]}]\n'
                '  - option_strings: ["--value-list-2"]\n'
                '    complete: ["value_list", {"values": {"one": "Description '
                '1", "two": "Description 2"}}]\n',
  'definition_colored': '\x1b[94mprog\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[33mexample\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[94moptions\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33m--value-list-1\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33mvalue_list\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m,\x1b[37m '
                        '\x1b[39;49;00m{\x1b[33m"\x1b[39;49;00m\x1b[33mvalues\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33mexec\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m,\x1b[37m '
                        '\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[33mnoexec\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m]}]\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33m--value-list-2\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33mvalue_list\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m,\x1b[37m '
                        '\x1b[39;49;00m{\x1b[33m"\x1b[39;49;00m\x1b[33mvalues\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m{\x1b[33m"\x1b[39;49;00m\x1b[33mone\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[33mDescription\x1b[39;49;00m\x1b[31m '
                        '\x1b[39;49;00m\x1b[33m1\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m,\x1b[37m '
                        '\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[33mtwo\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[33mDescription\x1b[39;49;00m\x1b[31m '
                        '\x1b[39;49;00m\x1b[33m2\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m}}]\x1b[37m\x1b[39;49;00m\n',
  'implemented': None,
  'long': 'Complete one or more items from a list of items. Similar to `mount '
          '-o`.\n'
          ' \n'
          'Arguments are supplied by adding `{"values": ...}`.\n'
          ' \n'
          'A separator can be supplied by adding `{"separator": ...}` (the '
          'default is `","`).\n'
          ' \n'
          'By default, duplicate values are not offered for completion. This '
          'can be changed by adding `{"duplicates": true}`.\n',
  'long_colored': 'Complete one or more items from a list of items. Similar to '
                  '\x1b[33m`mount -o`\x1b[39;49;00m.\x1b[37m\x1b[39;49;00m\n'
                  ' \x1b[37m\x1b[39;49;00m\n'
                  'Arguments are supplied by adding \x1b[33m`{"values": '
                  '...}`\x1b[39;49;00m.\x1b[37m\x1b[39;49;00m\n'
                  ' \x1b[37m\x1b[39;49;00m\n'
                  'A separator can be supplied by adding '
                  '\x1b[33m`{"separator": ...}`\x1b[39;49;00m (the default is '
                  '\x1b[33m`","`\x1b[39;49;00m).\x1b[37m\x1b[39;49;00m\n'
                  ' \x1b[37m\x1b[39;49;00m\n'
                  'By default, duplicate values are not offered for '
                  'completion. This can be changed by adding '
                  '\x1b[33m`{"duplicates": '
                  'true}`\x1b[39;49;00m.\x1b[37m\x1b[39;49;00m\n',
  'notes': [],
  'output': '~ > example --value-list-1=<TAB>\n'
            'exec    noexec\n'
            '~ > example --value-list-1=exec,<TAB>\n'
            'noexec\n'
            '~ > example --value-list-2=<TAB>\n'
            'one  -- Description 1\n'
            'two  -- Description 2\n',
  'short': 'Complete a comma-separated list of values'},
 {'also': {'environment': 'For completing an environment variable'},
  'category': 'basic',
  'command': 'variable',
  'definition': 'prog: "example"\n'
                'options:\n'
                '  - option_strings: ["--variable"]\n'
                '    complete: ["variable"]\n',
  'definition_colored': '\x1b[94mprog\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[33mexample\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[94moptions\x1b[39;49;00m:\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m  \x1b[39;49;00m-\x1b[37m '
                        '\x1b[39;49;00m\x1b[94moption_strings\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33m--variable\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n'
                        '\x1b[37m    '
                        '\x1b[39;49;00m\x1b[94mcomplete\x1b[39;49;00m:\x1b[37m '
                        '\x1b[39;49;00m[\x1b[33m"\x1b[39;49;00m\x1b[33mvariable\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m]\x1b[37m\x1b[39;49;00m\n',
  'implemented': None,
  'long': None,
  'long_colored': None,
  'notes': [],
  'output': '~ > example --variable=HO<TAB>\nHOME      HOSTNAME  HOSTTYPE\n',
  'short': 'Complete a shell variable name'}]


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
    except CrazyError:
        commands = [cmd['command'] for cmd in COMMANDS]
        print('Topic not found')
        print('')
        print('Available completers:')
        print(indent(join_with_wrap(' ', '\n', 40, commands), 4))
