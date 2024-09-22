from collections import namedtuple, OrderedDict

from .commandline import *

def jsonToObject(json, prog):
    commandline = CommandLine(
        prog,
        parent = None,
        help = json.get('help', None),
        aliases = json.get('aliases', []),
        abbreviate_commands=json.get('abbreviate_commands', ExtendedBool.INHERIT),
        abbreviate_options=json.get('abbreviate_options', ExtendedBool.INHERIT),
        inherit_options=json.get('inherit_options', ExtendedBool.INHERIT))

    for json_option in json.get('options', []):
        commandline.add_option(
            json_option['option_strings'],
            metavar = json_option.get('metavar', None),
            help = json_option.get('help', None),
            takes_args = json_option.get('takes_args', True),
            group = json_option.get('group', None),
            multiple_option = json_option.get('multiple_option', ExtendedBool.INHERIT),
            complete = json_option.get('complete', None),
            when = json_option.get('when', None)),

    for json_positional in json.get('positionals', []):
        commandline.add_positional(
            json_positional['number'],
            metavar = json_positional.get('metavar', None),
            help = json_positional.get('help', None),
            repeatable = json_positional.get('repeatable', False),
            complete = json_positional.get('complete', None),
            when = json_positional.get('when', None)),

    return commandline

class CommandlineTree:
    Node = namedtuple('Node', ['commandline', 'subcommands'])

    def __init__(self):
        self.root = CommandlineTree.Node(None, {})

    def add_commandline(self, commandline):
        previous_commands = commandline['prog'].split()
        command = previous_commands.pop()

        node = self.root

        for previous_command in previous_commands:
            node = node.subcommands[previous_command]

        node.subcommands[command] = CommandlineTree.Node(jsonToObject(commandline, command), {})

    def get_root_commandline(self):
        if len(self.root.subcommands) == 0:
            raise Exception("No programs defined")

        if len(self.root.subcommands) > 1:
            raise Exception("Too many programs defined")

        return list(self.root.subcommands.values())[0]

def Dictionaries_To_Commandline(dictionaries):
    def visit(node):
        if len(node.subcommands):
            subp = node.commandline.add_subcommands()
            for subcommand in node.subcommands.values():
                subp.add_commandline_object(subcommand.commandline)
                visit(subcommand)

    commandline_tree = CommandlineTree()

    for dictionary in dictionaries:
        commandline_tree.add_commandline(dictionary)

    visit(commandline_tree.get_root_commandline())

    return commandline_tree.get_root_commandline().commandline

def Option_To_Dictionary(self):
    r = OrderedDict()
    r['option_strings'] = self.option_strings

    if self.metavar is not None:
        r['metavar'] = self.metavar

    if self.help is not None:
        r['help'] = self.help

    if self.takes_args != True:
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

def Positional_To_Dictionary(self):
    r = OrderedDict()

    r['number'] = self.number

    if self.metavar is not None:
        r['metavar'] = self.metavar

    if self.help is not None:
        r['help'] = self.help

    if self.repeatable is not False:
        r['repeatable'] = self.repeatable

    if self.when is not None:
        r['when'] = self.when

    if self.complete and self.complete[0] != 'none':
        r['complete'] = self.complete

    return r

def CommandLine_To_Dictionary(commandline):
    r = OrderedDict()

    prog = ' '.join(c.prog for c in commandline.get_parents(include_self=True))

    r['prog'] = prog

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
            r['options'].append(Option_To_Dictionary(option))

    if commandline.positionals:
        r['positionals'] = []
        for positional in commandline.positionals:
            r['positionals'].append(Positional_To_Dictionary(positional))

    return r

def CommandLine_To_Dictionaries(commandline):
    dictionaries = []
    commandline.visit_commandlines(lambda c: dictionaries.append(CommandLine_To_Dictionary(c)))
    return dictionaries
