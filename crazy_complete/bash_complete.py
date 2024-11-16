'''This module contains code for completing arguments in Bash.'''

from . import shell

class BashCompletionBase:
    '''Base class for BASH completions.'''

    def get_code(self, append=False):
        '''
        Returns the command for BASH completion. If `append` is `True`, then
        the results will be appended to COMPREPLY, otherwise COMPREPLY will be truncated.

        Args:
            append (bool): If True, the results will be appended to COMPREPLY.

        Returns:
            str: The command for Bash completion.
        '''
        raise NotImplementedError

class BashCompletionCommand(BashCompletionBase):
    '''Used for completion functions that internally modify COMPREPLY.'''
    def __init__(self, ctxt, cmd):
        self.ctxt = ctxt
        self.cmd = cmd

    def get_code(self, append=False):
        if not self.cmd:
            return ''

        r = []

        if append:
            r.append('local -a COMPREPLY_BACK=("${COMPREPLY[@]}")')

        r.append(self.cmd)

        if append:
            r.append('COMPREPLY=("${COMPREPLY_BACK[@]}" "${COMPREPLY[@]}")')

        return '\n'.join(r)

class CompgenW(BashCompletionBase):
    def __init__(self, ctxt, values):
        self.ctxt = ctxt
        self.values = values

    def get_code(self, append=False):
        compgen_funcname = self.ctxt.helpers.use_function('compgen_w_replacement')
        return ('%s %s-- "$cur" %s' % (
            compgen_funcname,
            ('-a ' if append else ''),
            ' '.join(shell.escape(str(s)) for s in self.values)))

class BashCompletionCompgen(BashCompletionBase):
    '''Used for completion using `compgen`.'''
    def __init__(self, ctxt, compgen_args, word='"$cur"'):
        self.compgen_args = compgen_args
        self.word = word

    def get_code(self, append=False):
        return 'COMPREPLY%s=($(compgen %s -- %s))' % (
            ('+' if append else ''),
            self.compgen_args,
            self.word)

class BashCompleter(shell.ShellCompleter):
    def none(self, ctxt, *a):
        return BashCompletionCommand(ctxt, '')

    def choices(self, ctxt, choices):
        return CompgenW(ctxt, choices)

    def command(self, ctxt):
        return BashCompletionCompgen(ctxt, '-A command')

    def directory(self, ctxt, opts=None):
        directory = None if opts is None else opts.get('directory', None)
        if directory:
            cmd =  'builtin pushd %s &>/dev/null && {\n' % shell.escape(directory)
            cmd += '  _filedir -d\n'
            cmd += '  builtin popd &>/dev/null\n'
            cmd += '}'
            return BashCompletionCommand(ctxt, cmd)
        else:
            return BashCompletionCommand(ctxt, '_filedir -d')

    def file(self, ctxt, opts=None):
        directory = None if opts is None else opts.get('directory', None)
        if directory:
            cmd =  'builtin pushd %s &>/dev/null && {\n' % shell.escape(directory)
            cmd += '  _filedir\n'
            cmd += '  builtin popd &>/dev/null\n'
            cmd += '}'
            return BashCompletionCommand(ctxt, cmd)
        else:
            return BashCompletionCommand(ctxt, '_filedir')

    def group(self, ctxt):
        return BashCompletionCompgen(ctxt, '-A group')

    def hostname(self, ctxt):
        return BashCompletionCompgen(ctxt, '-A hostname')

    def pid(self, ctxt):
        return BashCompletionCommand(ctxt, '_pids')

    def process(self, ctxt):
        return BashCompletionCommand(ctxt, '_pnames')

    def range(self, ctxt, start, stop, step=1):
        if step == 1:
            return BashCompletionCompgen(ctxt, f"-W '{{{start}..{stop}}}'")
        else:
            return BashCompletionCompgen(ctxt, f"-W '{{{start}..{stop}..{step}}}'")

    def service(self, ctxt):
        return BashCompletionCompgen(ctxt, '-A service')

    def user(self, ctxt):
        return BashCompletionCompgen(ctxt, '-A user')

    def variable(self, ctxt):
        return BashCompletionCompgen(ctxt, '-A variable')

    def environment(self, ctxt):
        return BashCompletionCompgen(ctxt, '-A export')

    def exec(self, ctxt, command):
        funcname = ctxt.helpers.use_function('exec')
        return BashCompletionCommand(ctxt, '%s %s' % (funcname, shell.escape(command)))

    def value_list(self, ctxt, opts):
        funcname = ctxt.helpers.use_function('value_list')
        separator = opts.get('separator', ',')
        values = opts['values']
        if hasattr(values, 'items'):
            values = list(values.keys())

        return BashCompletionCommand(ctxt, '%s %s %s' % (
            funcname,
            shell.escape(separator),
            ' '.join(shell.escape(v) for v in values)))
