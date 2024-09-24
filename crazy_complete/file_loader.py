import os
import sys
import importlib
import tempfile
import __main__

def execute_file(file):
    ''' Import file using exec '''

    with open(os.devnull, 'w') as null_fh:
        sys.stdout = null_fh
        sys.stderr = null_fh

        with open(file, 'r') as fh:
            source = fh.read()
            compiled = compile(source, file, 'exec')
            try:
                # pylint: disable=exec-used
                exec(compiled, globals())
            except SystemExit:
                pass

    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__

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
