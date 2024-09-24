import json
import yaml

from . import utils
from . import dictionary_source
from .commandline import ExtendedBool

def str_to_yaml(s):
    return json.dumps(s)

def bool_to_yaml(b):
    return {True: 'true', False: 'false'}[b]

def option_to_yaml(obj):
    r = '- option_strings: %s\n' % json.dumps(obj['option_strings'])

    if 'metavar' in obj:
        r += '  metavar: %s\n' % str_to_yaml(obj['metavar'])

    if 'help' in obj:
        r += '  help: %s\n' % str_to_yaml(obj['help'])

    if obj.get('takes_args', True) is not True:
        try:
            r += '  takes_args: %s\n' % bool_to_yaml(obj['takes_args'])
        except: # takes_args may be "?"
            r += '  takes_args: %s\n' % str_to_yaml(obj['takes_args'])

    if 'group' in obj:
        r += '  group: %s\n' % str_to_yaml(obj['group'])

    if obj.get('multiple_option', ExtendedBool.INHERIT) !=  ExtendedBool.INHERIT:
        r += '  multiple_option: %s\n' % bool_to_yaml(obj['multiple_option'])

    if 'complete' in obj:
        r += '  complete: %s\n' % json.dumps(obj['complete'])

    if 'when' in obj:
        r += '  when: %s\n' % str_to_yaml(obj['when'])

    return r

def positional_to_yaml(obj):
    r = '- number: %d\n' % obj['number']

    if 'metavar' in obj:
        r += '  metavar: %s\n' % str_to_yaml(obj['metavar'])

    if 'help' in obj:
        r += '  help: %s\n' % str_to_yaml(obj['help'])

    if obj.get('repeatable', False) is not False:
        r += '  repeatable: %s\n' % bool_to_yaml(obj['repeatable'])

    if 'complete' in obj:
        r += '  complete: %s\n' % json.dumps(obj['complete'])

    if 'when' in obj:
        r += '  when: %s\n' % str_to_yaml(obj['when'])

    return r

def to_yaml(obj):
    r = ''
    r += 'prog: %s\n' % str_to_yaml(obj['prog'])

    if obj.get('aliases', []):
        r += 'aliases: %s\n' % json.dumps(obj['aliases'])

    if 'help' in obj:
        r += 'help: %s\n' % str_to_yaml(obj['help'])

    if obj.get('abbreviate_commands', ExtendedBool.INHERIT) != ExtendedBool.INHERIT:
        r += 'abbreviate_commands: %s\n' % bool_to_yaml(obj['abbreviate_commands'])

    if obj.get('abbreviate_options', ExtendedBool.INHERIT) != ExtendedBool.INHERIT:
        r += 'abbreviate_options: %s\n' % bool_to_yaml(obj['abbreviate_options'])

    if obj.get('inherit_options', ExtendedBool.INHERIT) != ExtendedBool.INHERIT:
        r += 'inherit_options: %s\n' % bool_to_yaml(obj['inherit_options'])

    if 'options' in obj:
        r += 'options:\n'
        for option in obj['options']:
            r += utils.indent(option_to_yaml(option), 2)
            r += '\n'

    if 'positionals' in obj:
        r += 'positionals:\n'
        for positional in obj['positionals']:
            r += utils.indent(positional_to_yaml(positional), 2)
            r += '\n'

    return r

def CommandLine_To_YAML(commandline):
    dictionaries = dictionary_source.CommandLine_To_Dictionaries(commandline)
    r = []

    for dictionary in dictionaries:
        r.append(to_yaml(dictionary))

    return '---\n'.join(r)

def load_from_file(file):
    with open(file, 'r') as fh:
        dictionaries = list(yaml.safe_load_all(fh))
        return dictionary_source.Dictionaries_To_Commandline(dictionaries)
