'''Contains code for preprocessing text.'''

def preprocess(string, defines):
    '''Simple preprocessor function.'''

    defines = set(defines)
    output = []
    stack = []

    lines = string.splitlines(keepends=True)
    ignore = False

    for line in lines:
        stripped_line = line.lstrip()
        if stripped_line.startswith("#ifdef"):
            define = stripped_line.split()[1]
            if define in defines:
                stack.append(True)
            else:
                stack.append(False)
                ignore = True
        elif stripped_line.startswith("#endif"):
            if stack.pop() is False:
                ignore = False if len(stack) == 0 else not any(stack)
        else:
            if not ignore:
                output.append(line)

    return ''.join(output)

def strip_double_empty_lines(string):
    '''Collapse triple newlines into double newlines.'''

    return string.replace('\n\n\n', '\n\n')

def _test():
    string = """\
Lorem Ipsum
#ifdef DEBUG
    This is debug code.
    #ifdef FOO
    This is foo code.
    #endif
#endif
Dolor Sit Amet\
"""
    defines = ["DEBUG"]
    result = preprocess(string, defines)
    print(result)

if __name__ == '__main__':
    _test()
