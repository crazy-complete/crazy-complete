'''Contains code for preprocessing text.'''


def preprocess(string, defines):
    '''Simple preprocessor function with #ifdef, #else, and #endif support.'''

    defines = set(defines)
    output = []
    stack = []  # stack of booleans: is this block currently active?

    lines = string.splitlines(keepends=True)

    for line in lines:
        stripped_line = line.lstrip()

        if stripped_line.startswith("#ifdef"):
            define = stripped_line.split()[1]
            active = define in defines
            stack.append(active)

        elif stripped_line.startswith("#else"):
            if not stack:
                raise SyntaxError("#else without #ifdef")
            # flip only the current (top of stack)
            stack[-1] = not stack[-1]

        elif stripped_line.startswith("#endif"):
            if not stack:
                raise SyntaxError("#endif without #ifdef")
            stack.pop()

        else:
            # output only if all enclosing blocks are active
            if not stack or all(stack):
                output.append(line)

    if stack:
        raise SyntaxError("Unclosed #ifdef")

    return ''.join(output)


def _test():
    string = """\
Lorem Ipsum
#ifdef DEBUG
    This is debug code.
    #ifdef FOO
    This is foo code.
    #else
    This is foo else code.
    #endif
#endif
Dolor Sit Amet\
"""
    defines = ["DEBUG"]
    result = preprocess(string, defines)
    print(result)


if __name__ == '__main__':
    _test()
