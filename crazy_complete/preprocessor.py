''' Contains code for preprocessing text '''

def preprocess(string, defines):
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
            if stack.pop() == False:
                ignore = False if len(stack) == 0 else not any(stack)
        else:
            if not ignore:
                output.append(line)

    return ''.join(output)

def strip_double_empty_lines(string):
    return string.replace('\n\n\n', '\n\n')

if __name__ == '__main__':
    input_str = """\
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

    result = preprocess(input_str, defines)
    print(result)
