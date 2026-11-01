# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2025-2026 Benjamin Abendroth <braph93@gmx.de>

'''
Convert a completely flat or nested configuration to a crazy-complete node
tree.

The flat and nested formats store one list of completion words per command
context: plain words are subcommands, `<builtin>` words are built-in sources
and `$(...)` words are dynamic sources.  Nested configs (a tree of
`command: [...]` mappings) are first flattened; both formats share this
converter.
'''

import re

from ..errors import CrazyError
from .common import Node, source_to_completer


BUILTIN_WORD_RE = re.compile(r'^<(.+)>$')


def is_option_word(word):
    '''True if `word` is an option (starts with `-` and is longer than `-`).'''

    return isinstance(word, str) and word.startswith('-') and len(word) > 1


def collect_immediate_children(items):
    '''Collect the direct words of a context, stripping a single leading
    `*` or `+` marker.  '''

    children = []

    for item in items:
        word = next(iter(item.keys())) if isinstance(item, dict) else item
        children.append(re.sub(r'^[*+]', '', str(word)))

    return children


def generate_nested_prefix(prefix, key):
    '''Build the context prefix of a nested key relative to `prefix`.'''

    added = re.sub(r'^\+', '*', key)

    if not added.startswith('*'):
        added = ' ' + added

    return prefix + added


def process_key(prefix, items):
    '''Flatten one context and all of its nested contexts.'''

    result = {prefix: collect_immediate_children(items)}

    for item in items:
        if not isinstance(item, dict):
            continue
        key = next(iter(item.keys()))
        nested_items = next(iter(item.values()))
        nested_prefix = generate_nested_prefix(prefix, key)
        result.update(process_key(nested_prefix, nested_items))

    return result


def normalize_flat(config):
    '''Flatten a completely config to `{context: [words]}`.'''

    flat = {}

    for root_key, root_items in config.items():
        if not isinstance(root_items, list):
            continue
        flat.update(process_key(root_key, root_items))

    return flat


def split_contexts(flat):
    '''Split flat contexts into plain contexts and option value contexts.'''

    plain = {}
    value_contexts = {}

    for prefix, words in flat.items():
        if '*' in prefix:
            context, option = prefix.split('*', 1)
            value_contexts[(context, option)] = words
        else:
            plain[prefix] = words

    return plain, value_contexts


def is_subcommand(prefix, word, plain):
    '''True if `word` opens a deeper command context.'''

    return (prefix + ' ' + str(word)) in plain


def add_context_children(node, root_name, plain):
    '''Pre-create all child command nodes so parents can count subcommands.'''

    for prefix in plain:
        parts = prefix.split()

        if parts[0] != root_name:
            continue

        current = node

        for name in parts[1:]:
            if name not in current.children:
                current.children[name] = Node(name)
            current = current.children[name]


def add_context(node, prefix, plain, value_contexts):
    '''Derive the options and positionals of one command context.'''

    plain_prefix = prefix.split('*')[0]
    words = plain.get(plain_prefix, [])

    node.options = []
    node.positionals = []

    seen_options = set()
    builtin_positionals = []
    choices = []

    for word in words:
        if not isinstance(word, str):
            choices.append(word)
            continue

        if is_option_word(word):
            value_words = value_contexts.get((plain_prefix, word))

            option = {'option_strings': [word]}

            if value_words:
                option['complete'] = source_to_completer(value_words)

            if word not in seen_options:
                seen_options.add(word)
                node.options.append(option)
            continue

        if BUILTIN_WORD_RE.match(word):
            builtin_positionals.append(source_to_completer([word]))
            continue

        if is_subcommand(plain_prefix, word, plain):
            continue

        choices.append(word)

    for number, complete in enumerate(builtin_positionals, start=1):
        node.positionals.append({'number': number, 'complete': complete})

    if choices:
        number = len(builtin_positionals) + 1
        node.positionals.append({
            'number': number,
            'complete': ['choices', [str(word) for word in choices]],
        })


def convert(config):
    '''Convert a completely flat/nested config to a Node tree (root node).'''

    if not isinstance(config, dict):
        raise CrazyError('The completely flat config must be a mapping')

    flat = normalize_flat(config)

    if not flat:
        raise CrazyError('The completely config contains no commands')

    plain, value_contexts = split_contexts(flat)

    if not plain:
        raise CrazyError('The completely config contains no commands')

    programs = {prefix.split()[0] for prefix in plain}

    if len(programs) != 1:
        raise CrazyError('Too many main programs defined: ' + ', '.join(
            sorted(programs)))

    root_name = programs.pop()

    root = Node(root_name)
    add_context_children(root, root_name, plain)

    for prefix in plain:
        parts = prefix.split()

        if parts[0] != root_name:
            raise CrazyError('Unknown program name in ' + prefix)

        target = root

        for name in parts[1:]:
            target = target.children[name]

        add_context(target, prefix, plain, value_contexts)

    return root
