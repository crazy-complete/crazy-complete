'''JSON schemas used for the input JSON file.

This schema is also used indirectly in YAML file loading, see
strictyaml_convert_schema for more info.

Variables:
    completion_commands (frozenset): A set of all valid completion commands
      (documented in commands.md). These specify the valid values of the first
      element of the `complete` key in the subdicts of `positionals` and
      `options`.
    base_schema (dict): Base schema for validating input files. Note that
      completions read from the --help parser and from argparse (Python) are
      handled separately. This schema is shared between the JSON and YAML
      validators. Some validation is not present, because it is not convertible
      to YAML and has to be checked manually.
    json_schema (dict): base_schema extended by JSON only checks. If an input
      JSON file passes this schema, it should be valid (some specific things
      cannot be effectively validated by a schema, so some checks are still
      required).
'''

# https://json-schema.org/understanding-json-schema

import copy

# All valid complete commands for the `options` and `positionals` keys.
completion_commands = frozenset((
    'none',
    'file',
    'directory',
    'choices',
    'value_list',
    'exec',
    'range',
    'signal',
    'process',
    'pid',
    'command',
    'user',
    'group',
    'service',
    'variable',
    'environment',
))

# A helper schema for a nonempty string. It is used in several places.
_nonempty_string = {'type': 'string', 'minLength': 1}
# A nonempty array of `_nonempty_string`s
_nonempty_string_array = {
    'type': 'array',
    'items': _nonempty_string,
    # WARNING: `minItems` is ignored by strictyaml validator! It has to be
    # enforced manually in YAML!
    'minItems': 1,
}

# See documentation.md for the description of these fields
# This is the schema for a singe `prog` entry. It is reused in
# strictyaml_convert_schema to generate a strictyaml schema.
base_schema = {
    'type': 'object',
    'properties': {
        'prog': _nonempty_string,
        'aliases': _nonempty_string_array,
        # TODO: Can this be empty?
        'help': {'type': 'string'},
        'options': {
            'type': 'array',
            'items': {
                'type': 'object',
                'properties': {
                    'option_strings': {
                        'type': 'array',
                        'items': {
                            'type': 'string',
                            # valid:
                            # -a
                            # --flag
                            # invalid:
                            # text
                            # -
                            # --
                            # --fla,g
                            'pattern': r'^-(?:(?:[^\s,-]+[^\s,]*)|(?:-[^\s,]+))$'
                        },
                        # WARNING: `minItems` is ignored by strictyaml
                        # validator! It has to be enforced manually!
                        'minItems': 1
                    },
                    # TODO: Can this be empty?
                    'metavar': {'type': 'string'},
                    # TODO: Can this be empty?
                    'help': {'type': 'string'},
                    'optional_arg': {'type': 'boolean'},
                    # Proper handling of `complete` is too complicated to be
                    # handled by strictyaml_convert_schema.py. It is handled
                    # below for JSON only.
                    'complete': {
                        'type': 'array',
                        'items': {}
                    },
                    'repeatable': {'type': 'boolean'},
                    # This is deprecated, see crazy_complete/compat.py
                    'multiple_option': {'type': 'boolean'},
                    'final': {'type': 'boolean'},
                    'hidden': {'type': 'boolean'},
                    'groups': {
                        'type': 'array',
                        'items': {'type': 'string'}
                    },
                    # This is deprecated, see crazy_complete/compat.py
                    'group': {
                        'type': 'array',
                        'items': {'type': 'string'}
                    },
                    'when': {'type': 'string'}
                    # TODO: Are 'abbreviate_commands', 'abbreviate_options'
                    # and 'inherit_options' also allowed? They aren't
                    # documented.
                },
                'required': ['option_strings'],
                'additionalProperties': False
            }
        },
        'positionals': {
            'type': 'array',
            'items': {
                'type': 'object',
                'properties': {
                    'number': {'type': 'integer'},
                    'metavar': {'type': 'string'},
                    'help': {'type': 'string'},
                    'repeatable': {'type': 'boolean'},
                    # See above.
                    'complete': {
                        'type': 'array',
                        'items': {}
                    },
                    'when': {'type': 'string'}
                },
                'required': ['number'],
                'additionalProperties': False
            }
        }
    },
    'required': ['prog'],
    'additionalProperties': False
}

# _json_base_schema includes checks which can be done using JSON schema but
# cannot be converted to strictyaml.
_json_base_schema = copy.deepcopy(base_schema)
_nonempty_array_or_dict = {
    'anyOf': [
        {
            'type': 'array',
            'items': _nonempty_string,
            'minItems': 1
        },
        {
            'type': 'object',
            'patternProperties': {
                '.*': _nonempty_string
            },
            'minProperties': 1,
            'additionalProperties': False
        }
    ]
}
# WARNING: This MUST be kept in sync with `complete` validation in
# yaml_source.py!
_complete_schema = {
    'anyOf': [
        {
            'type': 'array',
            'prefixItems': [
                {'enum': ['file', 'directory']},
                {
                    'type': 'object',
                    'properties': {
                        'directory': _nonempty_string
                    }
                }
            ],
            'unevaluatedItems': False
        },
        {
            'type': 'array',
            'prefixItems': [
                {'enum': ['choices']},
                _nonempty_array_or_dict
            ],
            'unevaluatedItems': False
        },
        {
            'type': 'array',
            'prefixItems': [
                {'enum': ['value_list']},
                {
                    'type': 'object',
                    'properties': {
                        'values': _nonempty_array_or_dict
                    },
                    'additionalProperties': False
                }
            ],
            'unevaluatedItems': False
        },
        {
            'type': 'array',
            'prefixItems': [
                {'enum': ['exec']},
                _nonempty_string
            ],
            'unevaluatedItems': False
        },
        {
            'type': 'array',
            'prefixItems': [
                {'enum': ['range']},
                # TODO: Allowed ranges?
                {'type': 'integer'},
                {'type': 'integer'}
            ],
            'unevaluatedItems': False
        },
        {
            'type': 'array',
            'prefixItems': [
                {'enum': list(completion_commands - {'choices', 'value_list', 'exec', 'range'})},
            ],
            'unevaluatedItems': False
        }
    ]
}
_json_base_schema['properties']['options']['items']['properties']['complete']['items'] = _complete_schema
_json_base_schema['properties']['positionals']['items']['properties']['complete']['items'] = _complete_schema
_json_base_schema['properties']['positionals']['items']['properties']['number']['minimum'] = 1

# Finalized JSON schema.
json_schema = {
    'type': 'array',
    'items': _json_base_schema
}
