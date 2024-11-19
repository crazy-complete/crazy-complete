'''Algorithm functions.'''

def flatten(iterable):
    result = []
    for item in iterable:
        result.extend(item)
    return result

def uniq(iterable):
    result = []
    seen = set()
    for item in iterable:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result
