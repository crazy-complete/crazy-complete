"""
This module provides functions for creating CommandLine objects from YAML
and vice versa.
"""

import json
import yaml

from . import dictionary_source
from . import scheme_validator
from .str_utils import indent
from .extended_yaml_parser import ExtendedYAMLParser
from .cli import ExtendedBool


# pylint: disable=redefined-builtin


_INHERIT = ExtendedBool.INHERIT


def option_to_yaml(dictionary):
    '''Convert an option dictionary to YAML.'''

    option_strings = dictionary['option_strings']

    fields = [
        # name,             default,    include-if
        ('metavar',         None,       lambda v: v is not None),
        ('help',            None,       lambda v: v is not None),
        ('optional_arg',    False,      lambda v: v is True),
        ('groups',          None,       lambda v: v is not None),
        ('repeatable',      _INHERIT,   lambda v: v != _INHERIT),
        ('final',           False,      lambda v: v is True),
        ('hidden',          False,      lambda v: v is True),
        ('complete',        None,       lambda v: v is not None),
        ('nosort',          None,       lambda v: v is True),
        ('when',            None,       lambda v: v is not None),
        ('capture',         None,       lambda v: v is not None),
    ]

    r = [f'- option_strings: {json.dumps(option_strings)}']

    for name, default, include_if in fields:
        value = dictionary.get(name, default)

        if include_if(value):
            r.append(f'  {name}: {json.dumps(value)}')

    return '\n'.join(r)


def positional_to_yaml(dictionary):
    '''Convert a positional dictionary to YAML.'''

    number = dictionary['number']

    fields = [
        # name,             default,    include-if
        ('metavar',         None,       lambda v: v is not None),
        ('help',            None,       lambda v: v is not None),
        ('repeatable',      False,      lambda v: v is True),
        ('complete',        None,       lambda v: v is not None),
        ('nosort',          None,       lambda v: v is True),
        ('when',            None,       lambda v: v is not None),
        ('capture',         None,       lambda v: v is not None),
    ]

    r = [f'- number: {number}']

    for name, default, include_if in fields:
        value = dictionary.get(name, default)

        if include_if(value):
            r.append(f'  {name}: {json.dumps(value)}')

    return '\n'.join(r)


def to_yaml(dictionary):
    '''Convert a single dictionary to YAML.'''

    prog                = dictionary['prog']
    aliases             = dictionary.get('aliases',             None)
    help                = dictionary.get('help',                None)
    wraps               = dictionary.get('wraps',               None)
    abbreviate_commands = dictionary.get('abbreviate_commands', _INHERIT)
    abbreviate_options  = dictionary.get('abbreviate_options',  _INHERIT)
    inherit_options     = dictionary.get('inherit_options',     _INHERIT)
    options             = dictionary.get('options',             None)
    positionals         = dictionary.get('positionals',         None)

    r = 'prog: %s\n' % json.dumps(prog)

    if aliases is not None:
        r += 'aliases: %s\n' % json.dumps(aliases)

    if help is not None:
        r += 'help: %s\n' % json.dumps(help)

    if wraps is not None:
        r += 'wraps: %s\n' % json.dumps(wraps)

    if abbreviate_commands != ExtendedBool.INHERIT:
        r += 'abbreviate_commands: %s\n' % json.dumps(abbreviate_commands)

    if abbreviate_options != ExtendedBool.INHERIT:
        r += 'abbreviate_options: %s\n' % json.dumps(abbreviate_options)

    if inherit_options != ExtendedBool.INHERIT:
        r += 'inherit_options: %s\n' % json.dumps(inherit_options)

    if options:
        r += 'options:\n'
        for option in options:
            r += indent(option_to_yaml(option), 2)
            r += '\n\n'

    if positionals:
        r += 'positionals:\n'
        for positional in positionals:
            r += indent(positional_to_yaml(positional), 2)
            r += '\n\n'

    return r.rstrip()


def commandline_to_yaml(commandline):
    '''Convert a cli.CommandLine object to YAML.'''

    dictionaries = dictionary_source.commandline_to_dictionaries(commandline)
    r = []

    for dictionary in dictionaries:
        r.append(to_yaml(dictionary))

    return '\n---\n'.join(r)


def replace_defines_in_documents(documents):
    '''Replaces defines in a list of documents.

    Example:
        prog: '%defines%'
        my_completer: ['choices', ['foo', 'bar']]
        ---
        prog: 'example'
        options:
          - option_strings: ['-o']
            complete: 'my_completer'
    '''

    defines = None

    for document in documents:
        if not isinstance(document.value, dict):
            continue

        if 'prog' in document.value and document.value['prog'].value == '%defines%':
            defines = document
            break

    if defines is None:
        return documents

    documents.remove(defines)
    defines.value.pop('prog')

    def replace_defines(obj):
        if isinstance(obj.value, str):
            return defines.value.get(obj.value, obj)
        if isinstance(obj.value, list):
            obj.value = [replace_defines(sub) for sub in obj.value]
            return obj
        if isinstance(obj.value, dict):
            obj.value = {key: replace_defines(val) for key, val in obj.value.items()}
            return obj
        return obj

    new = []
    for document in documents:
        new.append(replace_defines(document))
    return new


def load_from_file(file):
    '''Load a YAML file and turn it into a cli.CommandLine object.'''

    # First, load using normal yaml loader. It gives better error messages
    # in case of syntax errors.
    with open(file, 'r', encoding='utf-8') as fh:
        dictionaries = list(yaml.safe_load_all(fh))

    # Then load using extended yaml loader...
    with open(file, 'r', encoding='utf-8') as fh:
        content = fh.read()

    # Validate YAML...
    parser = ExtendedYAMLParser()
    parsed = parser.parse(content)
    parsed = replace_defines_in_documents(parsed)
    scheme_validator.validate(parsed)

    # Finally convert the config structure to CommandLine objects
    return dictionary_source.dictionaries_to_commandline(dictionaries)
