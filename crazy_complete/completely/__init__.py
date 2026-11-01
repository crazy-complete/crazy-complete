# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2025-2026 Benjamin Abendroth <braph93@gmx.de>

'''
This module converts `completely` completion configs (pattern, flat or nested
format) to a crazy-complete `CommandLine`.
'''

import yaml

from .. import dictionary_source, scheme_validator, yaml_source
from ..errors import CrazyError
from ..extended_yaml_parser import ExtendedYAMLParser
from . import common, flat, pattern


def detect(config):
    '''Pick the converter for `config`: configs with a `patterns` list use
    the pattern format, everything else the flat/nested format.  '''

    if isinstance(config, dict) and isinstance(config.get('patterns'), list):
        return pattern
    return flat


def validate_roundtrip(dictionaries):
    '''Round-trip the converted dictionaries through the crazy-complete
    validator to make sure they describe a valid command line.  '''

    content = '\n---\n'.join(
        yaml_source.to_yaml(dictionary) for dictionary in dictionaries)

    parser = ExtendedYAMLParser()
    parsed = parser.parse(content)

    if not isinstance(parsed, list):
        parsed = [parsed]

    scheme_validator.validate(parsed)


def load_from_file(file):
    '''Load a completely config file and convert it to a CommandLine.'''

    with open(file, 'r', encoding='utf-8') as fh:
        try:
            config = yaml.safe_load(fh)
        except yaml.YAMLError as e:
            raise CrazyError('Invalid YAML: ' + e) from e

    if config is None:
        raise CrazyError('The config file is empty')

    converter = detect(config)
    root = converter.convert(config)
    dictionaries = common.node_to_dictionaries(root)
    validate_roundtrip(dictionaries)

    return dictionary_source.dictionaries_to_commandline(dictionaries)


__all__ = ['load_from_file']
