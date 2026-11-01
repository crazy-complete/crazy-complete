# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2025-2026 Benjamin Abendroth <braph93@gmx.de>

"""
This module contains code that is shared by the completely converters:
the mapping from completely sources to crazy-complete completers, and the
conversion of the internal node model to crazy-complete dictionaries.
"""

import re

from .. import utils


# crazy-complete completer names for the known completely built-in sources
BUILTIN_MAP = {
    'file':       'file',
    'directory':  'directory',
    'user':       'user',
    'command':    'command',
    'group':      'group',
    'hostname':   'hostname',
    'service':    'service',
    'signal':     'signal',
    'variable':   'variable',
    'export':     'environment',
}


def exec_inner(text):
    '''Return the command of a `$(command)` word with the wrapper removed.

    Only the leading `$(` and the final `)` are stripped.  The command
    itself is kept as-is.  '''

    inner = text[2:]          # strip leading '$('
    if inner.endswith(')'):
        inner = inner[:-1]   # strip the final ')'
    if inner.startswith(' '):
        inner = inner[1:]    # strip one optional leading space
    return inner


def classify_word(word):
    '''Classify a single completely source word.

    Returns one of:
        None                  for `~` / null
        ('literal', value)    for plain words, numbers and `++word`
        ('builtin', name)     for `+name` and `<name>`
        ('exec', command)     for `$(command)`
    '''

    if word is None:
        return None

    if isinstance(word, (int, float)):
        return ('literal', str(word))

    text = str(word)

    if text.startswith('++'):
        return ('literal', text[1:])

    if text.startswith('$('):
        return ('exec', exec_inner(text))

    if text.startswith('+'):
        return ('builtin', text[1:])

    match = re.match(r'^<(.+?)>$', text)
    if match:
        return ('builtin', match.group(1))

    return ('literal', text)


def builtin_completer(name):
    '''Map a completely built-in source name to a crazy-complete completer.'''

    if name in BUILTIN_MAP:
        return [BUILTIN_MAP[name]]

    utils.print_err(
        'Unknown completion source `+%s`. Falling back to `none`.' % name)
    return ['none']


def completer_from_classified(classified):
    '''Build a crazy-complete completer from a list of classified items.

    classified is a list of (kind, value) tuples as returned by
    classify_word().  Items that could not be resolved to a completer
    (i.e. ['none']) are dropped; if all of them are dropped the result is
    ['none'].  '''

    items = [item for item in classified if item is not None]

    if not items:
        return ['none']

    if all(kind == 'literal' for kind, _ in items):
        return ['choices', [value for _, value in items]]

    completers = []
    for kind, value in items:
        if kind == 'literal':
            completers.append(['choices', [value]])
        elif kind == 'builtin':
            completers.append(builtin_completer(value))
        else:
            completers.append(['exec', value])

    completers = [completer for completer in completers if completer != ['none']]

    if not completers:
        return ['none']

    if len(completers) == 1:
        return completers[0]

    return ['combine', completers]


def source_to_completer(source):
    '''Convert a completely source (a single word or a list of words) to a
    crazy-complete completer list.  '''

    items = source if isinstance(source, (list, tuple)) else [source]
    classified = [classify_word(item) for item in items]
    return completer_from_classified(classified)


# -----------------------------------------------------------------------------
# Internal node model
# -----------------------------------------------------------------------------

class Node:
    '''Internal representation of a single command in the completion tree.'''

    def __init__(self, name):
        self.name = name
        self.aliases = []
        self.option_group_names = []
        self.options = []
        self.positionals = []
        self.children = {}


def merge_aliases(target, word):
    '''Merge the aliases of `word` into the `target` node (order preserved).'''

    names = [target.name] + target.aliases + [word['name']] + word['aliases']
    aliases = []

    for name in names:
        if name == target.name or name in aliases:
            continue
        aliases.append(name)

    target.aliases = aliases


def node_to_dictionaries(root):
    '''Convert a Node tree to a list of crazy-complete commandline dicts.'''

    dictionaries = []

    def walk(node, path):
        dictionary = {'prog': ' '.join(path)}

        if node.aliases:
            dictionary['aliases'] = node.aliases

        if node.options:
            dictionary['options'] = node.options

        if node.positionals:
            dictionary['positionals'] = node.positionals

        dictionaries.append(dictionary)

        for child in node.children.values():
            walk(child, path + [child.name])

    walk(root, [root.name])
    return dictionaries
