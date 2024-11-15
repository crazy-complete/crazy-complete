'''Module for converting JSON schema into strictyaml compatible format.'''
from strictyaml import Any, Bool, Int, Map, Optional, Regex, Seq, Str

# https://hitchdev.com/strictyaml/using/

def convert_jsonschema_to_strictyaml(input):
    '''Convert JSON schema into strictyaml format.

    Args:
        input: A JSON schema compatible dict.

    Returns:
        Any: A strictyaml compatible scheme.
    '''
    # This function is recursive.
    if input == {}:
        return Any()
    match input['type']:
        case 'object':
            if input.get('additionalProperties', None) is not False:
                # We assume that dictionaries only allow the listed keys.
                raise NotImplementedError()
            required = set(input.get('required', ()))
            result = {}
            for prop, value in input['properties'].items():
                if prop in required:
                    result[prop] = convert_jsonschema_to_strictyaml(value)
                else:
                    result[Optional(prop)] = convert_jsonschema_to_strictyaml(value)
            return Map(result)
        case 'array':
            # WARNING: This has to be checked manually!
            # if 'minItems' in input:
            #     raise NotImplementedError()
            return Seq(convert_jsonschema_to_strictyaml(input['items']))
        case 'string':
            if 'pattern' in input:
                return Regex(input['pattern'])
            else:
                return Str()
        case 'boolean':
            return Bool()
        case 'integer':
            return Int()
        case _:
            raise NotImplementedError()
