"""
This module provides functions for creating CommandLine objects from JSON
and vice versa.
"""

import json

from . import dictionary_source

def load_from_file(file):
    '''Load a JSON file and turn it into a cli.CommandLine object.'''

    with open(file, 'r', encoding='utf-8') as fh:
        dictionaries = json.load(fh)
        return dictionary_source.dictionaries_to_commandline(dictionaries)

def commandline_to_json(commandline):
    '''Convert a cli.CommandLine object into JSON.'''

    dictionaries = dictionary_source.commandline_to_dictionaries(commandline)
    json_string = json.dumps(dictionaries, indent=None)
    return json_string
