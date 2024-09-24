import re
import collections

from . import completion_validator
from . import commandline as _commandline
from . import utils
from . import config as _config

def make_identifier(string):
    '''
    Make `string` a valid shell identifier.

    This function replaces any dashes '-' with underscores '_',
    removes any characters that are not letters, digits, or underscores,
    and ensures that consecutive underscores are replaced with a single underscore.

    Args:
        string (str): The input string to be converted into a valid shell identifier.

    Returns:
        str: The modified string that is a valid shell identifier.
    '''
    assert isinstance(string, str), "make_identifier: string: expected str, got %r" % string

    string = string.replace('-', '_')
    string = re.sub('[^a-zA-Z0-9_]', '', string)
    string = re.sub('_+', '_', string)
    if string and string[0] in '0123456789':
        return '_' + string
    return string

def escape(string, escape_empty_string=True):
    '''
    Escapes special characters in a string for safe usage in shell commands or scripts.

    Args:
        string (str): The input string to be escaped.
        escape_empty_string (bool, optional): Determines whether to escape an empty string or not.
            Defaults to True.

    Returns:
        str: The escaped string.
    '''
    assert isinstance(string, str), "escape: s: expected str, got %r" % string

    if not string and not escape_empty_string:
        return ''

    if re.fullmatch('[a-zA-Z0-9_@%+=:,./-]+', string):
        return string

    if "'" not in string:
        return "'%s'" % string

    if '"' not in string:
        return '"%s"' % string.replace('\\', '\\\\').replace('$', '\\$').replace('`', '\\`')

    return "'%s'" % string.replace("'", '\'"\'"\'')

def make_completion_funcname(cmdline, prefix='_', suffix=''):
    '''
    Generates a function name for auto-completing a program or subcommand.

    Args:
        cmdline (CommandLine): The CommandLine instance representing the program or subcommand.

    Returns:
        str: The generated function name for auto-completion.

    This function is used to generate a unique function name for auto-completing
    a program or subcommand in the specified shell. It concatenates the names of
    all parent commandlines, including the current commandline, and converts them
    into a valid function name format.

    Example:
        For a program with the name 'my_program' and a subcommand with the name 'subcommand',
        the generated function name is '_my_program_subcommand'.
    '''
    assert isinstance(cmdline, _commandline.CommandLine), "make_completion_funcname: cmdline: expected CommandLine, got %r" % cmdline

    commandlines = cmdline.get_parents(include_self=True)

    r = '%s%s%s' % (
        prefix,
        make_identifier('_'.join(p.prog for p in commandlines)),
        suffix
    )

    return r

def make_completion_funcname_for_context(ctxt):
    commandlines = ctxt.commandline.get_parents(include_self=True)
    del commandlines[0]

    funcname = make_identifier('_'.join(p.prog for p in commandlines))

    if isinstance(ctxt.option, _commandline.Option):
        return '%s_%s' % (funcname, ctxt.option.option_strings[0])
    if isinstance(ctxt.option, _commandline.Positional):
        return '%s_%s' % (funcname, ctxt.option.metavar)

class ShellCompleter:
    def complete(self, ctxt, completion, *a):
        if not hasattr(self, completion):
            utils.warn("ShellCompleter: Falling back from `%s` to `none`" % (completion,))
            completion = 'none'

        return getattr(self, completion)(ctxt, *a)

    def fallback(self, ctxt, from_, to, *a):
        utils.warn("ShellCompleter: Falling back from `%s` to `%s`" % (from_, to))
        return self.complete(ctxt, to, *a)

    def none(self, ctxt, *a):
        return ''

    def signal(self, ctxt, prefix=''):
        sig = prefix
        signals = collections.OrderedDict([
            (sig+'ABRT',   'Process abort signal'),
            (sig+'ALRM',   'Alarm clock'),
            (sig+'BUS',    'Access to an undefined portion of a memory object'),
            (sig+'CHLD',   'Child process terminated, stopped, or continued'),
            (sig+'CONT',   'Continue executing, if stopped'),
            (sig+'FPE',    'Erroneous arithmetic operation'),
            (sig+'HUP',    'Hangup'),
            (sig+'ILL',    'Illegal instruction'),
            (sig+'INT',    'Terminal interrupt signal'),
            (sig+'KILL',   'Kill (cannot be caught or ignored)'),
            (sig+'PIPE',   'Write on a pipe with no one to read it'),
            (sig+'QUIT',   'Terminal quit signal'),
            (sig+'SEGV',   'Invalid memory reference'),
            (sig+'STOP',   'Stop executing (cannot be caught or ignored)'),
            (sig+'TERM',   'Termination signal'),
            (sig+'TSTP',   'Terminal stop signal'),
            (sig+'TTIN',   'Background process attempting read'),
            (sig+'TTOU',   'Background process attempting write'),
            (sig+'USR1',   'User-defined signal 1'),
            (sig+'USR2',   'User-defined signal 2'),
            (sig+'POLL',   'Pollable event'),
            (sig+'PROF',   'Profiling timer expired'),
            (sig+'SYS',    'Bad system call'),
            (sig+'TRAP',   'Trace/breakpoint trap'),
            (sig+'XFSZ',   'File size limit exceeded'),
            (sig+'VTALRM', 'Virtual timer expired'),
            (sig+'XCPU',   'CPU time limit exceeded'),
        ])

        return self.complete(ctxt, 'choices', signals)

    def range(self, ctxt, start, stop, step=1):
        return self.complete('choices', list(range(start, stop, step)))

    def directory(self, ctxt, opts):
        return self.fallback(ctxt, 'directory', 'file', opts)

    def process(self, ctxt):
        return self.fallback(ctxt, 'process', 'none')

    def pid(self, ctxt):
        return self.fallback(ctxt, 'pid', 'none')

    def command(self, ctxt):
        return self.fallback(ctxt, 'command', 'file')

    def variable(self, ctxt, option):
        return self.fallback(ctxt, 'variable', 'none')

    def service(self, ctxt):
        return self.fallback(ctxt, 'service', 'none')

    def user(self, ctxt):
        return self.fallback(ctxt, 'user', 'none')

    def group(self, ctxt):
        return self.fallback(ctxt, 'group', 'none')

class GenerationContext:
    def __init__(self, config, helpers):
        self.config = config
        self.helpers = helpers

    def getOptionGenerationContext(self, commandline, option):
        return OptionGenerationContext(
            self.config,
            self.helpers,
            commandline,
            option
        )

class OptionGenerationContext(GenerationContext):
    def __init__(self, config, helpers, commandline, option):
        super().__init__(config, helpers)
        self.commandline = commandline
        self.option = option

class CompletionGenerator:
    def __init__(self, completion_klass, helpers_klass, commandline, program_name, config):
        commandline = commandline.copy()

        if program_name is not None:
            commandline.prog = program_name

        if config is None:
            config = _config.Config()

        _commandline.CommandLine_Apply_Config(commandline, config)
        completion_validator.CompletionValidator().validate_commandlines(commandline)

        self.include_files_content = []
        for file in config.include_files:
            with open(file, 'r') as fh:
                self.include_files_content.append(fh.read().strip())

        self.completion_klass = completion_klass
        self.ctxt = GenerationContext(config, helpers_klass(commandline.prog))
        self.result = []
        commandline.visit_commandlines(self._call_generator)

    def _call_generator(self, commandline):
        self.result.append(self.completion_klass(self.ctxt, commandline))
