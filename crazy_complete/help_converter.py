'''This module contains functions for generating a YAML file from help texts.'''

from . import help_parser
from . import yaml_source
from .str_utils import indent


def fix_description(s):
    '''Fix description.'''

    s = s.strip()

    # Replace hyphens followed by a newline ('-\n') with a simple hyphen.
    # This prevents words like "Some-word-with-\nhyphens" from being split
    # incorrectly due to the newline. Instead, it will correctly join as
    # "Some-word-with-hyphens".
    s = s.replace('-\n', '-')

    s = s.replace('\n', ' ')
    return s


def strip_metavar(s):
    '''Strip metavar.'''

    if s and s[0] == '[' and s[-1] == ']':
        s = s[1:-1]

    if s and s[0] == '=':
        s = s[1:]

    if s and s[0] == '<' and s[-1] == '>':
        s = s[1:-1]

    return s


def complete_for_metavar(string):
    '''Return completion for metavar.'''

    string = string.strip('<>')
    lower  = string.lower()

    equals = {
        'f':            ['file'],
        'n':            ['integer'],
        'duration':     ['integer'],
        'bits':         ['integer'],
        'cols':         ['integer'],
        'column':       ['integer'],
        'digits':       ['integer'],
        'size':         ['integer'],
        'bytes':        ['integer'],
        'pid':          ['pid'],
        'user':         ['user'],
        'group':        ['group'],
        'program':      ['command'],
        'command':      ['command'],
        'cmd':          ['cmd'],
        'signal':       ['signal'],
        'sig':          ['signal'],
    }

    endswith = {
        'file':         ['file'],
        'filename':     ['file'],
        'dir':          ['directory'],
        'directory':    ['directory'],
        'seconds':      ['integer'],
        'length':       ['integer'],
        'width':        ['integer'],
        'num':          ['integer'],
        'number':       ['integer'],
    }

    if lower in equals:
        return equals[lower]

    for suffix, complete in endswith.items():
        if lower.endswith(suffix):
            return complete

    if string.startswith('{') and string.endswith('}'):
        string = string.strip('{}')
        for sep in ['|', ',']:
            if sep in string:
                return ['choices', [item.strip() for item in string.split(sep)]]

    return ['none']


def from_file_to_yaml(file):
    '''Parse help text in a file and return YAML.'''

    with open(file, 'r', encoding='utf-8') as fh:
        content = fh.read()

    prog = help_parser.get_program_name_from_help(content)
    char_stream = help_parser.CharStream(content)
    parsed = help_parser.parse(char_stream)

    output = []

    output.append(f'prog: "{prog}"\nhelp: "<Program description here>"\noptions:')

    for obj in parsed:
        if isinstance(obj, help_parser.Unparsed):
            output.append(f"# {obj.text.rstrip()}")
        elif isinstance(obj, help_parser.OptionsWithDescription):
            option_dict = {
                'option_strings': [],
                'metavar':        None,
                'optional_arg':   False,
                'help':           fix_description(obj.description or '')
            }

            for option in obj.options:
                option_dict['option_strings'].append(option.option)

                if option.optional:
                    option_dict['optional_arg'] = True

                if option.metavar:
                    option_dict['metavar'] = strip_metavar(option.metavar)
                    option_dict['complete'] = complete_for_metavar(option_dict['metavar'])

            output.append(
                indent(yaml_source.option_to_yaml(option_dict), 2)
            )

            output.append('')

    return '\n'.join(output)
