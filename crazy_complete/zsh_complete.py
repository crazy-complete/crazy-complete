''' This module contains code for completing arguments in Zsh '''

from . import shell
from . import helpers

def escape_colon(s):
    return s.replace(':', '\\:')

class ZshCompleter(shell.ShellCompleter):
    def none(self, ctxt, *a):
        return "' '"

    def choices(self, ctxt, choices):
        if hasattr(choices, 'items'):
            funcname = shell.make_completion_funcname_for_context(ctxt)
            metavar = shell.escape(ctxt.option.metavar or '')
            code  = 'local -a items=(\n'
            for item, description in choices.items():
                item = shell.escape(escape_colon(str(item)))
                desc = shell.escape(str(description))
                code += f'  {item}:{desc}\n'
            code += ')\n\n'
            code += f'_describe -- {metavar} items'

            ctxt.helpers.add_function(helpers.ShellFunction(funcname, code))
            funcname = ctxt.helpers.use_function(funcname)
            return funcname
        else:
            return shell.escape("(%s)" % (' '.join(shell.escape(str(c)) for c in choices)))

    def command(self, ctxt):
        return '_command_names'

    def directory(self, ctxt, opts={}):
        directory = opts.get('directory', None)
        if directory:
            return '"_directories -W %s"' % shell.escape(directory)
        return '_directories'

    def file(self, ctxt, opts={}):
        directory = opts.get('directory', None)
        if directory:
            return '"_files -W %s"' % shell.escape(directory)
        return '_files'

    def group(self, ctxt):
        return '_groups'

    def hostname(self, ctxt):
        return '_hosts'

    def pid(self, ctxt):
        return '_pids'

    def process(self, ctxt):
        return '"_process_names -a"'

    def range(self, ctxt, start, stop, step=1):
        if step == 1:
            return f"'({{{start}..{stop}}})'"
        else:
            return f"'({{{start}..{stop}..{step}}})'"

    def user(self, ctxt):
        return '_users'

    def variable(self, ctxt, option=None):
        if option == '-x':
            return '"_parameters -g \'*export*\'"'
        else:
            return '_vars'

    def exec(self, ctxt, command):
        funcname = ctxt.helpers.use_function('exec')
        return shell.escape('{%s %s}' % (funcname, shell.escape(command)))

    def value_list(self, ctxt, opts):
        desc = ctxt.option.metavar or ''
        cmd = '_values -s %s %s %s' % (
            shell.escape(opts.get('separator', ',')),
            shell.escape(desc),
            ' '.join(shell.escape(i) for i in opts['values'])
        )
        return shell.escape(cmd)
