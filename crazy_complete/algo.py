'''Algorithm functions.'''

def flatten(iterable):
    '''Flatten a list of iterables into a single list.'''

    result = []
    for item in iterable:
        result.extend(item)
    return result

def uniq(iterable):
    '''Return list of unique items, preserving order.'''

    result = []
    seen = set()
    for item in iterable:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result
