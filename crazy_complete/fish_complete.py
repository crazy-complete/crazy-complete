'''This module contains code for completing arguments in Fish.'''

from . import shell
from . import helpers

class FishCompletionBase:
    def get_args(self):
        '''Return a list of arguments to be appended to the `complete`
        command in FISH.

        The returned arguments should be in raw form, without any escaping.
        Escaping will be handled at a later stage.
        '''
        raise NotImplementedError

    def get_code(self):
        '''Return the code that can be used for completing an argument.'''
        raise NotImplementedError

class FishCompleteNone(FishCompletionBase):
    def get_args(self):
        return ['-f']

    def get_code(self):
        return ''

class FishCompletionCommand(FishCompletionBase):
    '''Class for executing a command and parsing its output.'''
    def  __init__(self, command):
        self.command = command

    def get_code(self):
        return self.command

    def get_args(self):
        return ['-f', '-a', '(%s)' % self.command]

class FishCompleteChoices(FishCompletionBase):
    def __init__(self, ctxt, choices):
        self.ctxt = ctxt
        self.choices = choices

    def get_args(self):
        if hasattr(self.choices, 'items'):
            code = self.get_code()
            funcname = self.ctxt.helpers.get_unique_function_name(self.ctxt)
            self.ctxt.helpers.add_function(helpers.FishFunction(funcname, code))
            funcname = self.ctxt.helpers.use_function(funcname)
            return ['-f', '-a', '(%s)' % funcname]
        else:
            return ['-f', '-a', ' '.join(shell.escape(str(c)) for c in self.choices)]

    def get_code(self):
        if hasattr(self.choices, 'items'):
            code = "printf '%s\\t%s\\n' \\\n"
            for item, description in self.choices.items():
                code += '  %s %s \\\n' % (shell.escape(str(item)), shell.escape(str(description)))
            return code.rstrip(' \\\n')
        else:
            code = "printf '%s\\n' \\\n"
            for item in self.choices:
                code += '  %s \\\n' % (shell.escape(str(item)))
            return code.rstrip(' \\\n')

class FishCompleteFileDir(FishCompletionBase):
    def __init__(self, ctxt, mode, opts):
        self.ctxt = ctxt
        self.mode = mode
        self.directory = None

        if opts is not None:
            self.directory = opts.get('directory', None)

    def get_args(self):
        if self.mode == 'file':
            if self.directory is not None:
                funcname = self.ctxt.helpers.use_function('fish_complete_filedir')
                return ['-f', '-a', '(%s -C %s)' % (funcname, shell.escape(self.directory))]

            return ['-F']
        elif self.mode == 'directory':
            if self.directory is not None:
                funcname = self.ctxt.helpers.use_function('fish_complete_filedir')
                return ['-f', '-a', '(%s -D -C %s)' % (funcname, shell.escape(self.directory))]

            return ['-f', '-a', '(__fish_complete_directories)']

    def get_code(self):
        if self.mode == 'file':
            funcname = self.ctxt.helpers.use_function('fish_complete_filedir')

            if self.directory is not None:
                return '%s -C %s' % (funcname, shell.escape(self.directory))
            else:
                return '%s' % funcname
        elif self.mode == 'directory':
            if self.directory is not None:
                funcname = self.ctxt.helpers.use_function('fish_complete_filedir')
                return '%s -D -C %s' % (funcname, shell.escape(self.directory))

            return '__fish_complete_directories'

class FishCompleteValueList:
    def __init__(self, ctxt, opts):
        separator = opts.get('separator', ',')
        values = opts['values']
        funcname = ctxt.helpers.get_unique_function_name(ctxt)

        if hasattr(values, 'items'):
            code = "printf '%s\\t%s\\n' \\\n"
            for item, desc in values.items():
                code += '  %s %s \\\n' % (shell.escape(item), shell.escape(desc))
            code = code.rstrip(' \\\n')
        else:
            code = "printf '%s\\n' \\\n"
            for value in values:
                code += '  %s \\\n' % shell.escape(value)
            code = code.rstrip(' \\\n')

        ctxt.helpers.add_function(helpers.FishFunction(funcname, code))
        funcname = ctxt.helpers.use_function(funcname)

        self.cmd = '__fish_complete_list %s %s' % (shell.escape(separator), funcname)

    def get_args(self):
        return ['-f', '-a', '(%s)' % self.cmd]

    def get_code(self):
        return self.cmd

class FishCompleteCombine:
    def __init__(self, ctxt, completer, commands):
        self.ctxt = ctxt
        self.code = []

        for command_args in commands:
            command, *args = command_args
            obj = getattr(completer, command)(ctxt, *args)
            self.code.append(obj.get_code())

    def get_code(self):
        return '\n'.join(self.code)

    def get_args(self):
        code_is_singleline = True
        for code in self.code:
            if '\n' in code:
                code_is_singleline = False

        if code_is_singleline:
            return ['-f', '-a', '(%s)' % '; '.join(self.code)]
        else:
            code = '\n'.join(self.code)
            funcname = self.ctxt.helpers.get_unique_function_name(self.ctxt)
            self.ctxt.helpers.add_function(helpers.FishFunction(funcname, code))
            return ['-f', '-a', '(%s)' % self.ctxt.helpers.use_function(funcname)]

class FishCompleter(shell.ShellCompleter):
    def none(self, ctxt, *a):
        return FishCompleteNone()

    def integer(self, ctxt, *a):
        return FishCompleteNone()

    def float(self, ctxt, *a):
        return FishCompleteNone()

    def choices(self, ctxt, choices):
        return FishCompleteChoices(ctxt, choices)

    def command(self, ctxt):
        return FishCompletionCommand("__fish_complete_command")

    def directory(self, ctxt, opts=None):
        return FishCompleteFileDir(ctxt, 'directory', opts)

    def file(self, ctxt, opts=None):
        return FishCompleteFileDir(ctxt, 'file', opts)

    def group(self, ctxt):
        return FishCompletionCommand("__fish_complete_groups")

    def hostname(self, ctxt):
        return FishCompletionCommand("__fish_print_hostnames")

    def pid(self, ctxt):
        return FishCompletionCommand("__fish_complete_pids")

    def process(self, ctxt):
        return FishCompletionCommand("__fish_complete_proc")

    def range(self, ctxt, start, stop, step=1):
        if step == 1:
            return FishCompletionCommand(f"command seq {start} {stop}")
        else:
            return FishCompletionCommand(f"command seq {start} {step} {stop}")

    def service(self, ctxt):
        return FishCompletionCommand("__fish_systemctl_services")

    def user(self, ctxt):
        return FishCompletionCommand("__fish_complete_users")

    def variable(self, ctxt):
        return FishCompletionCommand("set -n")

    def environment(self, ctxt):
        return FishCompletionCommand("set -n -x")

    def exec(self, ctxt, command):
        return FishCompletionCommand(command)

    def exec_fast(self, ctxt, command):
        return FishCompletionCommand(command)

    def exec_internal(self, ctxt, command):
        return FishCompletionCommand(command)

    def value_list(self, ctxt, opts):
        return FishCompleteValueList(ctxt, opts)

    def combine(self, ctxt, commands):
        return FishCompleteCombine(ctxt, self, commands)
