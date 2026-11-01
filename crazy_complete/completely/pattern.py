# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2025-2026 Benjamin Abendroth <braph93@gmx.de>

'''
Convert a completely pattern configuration to a crazy-complete node tree.

The pattern format (see the completely documentation) stores its completion
rules in three sections: `patterns` (command trees), `options` (groups of
options) and `tokens` (positional arguments with their sources).  This module
re-implements the completely logic in Python and produces the same
command/option/positional structure.
'''

import re

from ..errors import CrazyError
from .common import Node, merge_aliases, source_to_completer


TOKEN_NAME_RE = re.compile(r'^<(.+)>$')
OPTION_PARTS_RE = re.compile(r'<[^>]+>|\([^)]+\)|\S+')
PATTERN_PARTS_RE = re.compile(r'\[[^\]]+\]|<[^>]+>\.\.\.|<[^>]+>|\S+')
TOKEN_PART_RE = re.compile(r'^<[^>]+>(\.\.\.)?$')


def is_option_group(part):
    '''True if `part` is an option group reference like `[group options]`.'''

    return part.startswith('[') and part.endswith(']')


def is_token(part):
    '''True if `part` is a token reference like `<source>` or `<source>...`.'''

    return bool(TOKEN_PART_RE.match(part))


def option_group_name(part):
    '''Extract the group name from an option group reference.'''

    name = part[1:-1]
    match = re.search(r'\s+options$', name)
    if match:
        name = name[:match.start()]
    return name


def token_name(part):
    '''Extract the token name from a token reference (drops `...`).'''

    if part.endswith('...'):
        part = part[:-3]
    match = TOKEN_NAME_RE.match(part)
    return match.group(1) if match else part


def pattern_parts(pattern):
    '''Split a pattern into its parts (commands, option groups, tokens).'''

    return PATTERN_PARTS_RE.findall(pattern)


def option_parts(entry):
    '''Split an option entry into its words.'''

    return OPTION_PARTS_RE.findall(entry)


def parse_word(part):
    '''Split a command part on `|` into {name, aliases}.'''

    names = part.split('|')
    return {'name': names[0], 'aliases': names[1:]}


def parse_token(part, tokens):
    '''Convert a token reference to a crazy-complete positional dict.'''

    repeatable = part.endswith('...')
    name = token_name(part)

    if name not in tokens:
        raise CrazyError('Unknown token `%s`' % name)

    positional = {
        'metavar': name,
        'complete': source_to_completer(tokens[name]),
    }

    if repeatable:
        positional['repeatable'] = True

    return positional


def parse_option(entry, tokens):
    '''Convert a single option entry to a crazy-complete option dict.'''

    parts = option_parts(entry)

    if not parts:
        raise CrazyError('Invalid option syntax: ' + entry)

    names = parts[0].split('|')
    option = {'option_strings': names}

    value_part = None
    metadata = []

    for part in parts[1:]:
        if value_part is None and is_token(part):
            value_part = part
        elif part.startswith('(') and part.endswith(')'):
            metadata.append(part)
        else:
            raise CrazyError('Invalid option syntax: ' + entry)

    if value_part is not None:
        positional = parse_token(value_part, tokens)
        option['metavar'] = positional['metavar']
        option['complete'] = positional['complete']

    for part in metadata:
        if part == '(repeatable)':
            option['repeatable'] = True
        else:
            raise CrazyError('Unknown option metadata: ' + part)

    return option


def find_or_create_child(node, word):
    '''Return the child node for `word`, creating or merging it if needed.'''

    names = set([word['name']] + word['aliases'])

    for child in node.children.values():
        if names & set([child.name] + child.aliases):
            merge_aliases(child, word)
            return child

    child = Node(word['name'])
    child.aliases = word['aliases']
    node.children[child.name] = child
    return child


def referenced_options(patterns):
    '''Collect the option group names referenced by `patterns`.'''

    groups = set()

    for pattern in patterns:
        for part in pattern_parts(pattern):
            if is_option_group(part):
                groups.add(option_group_name(part))

    return groups


def referenced_tokens(patterns, option_groups):
    '''Collect the token names referenced by patterns and option groups.'''

    tokens = set()

    for pattern in patterns:
        for part in pattern_parts(pattern):
            if is_token(part):
                tokens.add(token_name(part))

    for entries in option_groups.values():
        for entry in entries:
            for part in option_parts(entry)[1:]:
                if is_token(part):
                    tokens.add(token_name(part))

    return tokens


def check_repeatable_positional(pattern):
    '''A repeatable positional must be the last positional in its pattern.'''

    tokens = [part for part in pattern_parts(pattern) if is_token(part)]

    for part in tokens[:-1]:
        if part.endswith('...'):
            raise CrazyError(
                'Repeatable positional must be the last positional: ' + pattern)


def finalize(node, parsed_options):
    '''Fill the options and positional numbers of the node tree.'''

    options = {}

    for name in node.option_group_names:
        if name not in parsed_options:
            raise CrazyError('Unknown option group `%s`' % name)
        for option in parsed_options[name]:
            key = tuple(option['option_strings'])
            if key not in options:
                options[key] = option

    node.options = list(options.values())

    for number, positional in enumerate(node.positionals, start=1):
        positional['number'] = number

    for child in node.children.values():
        finalize(child, parsed_options)


def convert(config):
    '''Convert a completely pattern config to a Node tree (root node).'''

    if not isinstance(config, dict):
        raise CrazyError('The completely pattern config must be a mapping')

    patterns = config.get('patterns')

    if not isinstance(patterns, list) or not patterns:
        raise CrazyError('The pattern config needs a non-empty `patterns` list')

    option_groups = config.get('options') or {}
    token_sources = config.get('tokens') or {}

    programs = []

    for pattern in patterns:
        for part in pattern_parts(pattern):
            if not is_option_group(part) and not is_token(part):
                programs.append(parse_word(part)['name'])
                break

    if not programs:
        raise CrazyError('No program name found in the patterns')

    unique = sorted(set(programs))

    if len(unique) != 1:
        raise CrazyError('Too many main programs defined: ' + ', '.join(unique))

    parsed_options = {}

    for name, entries in option_groups.items():
        if not isinstance(entries, list):
            raise CrazyError('The option group `%s` must be a list' % name)
        parsed_options[name] = [parse_option(entry, token_sources)
                                for entry in entries]

    missing = sorted(referenced_options(patterns)
                     - set(parsed_options.keys()))

    if missing:
        raise CrazyError('Unknown option group: ' + ', '.join(missing))

    missing = sorted(referenced_tokens(patterns, option_groups)
                     - set(token_sources.keys()))

    if missing:
        raise CrazyError('Unknown token: ' + ', '.join(missing))

    for pattern in patterns:
        check_repeatable_positional(pattern)

    root = None

    for pattern in patterns:
        current = None

        for part in pattern_parts(pattern):
            if is_option_group(part):
                if current is None:
                    raise CrazyError(
                        'Option group before the command name: ' + pattern)
                name = option_group_name(part)
                if name not in current.option_group_names:
                    current.option_group_names.append(name)
            elif is_token(part):
                if current is None:
                    raise CrazyError('Token before the command name: ' + pattern)
                current.positionals.append(parse_token(part, token_sources))
            else:
                word = parse_word(part)

                if current is None:
                    if root is None:
                        root = Node(word['name'])
                        root.aliases = list(word['aliases'])
                    else:
                        merge_aliases(root, word)
                    current = root
                else:
                    current = find_or_create_child(current, word)

    if root is None:
        raise CrazyError('No program name found in the patterns')

    finalize(root, parsed_options)

    return root
