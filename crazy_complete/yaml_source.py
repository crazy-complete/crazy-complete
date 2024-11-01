"""
This module provides functions for creating CommandLine objects from YAML
and vice versa.
"""

import json
import yaml

from . import utils
from . import dictionary_source
from .cli import ExtendedBool

def option_to_yaml(dictionary):
    option_strings  = dictionary['option_strings']
    metavar         = dictionary.get('metavar',         None)
    help            = dictionary.get('help',            None)
    optional_arg    = dictionary.get('optional_arg',    False)
    groups          = dictionary.get('groups',          None)
    repeatable      = dictionary.get('repeatable',      ExtendedBool.INHERIT)
    final           = dictionary.get('final',           False)
    hidden          = dictionary.get('hidden',          False)
    complete        = dictionary.get('complete',        None)
    when            = dictionary.get('when',            None)

    r = '- option_strings: %s\n' % json.dumps(option_strings)

    if metavar is not None:
        r += '  metavar: %s\n' % json.dumps(metavar)

    if help is not None:
        r += '  help: %s\n' % json.dumps(help)

    if optional_arg is True:
        r += '  optional_arg: %s\n' % json.dumps(optional_arg)

    if groups is not None:
        r += '  groups: %s\n' % json.dumps(groups)

    if repeatable != ExtendedBool.INHERIT:
        r += '  repeatable: %s\n' % json.dumps(repeatable)

    if final is not False:
        r += '  final: %s\n' % json.dumps(final)

    if hidden is not False:
        r += '  hidden: %s\n' % json.dumps(hidden)

    if complete is not None:
        r += '  complete: %s\n' % json.dumps(complete)

    if when is not None:
        r += '  when: %s\n' % json.dumps(when)

    return r.rstrip()

def positional_to_yaml(dictionary):
    number     = dictionary['number']
    metavar    = dictionary.get('metavar',    None)
    help       = dictionary.get('help',       None)
    repeatable = dictionary.get('repeatable', False)
    complete   = dictionary.get('complete',   None)
    when       = dictionary.get('when',       None)

    r = '- number: %d\n' % number

    if metavar is not None:
        r += '  metavar: %s\n' % json.dumps(metavar)

    if help is not None:
        r += '  help: %s\n' % json.dumps(help)

    if repeatable is not False:
        r += '  repeatable: %s\n' % json.dumps(repeatable)

    if complete is not None:
        r += '  complete: %s\n' % json.dumps(complete)

    if when is not None:
        r += '  when: %s\n' % json.dumps(when)

    return r.rstrip()

def to_yaml(dictionary):
    prog                = dictionary['prog']
    aliases             = dictionary.get('aliases',             None)
    help                = dictionary.get('help',                None)
    abbreviate_commands = dictionary.get('abbreviate_commands', ExtendedBool.INHERIT)
    abbreviate_options  = dictionary.get('abbreviate_options',  ExtendedBool.INHERIT)
    inherit_options     = dictionary.get('inherit_options',     ExtendedBool.INHERIT)
    options             = dictionary.get('options',             None)
    positionals         = dictionary.get('positionals',         None)

    r = 'prog: %s\n' % json.dumps(prog)

    if aliases is not None:
        r += 'aliases: %s\n' % json.dumps(aliases)

    if help is not None:
        r += 'help: %s\n' % json.dumps(help)

    if abbreviate_commands != ExtendedBool.INHERIT:
        r += 'abbreviate_commands: %s\n' % json.dumps(abbreviate_commands)

    if abbreviate_options != ExtendedBool.INHERIT:
        r += 'abbreviate_options: %s\n' % json.dumps(abbreviate_options)

    if inherit_options != ExtendedBool.INHERIT:
        r += 'inherit_options: %s\n' % json.dumps(inherit_options)

    if options:
        r += 'options:\n'
        for option in options:
            r += utils.indent(option_to_yaml(option), 2)
            r += '\n\n'

    if positionals:
        r += 'positionals:\n'
        for positional in positionals:
            r += utils.indent(positional_to_yaml(positional), 2)
            r += '\n\n'

    return r.rstrip()

def commandline_to_yaml(commandline):
    dictionaries = dictionary_source.commandline_to_dictionaries(commandline)
    r = []

    for dictionary in dictionaries:
        r.append(to_yaml(dictionary))

    return '\n---\n'.join(r)

def load_from_file(file):
    with open(file, 'r', encoding='utf-8') as fh:
        dictionaries = list(yaml.safe_load_all(fh))
        return dictionary_source.dictionaries_to_commandline(dictionaries)
