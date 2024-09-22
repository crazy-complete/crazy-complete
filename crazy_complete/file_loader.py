#!/usr/bin/python3

import os
import sys
import importlib
import tempfile

DEV_NULL_FH = open(os.devnull, 'w')

def close_output_streams():
    sys.stdout = sys.stderr = DEV_NULL_FH

def restore_output_streams():
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__

def execute_file(file):
    ''' Import file using exec '''

    import __main__

    close_output_streams()

    with open(file, 'r') as fh:
        source = fh.read()
        compiled = compile(source, file, 'exec')
        try:
            exec(compiled, globals())
        except SystemExit:
            pass

    restore_output_streams()

    return __main__

def import_file(file):
    ''' Import file using importlib '''

    directory, filename = os.path.split(file)
    if filename.lower().endswith('.py'):
        module_name = filename[:-3]
    else:
        temp = tempfile.NamedTemporaryFile(mode='w', suffix='.py')
        with open(file, 'r') as fh:
            temp.file.write(fh.read())
            temp.flush()

        directory, file = os.path.split(temp.name)
        module_name = file[:-3]

    if not directory:
        directory = '.'

    if directory not in sys.path:
        sys.path.append(directory)

    return importlib.import_module(module_name)

