'''Class for main command line application.'''

import os
import sys
import shlex
import argparse

from .errors import CrazyError
from . import manual
from . import bash, fish, zsh
from . import argparse_source, json_source, yaml_source
from . import argparse_mod # .complete()
from . import help_converter
from . import utils
from . import config
from . import paths


# The import of `argparse_mod` only modifies the classes provided by the
# argparse module. We use the dummy function to silence warnings about the
# unused import.
argparse_mod.dummy()


def boolean(string):
    '''Convert string to bool, else raise ValueError.'''

    try:
        return {'true': True, 'false': False}[string.lower()]
    except KeyError as e:
        raise ValueError(f"Not a bool: {string}") from e


def version(string):
    '''Parse a version.'''

    return tuple(map(int, string.split('.')))


def feature_list(string):
    '''Convert a comma separated string of features to list.'''

    features = string.split(',')

    for feature in features:
        if feature not in ('hidden', 'final', 'groups', 'repeatable', 'when'):
            raise ValueError(f"Invalid feature: {feature}")

    return features


p = argparse.ArgumentParser(
    'crazy-complete',
    description='Generate shell auto completion files for all major shells',
    exit_on_error=False)

p.add_argument(
    'shell', choices=('bash', 'fish', 'zsh', 'json', 'yaml'),
    help='Specify the shell type for the completion script')

p.add_argument(
    'definition_file',
    help='The file containing the command line definitions'
).complete('file')

p.add_argument(
    '--version', action='version', version='%(prog)s 0.3.6',
    help='Show program version')

p.add_argument(
    '--manual', metavar='TOPIC', nargs='?',
    help='Show manual for topic')

p.add_argument(
    '--parser-variable', default=None,
    help='Specify the variable name of the ArgumentParser object (for --input-type=python)')

p.add_argument(
    '--input-type', choices=('yaml', 'json', 'python', 'help', 'auto'), default='auto',
    help='Specify input file type')

p.add_argument(
    '--abbreviate-commands', metavar='BOOL', default=False, type=boolean,
    help='Sets whether commands can be abbreviated'
).complete('choices', ('True', 'False'))

p.add_argument(
    '--abbreviate-options', metavar='BOOL', default=False, type=boolean,
    help='Sets whether options can be abbreviated'
).complete('choices', ('True', 'False'))

p.add_argument(
    '--repeatable-options', metavar='BOOL', default=False, type=boolean,
    help='Sets whether options are suggested multiple times during completion'
).complete('choices', ('True', 'False'))

p.add_argument(
    '--inherit-options', metavar='BOOL', default=False, type=boolean,
    help='Sets whether parent options are visible to subcommands'
).complete('choices', ('True', 'False'))

p.add_argument(
    '--option-stacking', metavar='BOOL', default=True, type=boolean,
    help='Sets whether short option stacking is allowed'
).complete('choices', ('True', 'False'))

p.add_argument(
    '--disable', metavar='FEATURES', default=[], type=feature_list,
    help='Disable features (hidden,final,groups,repeatable,when)'
).complete('value_list', {'values': {
    'hidden':     'Disable hidden options',
    'final':      'Disable final options',
    'groups':     'Disable option groups',
    'repeatable': 'Disable check for repeatable options',
    'when':       'Disable conditional options and positionals',
}})

p.add_argument(
    '--vim-modeline', metavar='BOOL', default=True, type=boolean,
    help='Sets whether a vim modeline comment shall be appended to the generated code'
).complete('choices', ('True', 'False'))

p.add_argument(
    '--bash-completions-version', metavar='VERSION', default=(2,), type=version,
    help='Generate code for a specific bash-completions version'
)

p.add_argument(
    '--zsh-compdef', metavar='BOOL', default=True, type=boolean,
    help='Sets whether #compdef is used in zsh scripts'
).complete('choices', ('True', 'False'))

p.add_argument(
    '--fish-fast', metavar='BOOL', default=False, type=boolean,
    help='Use faster commandline parsing at the cost of correctness'
).complete('choices', ('True', 'False'))

p.add_argument(
    '--fish-inline-conditions', metavar='BOOL', default=False, type=boolean,
    help="Don't store conditions in a variable"
).complete('choices', ('True', 'False'))

p.add_argument(
    '--include-file', metavar='FILE', action='append',
    help='Include file in output'
).complete('file')

p.add_argument(
    '--comment', metavar='COMMENT', action='append',
    help='Add a comment to output'
)

p.add_argument(
    '--debug', action='store_true', default=False,
    help='Enable debug mode')

p.add_argument(
    '--keep-comments', action='store_true', default=False,
    help='Keep comments in generated output')

p.add_argument(
    '--function-prefix', metavar='PREFIX', default='_$PROG',
    help='Set the prefix used for generated functions')

grp = p.add_mutually_exclusive_group()

grp.add_argument(
    '-o', '--output', metavar='FILE', default=None, dest='output_file',
    help='Write output to destination file [default: stdout]'
).complete('file')

grp.add_argument(
    '-i', '--install-system-wide', default=False, action='store_true',
    help='Write output to the system-wide completions dir of shell')

