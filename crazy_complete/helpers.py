''' Classes for including functions in the generation process '''

from . import utils
from . import preprocessor

class FunctionBase:
    def __init__(self, funcname, code):
        self.funcname = funcname
        self.code = code.strip()

    def get_code(self):
        raise NotImplementedError

class ShellFunction(FunctionBase):
    def get_code(self, funcname=None, defines=set()):
        if funcname is None:
            funcname = self.funcname

        code = self.code.replace('%FUNCNAME%', funcname)
        code = preprocessor.preprocess(code, defines)
        code = preprocessor.strip_double_empty_lines(code)

        r  = '%s() {\n' % funcname
        r += '%s\n'     % utils.indent(code, 2).rstrip()
        r += '}'
        return r

class FishFunction(FunctionBase):
    def get_code(self, funcname=None, defines=set()):
        if funcname is None:
            funcname = self.funcname

        code = self.code.replace('%FUNCNAME%', funcname)
        code = preprocessor.preprocess(code, defines)
        code = preprocessor.strip_double_empty_lines(code)

        r  = 'function %s\n' % funcname
        r += '%s\n'          % utils.indent(code, 2).rstrip()
        r += 'end'
        return r

class GeneralHelpers:
    def __init__(self, function_prefix):
        self.function_prefix = function_prefix
        self.functions = {}
        self.used_functions = {} # funcname:set(defines)

    def get_real_function_name(self, function_name):
        return '_%s_%s' % (self.function_prefix, function_name)

    def add_function(self, function):
        assert isinstance(function, FunctionBase), \
            "GeneralHelpers.add_function: function: expected FunctionBase, got %r" % function

        self.functions[function.funcname] = function

    def use_function(self, function_name, *defines):
        if function_name not in self.functions:
            raise KeyError('No such function: %r' % function_name)

        # Code deduplication. If we saw a function with the same code,
        # return its funcname.
        # (Currently only used for zsh completion generator)
        for function in self.used_functions.keys():
            if self.functions[function_name].code == self.functions[function].code:
                self.used_functions[function].update(defines)
                return self.get_real_function_name(function)

        if function_name not in self.used_functions:
            self.used_functions[function_name] = set(defines)

        return self.get_real_function_name(function_name)

    def is_used(self, function_name):
        return function_name in self.used_functions

    def get_used_functions_code(self):
        r = []
        for funcname, defines in self.used_functions.items():
            r.append(self.functions[funcname].get_code(
                self.get_real_function_name(funcname), defines))
        return r
