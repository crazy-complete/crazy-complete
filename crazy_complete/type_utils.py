'''Type utility functions.'''

from types import NoneType

from .errors import CrazyTypeError


def is_dict_type(obj):
    '''Return if `obj` is a dictionary type.'''

    return hasattr(obj, 'items')


def is_list_type(obj):
    '''Return if `obj` is list or tuple.'''

    return isinstance(obj, (list, tuple))


def validate_type(value, types, parameter_name):
    '''Check if `value` is one of `types`.'''

    if not isinstance(value, types):
        types_strings = []
        for t in types:
            types_strings.append({
                str:      'str',
                int:      'int',
                float:    'float',
                list:     'list',
                tuple:    'tuple',
                dict:     'dict',
                bool:     'bool',
                NoneType: 'None'}[t])
        types_string = '|'.join(types_strings)

        raise CrazyTypeError(parameter_name, types_string, value)
