"""
This module provides functions for creating CommandLine objects from
dictionaries and vice versa.
"""

from collections import OrderedDict

from .errors import CrazyError
from .cli import CommandLine, ExtendedBool

def dictionary_to_commandline(dictionary, prog):
    commandline = CommandLine(
        prog,
        parent              = None,
        help                = dictionary.get('help', None),
        aliases             = dictionary.get('aliases', []),
        abbreviate_commands = dictionary.get('abbreviate_commands', ExtendedBool.INHERIT),
        abbreviate_options  = dictionary.get('abbreviate_options', ExtendedBool.INHERIT),
        inherit_options     = dictionary.get('inherit_options', ExtendedBool.INHERIT))

    for option in dictionary.get('options', []):
        commandline.add_option(
            option['option_strings'],
            metavar         = option.get('metavar',         None),
            help            = option.get('help',            None),
            takes_args      = option.get('takes_args',      True),
            group           = option.get('group',           None),
            multiple_option = option.get('multiple_option', ExtendedBool.INHERIT),
            complete        = option.get('complete',        None),
            when            = option.get('when',            None))

    for positional in dictionary.get('positionals', []):
        commandline.add_positional(
            positional['number'],
            metavar    = positional.get('metavar',    None),
            help       = positional.get('help',       None),
            repeatable = positional.get('repeatable', False),
            complete   = positional.get('complete',   None),
            when       = positional.get('when',       None))

    return commandline

class CommandlineTree:
    class Node:
        def __init__(self, commandline, subcommands):
            self.commandline = commandline
            self.subcommands = subcommands

        def visit(self, callback):
            callback(self)
            if self.subcommands:
                for subcommand in self.subcommands.values():
                    subcommand.visit(callback)

    def __init__(self):
        self.root = CommandlineTree.Node(None, {})

    def add_commandline(self, commandline):
        previous_commands = commandline['prog'].split()
        command = previous_commands.pop()

        node = self.root

        for previous_command in previous_commands:
            node = node.subcommands[previous_command]

        node.subcommands[command] = CommandlineTree.Node(dictionary_to_commandline(commandline, command), {})

    def get_root_commandline(self):
        if len(self.root.subcommands) == 0:
            raise CrazyError("No programs defined")

        if len(self.root.subcommands) > 1:
            raise CrazyError("Too many programs defined")

        return list(self.root.subcommands.values())[0]

def dictionaries_to_commandline(dictionaries):
    def add_subcommands(node):
        if len(node.subcommands):
            subp = node.commandline.add_subcommands()
            for subcommand in node.subcommands.values():
                subp.add_commandline_object(subcommand.commandline)

    commandline_tree = CommandlineTree()

    for dictionary in dictionaries:
        commandline_tree.add_commandline(dictionary)

    root = commandline_tree.get_root_commandline()
    root.visit(add_subcommands)
    return root.commandline

def option_to_dictionary(self):
    r = OrderedDict()
    r['option_strings'] = self.option_strings

    if self.metavar is not None:
        r['metavar'] = self.metavar

    if self.help is not None:
        r['help'] = self.help

    if self.takes_args is not True:
        r['takes_args'] = self.takes_args

    if self.group is not None:
        r['group'] = self.group

    if self.multiple_option != ExtendedBool.INHERIT:
        r['multiple_option'] = self.multiple_option

    if self.complete and self.complete[0] != 'none':
        r['complete'] = self.complete

    if self.when is not None:
        r['when'] = self.when

    return r

def positional_to_dictionary(self):
    r = OrderedDict()

    r['number'] = self.number

    if self.metavar is not None:
        r['metavar'] = self.metavar

    if self.help is not None:
        r['help'] = self.help

    if self.repeatable is not False:
        r['repeatable'] = self.repeatable

    if self.complete and self.complete[0] != 'none':
        r['complete'] = self.complete

    if self.when is not None:
        r['when'] = self.when

    return r

def commandline_to_dictionary(commandline):
    r = OrderedDict()

    r['prog'] = commandline.get_command_path()

    if commandline.aliases:
        r['aliases'] = commandline.aliases

    if commandline.help is not None:
        r['help'] = commandline.help

    if commandline.abbreviate_commands != ExtendedBool.INHERIT:
        r['abbreviate_commands'] = commandline.abbreviate_commands

    if commandline.abbreviate_options != ExtendedBool.INHERIT:
        r['abbreviate_options'] = commandline.abbreviate_options

    if commandline.inherit_options != ExtendedBool.INHERIT:
        r['inherit_options'] = commandline.inherit_options

    if commandline.options:
        r['options'] = []
        for option in commandline.options:
            r['options'].append(option_to_dictionary(option))

    if commandline.positionals:
        r['positionals'] = []
        for positional in commandline.positionals:
            r['positionals'].append(positional_to_dictionary(positional))

    return r

def commandline_to_dictionaries(commandline):
    dictionaries = []
    commandline.visit_commandlines(lambda c: dictionaries.append(commandline_to_dictionary(c)))
    return dictionaries
