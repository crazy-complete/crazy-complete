import os
import argparse

from .errors import CrazyError
from . import bash, fish, zsh
from . import argparse_source, json_source, yaml_source
from . import argparse_mod # .complete() etc.
from . import help_converter
from . import config
from . import paths
from . import versions


def boolean(string):
    try:
        return {'true': True, 'false': False}[string.lower()]
    except KeyError:
        raise ValueError(f"Not a bool: {string}")


p = argparse.ArgumentParser('crazy-complete',
    description='Generate shell auto completion files for all major shells',
    exit_on_error=False)

p.add_argument('shell', choices=('bash', 'fish', 'fish3', 'fish4', 'zsh', 'json', 'yaml'),
    help='Specify the shell type for the completion script')

p.add_argument('definition_file',
    help='The file containing the command line definitions'
).complete('file')

p.add_argument('--version', action='version', version='%(prog)s 0.3.3',
    help='Show program version')

p.add_argument('--parser-variable', default=None,
    help='Specify the variable name of the ArgumentParser object (for --input-type=python)')

p.add_argument('--input-type', choices=('yaml', 'json', 'python', 'help', 'auto'), default='auto',
    help='Specify input file type')

p.add_argument('--abbreviate-commands', metavar='BOOL', default=False, type=boolean,
    help='Sets whether commands can be abbreviated'
).complete('choices', ('True', 'False'))

p.add_argument('--abbreviate-options', metavar='BOOL', default=False, type=boolean,
    help='Sets whether options can be abbreviated'
).complete('choices', ('True', 'False'))

# Be backwards compatible
p.add_argument('--multiple-options', metavar='BOOL', default=False, type=boolean,
    help=argparse.SUPPRESS, dest='repeatable_options',
).complete('choices', ('True', 'False'))

p.add_argument('--repeatable-options', metavar='BOOL', default=False, type=boolean,
    help='Sets whether options are suggested multiple times during completion'
).complete('choices', ('True', 'False'))

p.add_argument('--inherit-options', metavar='BOOL', default=False, type=boolean,
    help='Sets whether parent options are visible to subcommands'
).complete('choices', ('True', 'False'))

p.add_argument('--vim-modeline', metavar='BOOL', default=True, type=boolean,
    help='Sets whether a vim modeline comment shall be appended to the generated code'
).complete('choices', ('True', 'False'))

p.add_argument('--zsh-compdef', metavar='BOOL', default=True, type=boolean,
    help='Sets whether #compdef is used in zsh scripts'
).complete('choices', ('True', 'False'))

p.add_argument('--fish-fast', metavar='BOOL', default=False, type=boolean,
    help='Use faster commandline parsing at the cost of correctness'
).complete('choices', ('True', 'False'))

p.add_argument('--fish-inline-conditions', metavar='BOOL', default=False, type=boolean,
    help="Don't store conditions in a variable"
).complete('choices', ('True', 'False'))

p.add_argument('--include-file', metavar='FILE', action='append',
    help='Include file in output'
).complete('file')

p.add_argument('--debug', action='store_true', default=False,
    help='Enable debug mode')

grp = p.add_mutually_exclusive_group()

grp.add_argument('-o', '--output', metavar='FILE', default=None, dest='output_file',
    help='Write output to destination file [default: stdout]'
).complete('file')

grp.add_argument('-i', '--install-system-wide', default=False, action='store_true',
    help='Write output to the system-wide completions dir of shell')

grp.add_argument('-u', '--uninstall-system-wide', default=False, action='store_true',
    help='Uninstall the system-wide completion file for program')

# We use a unique object name for avoiding name clashes when
# importing/executing the foreign python script
_crazy_complete_argument_parser = p
del p

