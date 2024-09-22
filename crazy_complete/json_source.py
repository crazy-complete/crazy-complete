import json

from .dictionary_source import *

def load_from_file(file):
    with open(file, 'r') as fh:
        dictionaries = json.load(fh)
        return Dictionaries_To_Commandline(dictionaries)

def CommandLine_To_JSON(commandline):
    dictionaries = CommandLine_To_Dictionaries(commandline)
    json_string = json.dumps(dictionaries, indent=None)
    return json_string

