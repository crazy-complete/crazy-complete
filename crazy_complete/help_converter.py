'''This module contains functions for generating a YAML file from help texts'''

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
                    option_dict['metavar'] = option.metavar
                    option_dict['complete'] = ['none']

            output.append(
                utils.indent(yaml_source.option_to_yaml(option_dict), 2)
            )

            output.append('')

    return '\n'.join(output)