def load_definition_file(opts):
    if opts.input_type == 'auto':
        basename = os.path.basename(opts.definition_file)
        extension = os.path.splitext(basename)[1].lower().strip('.')
        if extension == 'json':
            return json_source.load_from_file(opts.definition_file)
        if extension in ('yaml', 'yml'):
            return yaml_source.load_from_file(opts.definition_file)
        if extension == 'py':
            raise CrazyError('Reading Python files must be enabled by --input-type=python')
        if extension == '':
            raise CrazyError('File has no extension. Please supply --input-type=json|yaml|help|python')
        raise CrazyError(f'Unknown file extension `{extension}`. Please supply --input-type=json|yaml|help|python')
    if opts.input_type == 'json':
        return json_source.load_from_file(opts.definition_file)
    if opts.input_type == 'yaml':
        return yaml_source.load_from_file(opts.definition_file)
    if opts.input_type == 'python':
        return argparse_source.load_from_file(opts.definition_file,
            opts.parser_variable,
            parser_blacklist=[_crazy_complete_argument_parser])

    raise AssertionError("Should not be reached")

def write_string_to_file(string, file):
    if file is not None:
        with open(file, 'w', encoding='utf-8') as fh:
            fh.write(string)
    else:
        print(string)

def generate(opts):
    if opts.input_type == 'help':
        if opts.shell != 'yaml':
            raise CrazyError('The `help` input-type currently only supports YAML generation')
        output = help_converter.from_file_to_yaml(opts.definition_file)
        write_string_to_file(output, opts.output_file)
        return

    cmdline = load_definition_file(opts)

    if opts.shell == 'json':
        output = json_source.commandline_to_json(cmdline)
        write_string_to_file(output, opts.output_file)
        return

    if opts.shell == 'yaml':
        output = yaml_source.commandline_to_yaml(cmdline)
        write_string_to_file(output, opts.output_file)
        return

    conf = config.Config()
    conf.set_abbreviate_commands(opts.abbreviate_commands)
    conf.set_abbreviate_options(opts.abbreviate_options)
    conf.set_repeatable_options(opts.repeatable_options)
    conf.set_inherit_options(opts.inherit_options)
    conf.set_vim_modeline(opts.vim_modeline)
    conf.set_zsh_compdef(opts.zsh_compdef)
    conf.set_fish_fast(opts.fish_fast)
    conf.set_fish_inline_conditions(opts.fish_inline_conditions)
    conf.include_many_files(opts.include_file or [])

    if opts.shell == 'bash':
        output = bash.generate_completion(cmdline, conf)
    elif opts.shell == 'fish':
        output = fish.generate_completion(cmdline, conf, versions.get_fish_major_version())
    elif opts.shell == 'fish3':
        output = fish.generate_completion(cmdline, conf, 3)
    elif opts.shell == 'fish4':
        output = fish.generate_completion(cmdline, conf, 4)
    elif opts.shell == 'zsh':
        output = zsh.generate_completion(cmdline, conf)

    if opts.install_system_wide or opts.uninstall_system_wide:
        file = {
            'bash':  paths.get_bash_completion_file,
            'fish':  paths.get_fish_completion_file,
            'fish3': paths.get_fish_completion_file,
            'fish4': paths.get_fish_completion_file,
            'zsh':   paths.get_zsh_completion_file,
        }[opts.shell](cmdline.prog)

        if opts.install_system_wide:
            print_err(f'Installing to {file}')
            write_string_to_file(output, file)
        else:
            print_err(f'Removing {file}')
            os.remove(file)
    else:
        write_string_to_file(output, opts.output_file)

class Application:
    def __init__(self):
        self.options = None

    def parse_args(self, args):
        '''Parse command line arguments.

        Raises:
            - argparse.ArgumentError
        '''
        self.options = _crazy_complete_argument_parser.parse_args(args)

    def run(self):
        '''Run the crazy-complete program.

        Raises:
            - CrazyError
            - FileNotFoundError
            - yaml.scanner.ScannerError
            - yaml.parser.ParserError
            - json.decoder.JSONDecodeError
        '''
        generate(self.options)
