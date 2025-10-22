'''Classes for including functions in the generation process.'''

from . import cli
from . import shell
from . import preprocessor
from .str_utils import indent


# pylint: disable=too-few-public-methods


class FunctionBase:
    '''Base class for functions.'''

    def __init__(self, funcname, code, dependencies=None):
        self.funcname = funcname
        self.code = code.strip()
        self.dependencies = dependencies if dependencies else []

    def get_code(self):
        '''Return the whole function.'''
        raise NotImplementedError


class ShellFunction(FunctionBase):
    '''Class for generating Bash and Zsh functions.'''

    def get_code(self, funcname=None, defines=frozenset()):
        if funcname is None:
            funcname = self.funcname

        code = self.code.replace('%FUNCNAME%', funcname)
        code = preprocessor.preprocess(code, defines)
        code = preprocessor.strip_double_empty_lines(code)

        r  = '%s() {\n' % funcname
        r += '%s\n'     % indent(code, 2).rstrip()
        r += '}'
        return r


class FishFunction(FunctionBase):
    '''Class for generating Fish functions.'''

    def get_code(self, funcname=None, defines=frozenset()):
        if funcname is None:
            funcname = self.funcname

        code = self.code.replace('%FUNCNAME%', funcname)
        code = preprocessor.preprocess(code, defines)
        code = preprocessor.strip_double_empty_lines(code)

        r  = 'function %s\n' % funcname
        r += '%s\n'          % indent(code, 2).rstrip()
        r += 'end'
        return r


def make_completion_funcname_for_context(ctxt, progname):
    '''TODO.'''

    commandlines = ctxt.commandline.get_parents(include_self=True)
    prognames = [p.prog for p in commandlines]
    prognames[0] = progname

    funcname = shell.make_identifier('_'.join(prognames))

    if isinstance(ctxt.option, cli.Option):
        return '_%s__%s' % (funcname, ctxt.option.option_strings[0])
    if isinstance(ctxt.option, cli.Positional):
        if ctxt.option.metavar:
            identifier = shell.make_identifier(ctxt.option.metavar)
        else:
            identifier = 'arg%d' % ctxt.option.get_positional_num()

        return '_%s__%s' % (funcname, identifier)

    raise AssertionError('make_completion_funcname_for_context: Should not be reached')


class GeneralHelpers:
    '''Class for including functions in the generation process.'''

    def __init__(self, function_prefix, function_class):
        self.function_prefix = function_prefix
        self.function_class = function_class

        # Dynamic functions
        self.dynamic_functions_code_to_funcname = {}

        # Builtin functins
        self.functions = {}
        self.used_functions = {} # funcname:set(defines)
        self.global_defines = set()

    # =========================================================================
    # Dynamic functions
    # =========================================================================

    def add_dynamic_func(self, ctxt, code):
        '''Add dynamically generated function.'''

        try:
            return self.dynamic_functions_code_to_funcname[code]
        except KeyError:
            funcname = self.get_dynamic_funcname(ctxt)
            self.dynamic_functions_code_to_funcname[code] = funcname
            return funcname

    def get_dynamic_funcname(self, ctxt):
        '''Return a unique function name for `ctxt`.'''

        funcname = make_completion_funcname_for_context(ctxt, self.function_prefix)
        num = 0
        funcname_plus_num = funcname
        while funcname_plus_num in self.dynamic_functions_code_to_funcname.values():
            funcname_plus_num = '%s%d' % (funcname, num)
            num += 1
        return funcname_plus_num

    def get_all_dynamic_functions(self):
        '''Return a list of code for all dynamically defined functions.'''

        r = []
        for code, funcname in self.dynamic_functions_code_to_funcname.items():
            r.append(self.function_class(funcname, code).get_code())
        return r

    # =========================================================================
    # Builtin functions
    # =========================================================================

    def add_function(self, function):
        '''Add a function to the function repository.'''

        assert isinstance(function, FunctionBase), \
            "GeneralHelpers.add_function: function: expected FunctionBase, got %r" % function

        self.functions[function.funcname] = function

    def define(self, name):
        '''Define a macro on global scope.'''

        self.global_defines.add(name)

    def use_function(self, function_name, *defines):
        '''Use a function from the function repository.'''

        if function_name not in self.functions:
            raise KeyError('No such function: %r' % function_name)

        if function_name not in self.used_functions:
            self.used_functions[function_name] = set(defines)
        else:
            self.used_functions[function_name].update(defines)

        # Add dependencies
        for function in self.functions[function_name].dependencies:
            self.use_function(function)

        return self.get_real_function_name(function_name)

    def get_real_function_name(self, function_name):
        '''Return the function name with its prefix.'''

        return '_%s__%s' % (self.function_prefix, function_name)

    def is_used(self, function_name):
        '''Check if a function is used.'''

        return function_name in self.used_functions

    def get_used_functions_code(self):
        '''Return a list of code for all used functions.'''

        r = []

        for funcname, defines in self.used_functions.items():
            function = self.functions[funcname]
            realname = self.get_real_function_name(funcname)
            code = function.get_code(realname, self.global_defines | defines)

            for dep_func in function.dependencies:
                code = code.replace(dep_func, self.get_real_function_name(dep_func))

            r.append(code)

        r.extend(self.get_all_dynamic_functions())

        return r
