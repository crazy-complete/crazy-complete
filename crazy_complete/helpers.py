#!/usr/bin/python3

from . import utils

class FunctionBase():
    def __init__(self, funcname, code):
        self.funcname = funcname
        self.code = code.strip()

    def get_code(self):
        raise NotImplementedError

class ShellFunction(FunctionBase):
    def get_code(self, funcname=None):
        if funcname is None:
            funcname = self.funcname

        r  = '%s() {\n' % funcname
        r += '%s\n'     % utils.indent(self.code, 2).rstrip()
        r += '}'
        return r

class FishFunction(FunctionBase):
    def get_code(self, funcname=None):
        if funcname is None:
            funcname = self.funcname

        r  = 'function %s\n' % funcname
        r += '%s\n'          % utils.indent(self.code, 2).rstrip()
        r += 'end'
        return r

class GeneralHelpers():
    def __init__(self, function_prefix):
        self.function_prefix = function_prefix
        self.functions = dict()
        self.used_functions = list()

    def get_real_function_name(self, function_name):
        return '_%s_%s' % (self.function_prefix, function_name)

    def add_function(self, function):
        assert isinstance(function, FunctionBase), "GeneralHelpers.add_function: function: expected FunctionBase, got %r" % function
        self.functions[function.funcname] = function

    def use_function(self, function_name):
        if function_name not in self.functions:
            raise KeyError('No such function: %r' % function_name)

        # Code deduplication. If we saw a function with the same code,
        # return its funcname.
        # (Currently only used for zsh completion generator)
        for function in self.used_functions:
            if self.functions[function_name].code == self.functions[function].code:
                return self.get_real_function_name(function)

        if function_name not in self.used_functions:
            self.used_functions.append(function_name)

        return self.get_real_function_name(function_name)

    def is_used(self, function_name):
        return function_name in self.used_functions

    def get_used_functions_code(self):
        r = []
        for funcname in self.used_functions:
            r.append(self.functions[funcname].get_code(self.get_real_function_name(funcname)))
        return r
