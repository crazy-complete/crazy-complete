"""
This module provides functions for creating CommandLine objects from YAML
and vice versa.
"""

import json
import yaml
import strictyaml

from . import utils
from . import dictionary_source
from .cli import ExtendedBool
from .strictyaml_convert_schema import convert_jsonschema_to_strictyaml
from . import json_schema

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

class YAMLSchemeError(Exception):
    pass

def _extra_validation(input):
    '''Perform additional validation on input which can't be done with schema.

    This function may change input!

    Args:
        input (strictyaml.YAML): Input data.
    '''
    # WARNING: This MUST be kept in sync with `complete` validation in
    # json_schema.py!
    def validate_complete(input):
        from strictyaml import Enum, FixedSeq, Int, Map, MapPattern, Regex, Seq, Str

        if len(input) == 0:
            raise YAMLSchemeError(f"'complete' must not be empty! (line {input.start_line})")
        # Validate that the first element is valid (none, )
        input[0].revalidate(Enum(json_schema.completion_commands))
        match input[0].data:
            case 'file' | 'directory':
                if len(input) != 1:
                    input.revalidate(
                        FixedSeq((Str(), Map({"directory": Regex('.+')})))
                    )
            case 'choices':
                item_scheme = FixedSeq((Str(), Seq(Regex('.+'))))
                item_desc_scheme = FixedSeq((Str(), MapPattern(Regex('.+'), Regex('.+'), minimum_keys=1)))
                if len(input) == 1 or (not input[1].is_sequence()):
                    raise YAMLSchemeError(
                        f"A 'choices' complete must contain either a list of "
                        f"valid completions or a mapping with items and their "
                        f"descriptions! (line {input.start_line})"
                    )
                elif input[1].is_sequence():
                    input.revalidate(item_scheme)
                elif input[1].is_mapping():
                    input.revalidate(item_desc_scheme)
                else:
                    input.revalidate(item_desc_scheme | item_scheme)
                if input[1].is_sequence():
                    if len(input[1]) == 0:
                        raise YAMLSchemeError(f"Choices may not be empty in 'complete'! (line {input.start_line})")
            case 'value_list':
                input.revalidate(
                    FixedSeq((Str(), Map({"values": Seq(Str()) | MapPattern(Str(), Str(), minimum_keys=1)})))
                )
                if input[1]['values'].is_sequence() and len(input[1]['values']) == 0:
                    raise YAMLSchemeError(f"Values may not be empty in 'complete'! (line {input.start_line})")
            case 'exec':
                input.revalidate(FixedSeq((Str(), Str())))
            case 'range':
                input.revalidate(FixedSeq((Str(), Int(), Int())))
            case _:
                input.revalidate(FixedSeq((Str(),)))
    for option in input.get('options', ()):
        if len(option['option_strings']) == 0:
            raise YAMLSchemeError(f"'option_string' must contain at least one flag! (line {option['option_strings'].start_line})")
        if 'groups' in option and len(option['groups']) == 0:
            raise YAMLSchemeError(f"'groups' must contain at least one group! (line {option['option_strings'].start_line})")
        if "complete" in option:
            validate_complete(option['complete'])
    for positional in input.get('positionals', ()):
        number = positional['number']
        if number < 1:
            raise YAMLSchemeError(
                f"The 'number' of a positional argument in 'positionals' must "
                f"be positive! Got: {number} (line {number.start_line})"
            )
        if "complete" in option:
            validate_complete(option['complete'])
    if 'aliases' in option and len(option['aliases']) == 0:
        raise YAMLSchemeError(f"'aliases' must contain at least one alias! (line {option['option_strings'].start_line})")

def _load_yaml(input, filename, document_beginning):
    '''Load a YAML file and handle errors.

    Args:
        input (str): Input string.
        filename (str): Filename (used for diagnostics only).
        document_beginning (int): Starting line number of this document (useful
          if there are several documents in a single YAML file).

    Returns:
        dict: A parsed, validated and "Pythonified" dict representing a single
          (sub)command.
    '''
    try:
        curr_dict = strictyaml.dirty_load(
            input,
            schema=convert_jsonschema_to_strictyaml(json_schema.base_schema),
            label=filename,
            allow_flow_style=True,
        )
        _extra_validation(curr_dict)
        return curr_dict.data
    except (strictyaml.YAMLValidationError, YAMLSchemeError) as exc:
        # TODO: Add better error message for regex fail.
        errmsg = f"'{filename}' is malformed!"
        if document_beginning != 0:
            errmsg += (
                f' (line numbers are reported relative to the '
                f'current document, which starts on '
                f'line {document_beginning})'
            )
        raise YAMLSchemeError(errmsg + '\n' + str(exc)) from exc

def load_from_file(file):
    with open(file, 'r', encoding='utf-8') as fh:
        buffer = ""
        dictionaries = []
        document_beginning = 0
        # Read the file line by line and look out for the end of document (---)
        # YAML markers. strictyaml doesn't have a builting way to read multiple
        # documents at once: https://github.com/crdoconnor/strictyaml/issues/210
        for lineno, line in enumerate(fh):
            if line == '---\n':
                dictionaries.append(_load_yaml(buffer, file, document_beginning))
                document_beginning = lineno + 1
                buffer = ''
            else:
                buffer += line
        if buffer:
            dictionaries.append(_load_yaml(buffer, file, document_beginning))
        return dictionary_source.dictionaries_to_commandline(dictionaries)
