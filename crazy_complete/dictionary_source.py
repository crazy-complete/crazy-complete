"""
This module provides functions for creating CommandLine objects from
dictionaries and vice versa.
"""

from collections import OrderedDict

from .errors import CrazyError, CrazyTypeError
from .cli import CommandLine, ExtendedBool
from .str_utils import validate_prog
from . import compat


def _validate_keys(dictionary, allowed_keys):
    for key in dictionary.keys():
        if key not in allowed_keys:
            raise CrazyError(f'Unknown key: {key}')


def dictionary_to_commandline(dictionary, prog=None):
    '''Convert a single dictionary to a cli.CommandLine object.'''

    _validate_keys(dictionary,
        ['prog', 'help', 'aliases', 'wraps',
         'abbreviate_commands', 'abbreviate_options',
         'inherit_options', 'options', 'positionals'])

    options = dictionary.get('options', [])
    if not isinstance(options, list):
        raise CrazyTypeError('options', 'list', options)

    positionals = dictionary.get('positionals', [])
    if not isinstance(positionals, list):
        raise CrazyTypeError('positionals', 'list', positionals)

    commandline = CommandLine(
        prog or dictionary['prog'],
        parent              = None,
        help                = dictionary.get('help', None),
        aliases             = dictionary.get('aliases', []),
        wraps               = dictionary.get('wraps', None),
        abbreviate_commands = dictionary.get('abbreviate_commands', ExtendedBool.INHERIT),
        abbreviate_options  = dictionary.get('abbreviate_options', ExtendedBool.INHERIT),
        inherit_options     = dictionary.get('inherit_options', ExtendedBool.INHERIT))

    for option in options:
        _validate_keys(option,
            ['option_strings', 'metavar', 'help', 'optional_arg', 'groups',
             'repeatable', 'final', 'hidden', 'complete', 'nosort',
             'when', 'capture'])

        commandline.add_option(
            option.get('option_strings',  None),
            metavar         = option.get('metavar',         None),
            help            = option.get('help',            None),
            optional_arg    = option.get('optional_arg',    False),
            groups          = option.get('groups',          None),
            repeatable      = option.get('repeatable',      ExtendedBool.INHERIT),
            final           = option.get('final',           False),
            hidden          = option.get('hidden',          False),
            complete        = option.get('complete',        None),
            nosort          = option.get('nosort',          False),
            when            = option.get('when',            None),
            capture         = option.get('capture',         None))

    for positional in positionals:
        _validate_keys(positional,
            ['number', 'metavar', 'help', 'repeatable', 'complete', 'nosort',
             'when', 'capture'])

        commandline.add_positional(
            positional.get('number', None),
            metavar    = positional.get('metavar',    None),
            help       = positional.get('help',       None),
            repeatable = positional.get('repeatable', False),
            complete   = positional.get('complete',   None),
            nosort     = positional.get('nosort',     False),
            when       = positional.get('when',       None),
            capture    = positional.get('capture',    None))

    return commandline


def _check_prog_in_dictionary(dictionary):
    if 'prog' not in dictionary:
        raise CrazyError('Missing `prog` field')

    if not isinstance(dictionary['prog'], str):
        raise CrazyTypeError('prog', 'str', dictionary["prog"])

    try:
        validate_prog(dictionary['prog'])
    except CrazyError as e:
        raise CrazyError(f'prog: {e}')


def _get_commandline_by_path(root, path):
    current = root

    for i, name in enumerate(path):
        path_str = ' '.join(path[0:i + 1])

        if not current.get_subcommands():
            raise CrazyError(f"Missing definition of program `{path_str}`")

        current = current.get_subcommands().get_subcommand_by_name(name)
        if not current:
            raise CrazyError(f"Missing definition of program `{path_str}`")

    return current


def dictionaries_to_commandline(dictionaries):
    '''Convert a list of dictionaries to a cli.CommandLine object.'''

    compat.fix_commandline_dictionaries(dictionaries)

    root = CommandLine('root')

    for dictionary in dictionaries:
        _check_prog_in_dictionary(dictionary)

        path = dictionary['prog'].split()
        progname = path.pop()

        cmdline = _get_commandline_by_path(root, path)

        subcommands = cmdline.get_subcommands()
        if not subcommands:
            subcommands = cmdline.add_subcommands()

        new_cmdline = dictionary_to_commandline(dictionary, progname)

        try:
            subcommands.add_commandline_object(new_cmdline)
        except CrazyError as e:
            raise CrazyError(f"Multiple definition of program `{progname}`") from e

    if not root.get_subcommands():
        raise CrazyError("No programs defined")

    if len(root.get_subcommands().subcommands) > 1:
        progs = [c.prog for c in root.get_subcommands().subcommands]
        raise CrazyError(f"Too many main programs defined: {progs}")

    cmdline = root.get_subcommands().subcommands[0]
    cmdline.parent = None
    return cmdline


def option_to_dictionary(self):
    '''Convert a cli.Option object to a dictionary.'''

    r = OrderedDict()

    r['option_strings'] = self.option_strings

    if self.metavar is not None:
        r['metavar'] = self.metavar

    if self.help is not None:
        r['help'] = self.help

    if self.optional_arg is not False:
        r['optional_arg'] = self.optional_arg

    if self.groups is not None:
        r['groups'] = self.groups

    if self.repeatable != ExtendedBool.INHERIT:
        r['repeatable'] = self.repeatable

    if self.final is True:
        r['final'] = self.final

    if self.hidden is True:
        r['hidden'] = self.hidden

    if self.complete:
        r['complete'] = self.complete

    if self.nosort is True:
        r['nosort'] = self.nosort

    if self.when is not None:
        r['when'] = self.when

    if self.capture is not None:
        r['capture'] = self.capture

    return r


def positional_to_dictionary(self):
    '''Convert a cli.Positional object to a dictionary.'''

    r = OrderedDict()

    r['number'] = self.number

    if self.metavar is not None:
        r['metavar'] = self.metavar

    if self.help is not None:
        r['help'] = self.help

    if self.repeatable is not False:
        r['repeatable'] = self.repeatable

    if self.complete:
        r['complete'] = self.complete

    if self.nosort is True:
        r['nosort'] = self.nosort

    if self.when is not None:
        r['when'] = self.when

    if self.capture is not None:
        r['capture'] = self.capture

    return r


def commandline_to_dictionary(commandline):
    '''Convert a cli.CommandLine object to a dictionary.'''

    r = OrderedDict()

    r['prog'] = commandline.get_command_path()

    if commandline.aliases:
        r['aliases'] = commandline.aliases

    if commandline.help is not None:
        r['help'] = commandline.help

    if commandline.wraps is not None:
        r['wraps'] = commandline.wraps

    if commandline.abbreviate_commands != ExtendedBool.INHERIT:
        r['abbreviate_commands'] = commandline.abbreviate_commands

    if commandline.abbreviate_options != ExtendedBool.INHERIT:
        r['abbreviate_options'] = commandline.abbreviate_options

    if commandline.inherit_options != ExtendedBool.INHERIT:
        r['inherit_options'] = commandline.inherit_options

    if commandline.options:
        r['options'] = options = []
        for option in commandline.options:
            options.append(option_to_dictionary(option))

    if commandline.positionals:
        r['positionals'] = positionals = []
        for positional in commandline.positionals:
            positionals.append(positional_to_dictionary(positional))

    return r


def commandline_to_dictionaries(commandline):
    '''Convert a cli.CommandLine object to dictionaries.'''

    dictionaries = []
    commandline.visit_commandlines(lambda c: dictionaries.append(commandline_to_dictionary(c)))
    return dictionaries
