'''Algorithm functions.'''

def flatten(iterable):
    r = []
    for l in iterable:
        r.extend(l)
    return r

def uniq(iterable):
    r = []
    seen = set()
    for item in iterable:
        if item not in seen:
            seen.add(item)
            r.append(item)
    return r
