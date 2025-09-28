'''Type utility functions.'''

def is_dict_type(obj):
    '''Return if `obj` is a dictionary type.'''

    return hasattr(obj, 'items')

def is_list_type(obj):
    '''Return if `obj` is list or tuple.'''

    return isinstance(obj, (list, tuple))
