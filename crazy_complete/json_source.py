"""
This module provides functions for creating CommandLine objects from JSON
and vice versa.
"""

import json
import jsonschema
from textwrap import indent
from pprint import pformat

from . import dictionary_source
from . import json_schema

class JSONSchemeError(Exception):
    pass

def load_from_file(file):
    with open(file, 'r', encoding='utf-8') as fh:
        dictionaries = json.load(fh)
        try:
            jsonschema.validate(
                instance=dictionaries,
                schema=json_schema.json_schema,
                format_checker=jsonschema.Draft202012Validator.FORMAT_CHECKER,
            )
        except jsonschema.exceptions.ValidationError as exc:
            if exc.validator == 'pattern' and 'option_strings' in exc.schema_path:
                # Print a custom error message in this specific scenario. The
                # failed regex error message can be cryptic.
                error_message = (
                    "The provided 'option_strings' flag is invalid! Use -f or "
                    "--flag style flags."
                )
            else:
                error_message = exc.message
            error_path = "".join(f'[{elem!r}]' for elem in exc.relative_path)
            instance = indent(pformat(exc.instance, sort_dicts=False), "    ")
            raise JSONSchemeError(
                f"'{file}' is malformed!\n"
                f'{error_message}\n\n'
                f'On {file}{error_path}:\n'
                f'{instance}'
            ) from exc
        return dictionary_source.dictionaries_to_commandline(dictionaries)

def commandline_to_json(commandline):
    dictionaries = dictionary_source.commandline_to_dictionaries(commandline)
    json_string = json.dumps(dictionaries, indent=None)
    return json_string
