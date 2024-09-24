import json

from . import dictionary_source

def load_from_file(file):
    with open(file, 'r') as fh:
        dictionaries = json.load(fh)
        return dictionary_source.Dictionaries_To_Commandline(dictionaries)

def CommandLine_To_JSON(commandline):
    dictionaries = dictionary_source.CommandLine_To_Dictionaries(commandline)
    json_string = json.dumps(dictionaries, indent=None)
    return json_string
