'''This module contains functions for generating a YAML file from help texts.'''

from . import help_parser
from . import yaml_source
from . import utils

def fix_description(s):
    s = s.strip()

    # Replace hyphens followed by a newline ('-\n') with a simple hyphen.
    # This prevents words like "Some-word-with-\nhyphens" from being split
    # incorrectly due to the newline. Instead, it will correctly join as
    # "Some-word-with-hyphens".
    s = s.replace('-\n', '-')

    s = s.replace('\n', ' ')
    return s

def strip_metavar(s):
    if s and s[0] == '[' and s[-1] == ']':
        s = s[1:-1]

    if s and s[0] == '=':
        s = s[1:]

    return s

def complete_for_metavar(s):
    s = s.lower()

    if s == 'f' or s.endswith('file'):
        return ['file']

    if s.endswith('dir') or s.endswith('directory'):
        return ['directory']

    if (s == 'n' or
        s == 'duration' or
        s == 'bits' or
        s == 'cols' or
        s == 'column' or 
        s == 'digits' or
        s == 'size' or
        s == 'bytes' or
        s.endswith('length') or
        s.endswith('width') or
        s.endswith('num') or
        s.endswith('number')
       ):
        return ['integer']

    if s == 'pid':
        return ['pid']

    if s == 'user':
        return ['user']

    if s == 'group':
        return ['group']

    if s == 'program' or s == 'command' or s == 'cmd':
        return ['command']

    if s == 'signal' or s == 'sig':
        return ['signal']

    if s.startswith('{') and s.endswith('}'):
        s = s.strip('{}')
        for sep in ['|', ',']:
            if sep in s:
                return ['choices', [item.strip() for item in s.split(sep)]]

    return ['none']

def from_file_to_yaml(file):
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
                utils.indent(yaml_source.option_to_yaml(option_dict), 2)
            )

            output.append('')

    return '\n'.join(output)