grp.add_argument(
    '-u', '--uninstall-system-wide', default=False, action='store_true',
    help='Uninstall the system-wide completion file for program')

# We use a unique object name for avoiding name clashes when
# importing/executing the foreign python script
_crazy_complete_argument_parser = p
del p


def write_string_to_file(string, file):
    '''Writes string to file if file is given.'''

    if file is not None:
        with open(file, 'w', encoding='utf-8') as fh:
            fh.write(string)
    else:
        print(string)


def load_definition_file(opts):
    '''Load a definition file as specified in `opts`.'''

    if opts.input_type == 'auto':
        basename = os.path.basename(opts.definition_file)
        extension = os.path.splitext(basename)[1].lower().strip('.')

        if extension == 'json':
            return json_source.load_from_file(opts.definition_file)

        if extension in ('yaml', 'yml'):
            return yaml_source.load_from_file(opts.definition_file)

        if extension == 'py':
            msg = 'Reading Python files must be enabled by --input-type=python'
            raise CrazyError(msg)

        if extension == '':
            msg = ('File has no extension. '
                   'Please supply --input-type=json|yaml|help|python')
            raise CrazyError(msg)

        msg = (f'Unknown file extension `{extension}`. '
               'Please supply --input-type=json|yaml|help|python')
        raise CrazyError(msg)

    if opts.input_type == 'json':
        return json_source.load_from_file(opts.definition_file)

    if opts.input_type == 'yaml':
        return yaml_source.load_from_file(opts.definition_file)

    if opts.input_type == 'python':
        return argparse_source.load_from_file(opts.definition_file,
            opts.parser_variable,
            parser_blacklist=[_crazy_complete_argument_parser])

    raise AssertionError("Should not be reached")


def _get_config_from_options(opts):
    conf = config.Config()
    conf.set_debug(opts.debug)
    conf.set_function_prefix(opts.function_prefix)
    conf.set_abbreviate_commands(opts.abbreviate_commands)
    conf.set_abbreviate_options(opts.abbreviate_options)
    conf.set_repeatable_options(opts.repeatable_options)
    conf.set_inherit_options(opts.inherit_options)
    conf.set_option_stacking(opts.option_stacking)
    conf.set_vim_modeline(opts.vim_modeline)
    conf.set_bash_completions_version(opts.bash_completions_version)
    conf.set_zsh_compdef(opts.zsh_compdef)
    conf.set_fish_fast(opts.fish_fast)
    conf.set_fish_inline_conditions(opts.fish_inline_conditions)
    conf.include_many_files(opts.include_file or [])
    conf.set_keep_comments(opts.keep_comments)
    conf.add_comments(opts.comment or [])

    for feature in opts.disable:
        if feature == 'hidden':
            conf.disable_hidden(True)
        elif feature == 'final':
            conf.disable_final(True)
        elif feature == 'groups':
            conf.disable_groups(True)
        elif feature == 'repeatable':
            conf.disable_repeatable(True)
        elif feature == 'when':
            conf.disable_when(True)

    return conf


def try_print_manual(args):
    '''Print manual.'''

    parser = argparse.ArgumentParser()
    parser.add_argument('--manual', nargs='?', const='all')
    opts, _ = parser.parse_known_args(args)

    if not opts.manual:
        return

    manual.print_help_topic(opts.manual, os.isatty(sys.stdout.fileno()))
    sys.exit(0)


def try_batch(args):
    '''Do batch processing.'''

    parser = argparse.ArgumentParser()
    parser.add_argument('--batch')
    opts, _ = parser.parse_known_args(args)

    if not opts.batch:
        return

    with open(opts.batch, 'r', encoding='utf-8') as fh:
        content = fh.read()

    for line in content.split('\n'):
        line = line.strip()

        if not line or line.startswith('#'):
            continue

        utils.print_err('Running:', sys.argv[0], line)

        app = Application()
        app.parse_args(shlex.split(line))
        app.run()

    sys.exit(0)


def generate(opts):
    '''Generate output file as specified in `opts`.'''

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

    conf = _get_config_from_options(opts)

    if opts.shell == 'bash':
        output = bash.generate_completion(cmdline, conf)
    elif opts.shell == 'fish':
        output = fish.generate_completion(cmdline, conf)
    elif opts.shell == 'zsh':
        output = zsh.generate_completion(cmdline, conf)

    if opts.install_system_wide or opts.uninstall_system_wide:
        file = {
            'bash':  paths.get_bash_completion_file,
            'fish':  paths.get_fish_completion_file,
            'zsh':   paths.get_zsh_completion_file,
        }[opts.shell](cmdline.prog)

        if opts.install_system_wide:
            utils.print_err(f'Installing to {file}')
            write_string_to_file(output, file)
        else:
            utils.print_err(f'Removing {file}')
            os.remove(file)
    else:
        write_string_to_file(output, opts.output_file)


class Application:
    '''Class for main command line application.'''

    def __init__(self):
        self.options = None

    def parse_args(self, args):
        '''Parse command line arguments.

        Raises:
            - argparse.ArgumentError
        '''
        try_print_manual(args)
        try_batch(args)
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
