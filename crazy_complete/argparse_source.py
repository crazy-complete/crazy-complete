"""
This module provides functions for creating CommandLine objects from
Python's argparse.ArgumentParser.
"""

import argparse
from collections import OrderedDict

from . import file_loader
from . import utils
from .errors import CrazyError
from .cli import CommandLine, MutuallyExclusiveGroup

# We have to use implementation details of the argparse module...
# pylint: disable=protected-access

def range_to_complete(r):
    '''Convert a Python range object to a range complete format.'''
    start = r.start
    step = r.step
    end = r.stop - 1 if step > 0 else r.stop + 1

    if step == 1:
        return ('range', start, end)
    else:
        return ('range', start, end, step)

def get_complete(action):
    '''
    Get the `complete` attribute of `action` if it is set.
    Otherwise determine `complete` from action type.
    '''
    complete = action.get_complete()

    if isinstance(action, (
        argparse._HelpAction,
        argparse._VersionAction,
        argparse._StoreTrueAction,
        argparse._StoreFalseAction,
        argparse._StoreConstAction,
        argparse._AppendConstAction,
        argparse._CountAction)):

        if complete:
            utils.warn(f"Action has .complete() set but takes no arguments: {action}")

        return None

    if isinstance(action, (
        argparse._StoreAction,
        argparse._ExtendAction,
        argparse._AppendAction)):

        if complete:
            if action.choices:
                utils.warn(f"Action's choices overridden by .complete(): {action}")
            return complete

        if action.choices:
            if isinstance(action.choices, range):
                return range_to_complete(action.choices)
            return ['choices', action.choices]

        return ['none']

    if isinstance(action, argparse.BooleanOptionalAction):
        raise CrazyError("argparse.BooleanOptionalAction is not supported yet")

    raise CrazyError(f'Unknown action type: {action}')

def get_final(action):
    if isinstance(action, (argparse._HelpAction, argparse._VersionAction)):
        return True

    return action.get_final()

def argumentparser_to_commandline(parser, prog=None, description=None):
    '''Converts an ArgumentParser object to a CommandLine object.

    Args:
        parser (argparse.ArgumentParser):
            The ArgumentParser object to convert.
        prog (str, optional):
            The name of the program.  Defaults to the program name of the parser.
        description (str, optional):
            The description of the program.  Defaults to the description of the parser.

    Returns:
        CommandLine: A CommandLine object representing the converted parser.
    '''
    if not description:
        description = parser.description

    if not prog:
        prog = parser.prog

    commandline = CommandLine(prog, help=description, aliases=parser.get_aliases())
    positional_number = 0

    for action in parser._actions:
        if isinstance(action, argparse._SubParsersAction):
            subparsers  = OrderedDict()
            for name, subparser in action.choices.items():
                subparsers[name] = {'parser': subparser, 'help': None}

            for subaction in action._get_subactions():
                subparsers[subaction.dest]['help'] = subaction.help

            subcommands = commandline.add_subcommands()
            for name, data in subparsers.items():
                subcmd = argumentparser_to_commandline(data['parser'], name, data['help'])
                subcommands.add_commandline_object(subcmd)
        elif not action.option_strings:
            if action.nargs in ('+', '*'):
                is_repeatable = True
            elif action.nargs in (1, None, '?'):
                is_repeatable = False
            else:
                is_repeatable = True
                utils.warn(f'Truncating nargs={action.nargs} of {action}')

            positional_number += 1
            commandline.add_positional(
                positional_number,
                metavar    = action.metavar or action.dest,
                complete   = get_complete(action),
                help       = action.help,
                repeatable = is_repeatable,
                when       = action.get_when()
            )
        else:
            complete = get_complete(action)
            optional_arg = False
            metavar = None
            help = None

            if action.nargs == '?':
                optional_arg = True
            elif action.nargs not in (None, 0, 1, True):
                utils.warn(f'Truncating nargs={action.nargs} of {action}')

            if complete:
                metavar = action.metavar or action.dest

            if action.help != argparse.SUPPRESS:
                help = action.help

            commandline.add_option(
                action.option_strings,
                metavar         = metavar,
                complete        = complete,
                help            = help,
                optional_arg    = optional_arg,
                repeatable      = action.get_repeatable(),
                final           = get_final(action),
                hidden          = (action.help == argparse.SUPPRESS),
                when            = action.get_when()
            )

    group_counter = 0
    for group in parser._mutually_exclusive_groups:
        group_counter += 1
        group_name = f'group{group_counter}'

        exclusive_group = MutuallyExclusiveGroup(commandline, group_name)
        for action in group._group_actions:
            for option in commandline.get_options():
                for option_string in action.option_strings:
                    if option_string in option.option_strings:
                        exclusive_group.add_option(option)
                        break

    return commandline

def find_objects_by_type(module, types):
    '''Search for objects in the specified module that match the given types.'''
    r = []

    for obj_name in dir(module):
        obj = getattr(module, obj_name)
        if isinstance(obj, types):
            r.append(obj)

    return r

def find_root_argument_parsers(module):
    '''Return a list of all ArgumentParser objects that have no parent.'''
    parsers = find_objects_by_type(module, argparse.ArgumentParser)
    actions = find_objects_by_type(module, argparse._SubParsersAction)

    for action in actions:
        for parser in action.choices.values():
            try:
                parsers.remove(parser)
            except ValueError:
                pass

    return parsers

def load_from_file(file, parser_variable=None, parser_blacklist=()):
    '''
    Load a Python file, search for the ArgumentParser object and convert
    it to a CommandLine object.
    '''
    try:
        module = file_loader.import_file(file)
    except Exception as e:
        utils.warn(e)
        utils.warn(f"Failed to load `{file}` using importlib, falling back to exec")
        module = file_loader.execute_file(file)

    if parser_variable is not None:
        try:
            parser = getattr(module, parser_variable)
        except AttributeError:
            raise CrazyError(f"No variable named `{parser_variable}` found in `{file}`") from None
    else:
        parsers = find_root_argument_parsers(module)
        for blacklisted in parser_blacklist:
            try:
                parsers.remove(blacklisted)
            except ValueError:
                pass
        if len(parsers) == 0:
            raise CrazyError(f"Could not find any ArgumentParser object in `{file}`")
        if len(parsers) > 1:
            raise CrazyError(f"Found too many ArgumentParser objects in `{file}`")
        parser = parsers[0]

    return argumentparser_to_commandline(parser)
