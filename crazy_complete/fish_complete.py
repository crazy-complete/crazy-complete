from . import shell
from . import helpers

class FishCompletionBase:
    def get_args(self):
        '''
        Return a list of arguments to be appended to the `complete`
        command in FISH.

        The returned arguments should be in raw form, without any escaping.
        Escaping will be handled at a later stage.
        '''
        raise NotImplementedError

class FishCompletionFromArgs(FishCompletionBase):
    def __init__(self, args):
        self.args = args

    def get_args(self):
        return self.args

class FishCompletionCommand(FishCompletionBase):
    '''
    Class for executing a command and parsing its output.
    '''
    def  __init__(self, command):
        self.command = command

    def get_args(self):
        return ['-f', '-a', '(%s)' % self.command]

class FishCompleter(shell.ShellCompleter):
    def none(self, ctxt):
        return FishCompletionFromArgs(['-f'])

    def choices(self, ctxt, choices):
        if hasattr(choices, 'items'):
            funcname = shell.make_completion_funcname_for_context(ctxt)
            code = 'printf "%s\\t%s\\n" \\\n'
            for item, description in choices.items():
                code += '  %s %s \\\n' % (shell.escape(str(item)), shell.escape(str(description)))
            code = code.rstrip(' \\\n')

            ctxt.helpers.add_function(helpers.FishFunction(funcname, code))
            funcname = ctxt.helpers.use_function(funcname)
            return FishCompletionCommand(funcname)

        return FishCompletionFromArgs(['-f', '-a', ' '.join(shell.escape(str(c)) for c in choices)])

    def command(self, ctxt):
        return FishCompletionCommand("__fish_complete_command")

    def directory(self, ctxt, opts={}):
        directory = opts.get('directory', None)
        if directory is not None:
            funcname = ctxt.helpers.use_function('fish_complete_filedir')
            return FishCompletionCommand('%s -D -C %s' % (funcname, shell.escape(directory)))
        return FishCompletionCommand("__fish_complete_directories")

    def file(self, ctxt, opts={}):
        directory = opts.get('directory', None)
        if directory is not None:
            funcname = ctxt.helpers.use_function('fish_complete_filedir')
            return FishCompletionCommand('%s -C %s' % (funcname, shell.escape(directory)))
        return FishCompletionFromArgs(['-F'])

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
            return FishCompletionCommand(f"seq {start} {stop}")
        else:
            return FishCompletionCommand(f"seq {start} {step} {stop}")

    def service(self, ctxt):
        return FishCompletionCommand("__fish_systemctl_services")

    def user(self, ctxt):
        return FishCompletionCommand("__fish_complete_users")

    def variable(self, ctxt, option=None):
        if option == '-x':
            return FishCompletionCommand("set -n -x")
        else:
            return FishCompletionCommand("set -n")

    def exec(self, ctxt, command):
        return FishCompletionCommand(command)

    def value_list(self, ctxt, opts):
        separator = opts.get('separator', ',')

        funcname = shell.make_completion_funcname_for_context(ctxt)
        code = 'printf "%s\\n" \\\n'
        for value in opts['values']:
            code += '  %s \\\n' % shell.escape(str(value))
        code = code.rstrip(' \\\n')

        ctxt.helpers.add_function(helpers.FishFunction(funcname, code))
        funcname = ctxt.helpers.use_function(funcname)

        cmd = '__fish_complete_list %s %s' % (shell.escape(separator), funcname)
        return FishCompletionCommand(cmd)

