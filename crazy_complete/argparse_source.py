#!/usr/bin/python3

import sys
import argparse

from . import file_loader
from . import utils
from .commandline import *

def get_complete(action):
    if isinstance(action, argparse._HelpAction):
        return None
    elif isinstance(action, argparse._VersionAction):
        return None
    elif isinstance(action, argparse._StoreTrueAction) or \
         isinstance(action, argparse._StoreFalseAction) or \
         isinstance(action, argparse._StoreConstAction) or \
         isinstance(action, argparse._AppendConstAction) or \
         isinstance(action, argparse._CountAction):

        if action.get_complete():
            raise Exception('Action has complete but takes no arguments', action)

        return None
    elif isinstance(action, argparse._StoreAction) or \
         isinstance(action, argparse._ExtendAction) or \
         isinstance(action, argparse._AppendAction):

        if action.choices and action.get_complete():
            raise Exception('Action has both choices and complete set', action)

        if action.choices:
            if isinstance(action.choices, range):
                if action.choices.step == 1:
                    complete = ('range', action.choices.start, action.choices.stop)
                else:
                    complete = ('range', action.choices.start, action.choices.stop, action.choices.step)
            else:
                complete = ('choices', action.choices)
        else:
            complete = action.get_complete()

        return complete

    elif isinstance(action, argparse.BooleanOptionalAction):
        raise Exception("not supported")

    raise Exception('Unknown action: %r' % action)

def ArgumentParser_to_CommandLine(parser, prog=None, description=None):
    '''
    Converts an ArgumentParser object to a CommandLine object.

    Args:
        parser (argparse.ArgumentParser): The ArgumentParser object to convert.
        prog (str, optional): The name of the program. Defaults to the program name of the parser.
        description (str, optional): The description of the program. Defaults to the description of the parser.

    Returns:
        CommandLine: A CommandLine object representing the converted parser.
    '''

    if not description:
        description = parser.description

    if not prog:
        prog = parser.prog

    commandline = CommandLine(prog, help=description, aliases=parser.get_aliases())
    number = 0

    for action in parser._actions:
        if isinstance(action, argparse._SubParsersAction):
            subparsers  = OrderedDict()

            for name, subparser in action.choices.items():
                subparsers[name] = {'parser': subparser, 'help': ''}

            for action in action._get_subactions():
                subparsers[action.dest]['help'] = action.help

            subp = commandline.add_subcommands(name='command', help='Subcommands')

            for name, data in subparsers.items():
                suboptions = ArgumentParser_to_CommandLine(data['parser'], name, data['help'])
                subp.add_commandline_object(suboptions)
        elif not action.option_strings:
            if action.nargs in ('+', '*'):
                is_repeatable = True
            elif action.nargs in (1, None, '?'):
                is_repeatable = False
            else:
                raise Exception("Invalid nargs: %r" % action)

            number += 1
            commandline.add_positional(
                number,
                metavar=action.metavar or action.dest,
                complete=get_complete(action),
                help=action.help,
                repeatable=is_repeatable,
                when=action.get_when()
            )
        else:
            if action.nargs is None or action.nargs == 1:
                takes_args = True
            elif action.nargs == '?':
                takes_args = '?'
            elif action.nargs == 0:
                takes_args = False
            else:
                utils.warn('Truncating %r nargs' % action)

            metavar = None
            if takes_args:
                metavar = action.metavar or action.dest

            commandline.add_option(
                action.option_strings,
                metavar=metavar,
                complete=get_complete(action),
                help=action.help,
                takes_args=takes_args,
                multiple_option=action.get_multiple_option(),
                when=action.get_when()
            )

    group_counter = 0
    for group in parser._mutually_exclusive_groups:
        group_counter += 1
        group_name = 'group%d' % group_counter

        exclusive_group = MutuallyExclusiveGroup(commandline, group_name)
        for action in group._group_actions:
            for option in commandline.get_options():
                for option_string in action.option_strings:
                    if option_string in option.option_strings:
                        exclusive_group.add_option(option)
                        break

    return commandline

def find_objects_by_type(module, type):
    r = []

    for obj_name in dir(module):
        obj = getattr(module, obj_name)
        if isinstance(obj, type):
            r.append(obj)

    return r

def find_RootArgumentParsers(module):
    ArgumentParsers = find_objects_by_type(module, argparse.ArgumentParser)
    SubParsersActions  = find_objects_by_type(module, argparse._SubParsersAction)

    for action in SubParsersActions:
        for parser in action.choices.values():
            try:
                ArgumentParsers.remove(parser)
            except:
                pass

    return ArgumentParsers

def load_from_file(file, parser_variable=None, parser_blacklist=[]):
    try:
        module = file_loader.import_file(file)
    except Exception as e:
        utils.warn(e)
        utils.warn("Failed to load `%s` using importlib, falling back to `exec`" % file, file=sys.stderr)
        module = file_loader.execute_file(file)

    if parser_variable is not None:
        try:
            parser = getattr(module, parser_variable)
        except:
            raise Exception("No variable named `%s` found in `%s`" % (parser_variable, file))
    else:
        parsers = find_RootArgumentParsers(module)
        for blacklisted in parser_blacklist:
            try:    parsers.remove(blacklisted)
            except: pass
        if len(parsers) == 0:
            raise Exception("Could not find any ArgumentParser object in `%s`" % file)
        elif len(parsers) > 1:
            raise Exception("Found too many ArgumentParser objects in `%s`" % file)
        parser = parsers[0]

    return ArgumentParser_to_CommandLine(parser)

