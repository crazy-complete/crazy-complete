# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2025-2026 Benjamin Abendroth <braph93@gmx.de>

'''Module for generating conditional code in Zsh.'''

from . import when
from . import shell


def _generate(ctxt, query, tokens):
    '''Turn tokens/objects into condition code.'''

    r = []

    for obj in tokens:
        if isinstance(obj, when.OptionIs):
            r.append(_generate_option_is(ctxt, query, obj))

        elif isinstance(obj, when.OptionMatch):
            r.append(_generate_option_match(ctxt, query, obj))

        elif isinstance(obj, when.HasOption):
            r.append(_generate_has_option(ctxt, query, obj))

        elif isinstance(obj, when.PositionalCount):
            r.append(_generate_positional_count(ctxt, query, obj))

        elif isinstance(obj, when.PositionalContains):
            r.append(_generate_positional_contains(ctxt, query, obj))

        elif obj in ('&&', '||', '!'):
            r.append(obj)

        elif obj == '(':
            r.append('{')

        elif obj == ')':
            r.append(';}')

        else:
            raise AssertionError("Not reached")

    if when.needs_braces(tokens):
        return '{ %s; }' % ' '.join(r)

    return ' '.join(r)


def _generate_option_is(ctxt, query, obj):
    func = query.use('option_is')
    args = ['--', *obj.options, '--', *obj.values]

    if obj.any:
        query.use('any')
        args.insert(0, '-a')

    if obj.ignore_case:
        query.use('nocase')
        args.insert(0, '-i')

    return shell.join_quoted([func, 'option_is'] + args)


def _generate_option_match(ctxt, query, obj):
    query.use() # option_match also needs query!
    func = ctxt.helpers.use_function('option_match')
    args = ['--', *obj.options, '--', obj.regex]

    if obj.any:
        ctxt.helpers.use_function('option_match', 'any')
        args.insert(0, '-a')

    if obj.ignore_case:
        ctxt.helpers.use_function('option_match', 'nocase')
        args.insert(0, '-i')

    return shell.join_quoted([func] + args)


def _generate_has_option(_ctxt, query, obj):
    func = query.use('has_option')
    args = [func, 'has_option', *obj.options]
    return shell.join_quoted(args)


def _generate_positional_count(_ctxt, _query, obj):
    return f'(( ${{#POSITIONALS[@]}} {obj.operator} {obj.number} ))'


def _generate_positional_contains(ctxt, _query, obj):
    func = ctxt.helpers.use_function('array_contains')
    values = shell.join_quoted(obj.values)
    return f'{func} "${{POSITIONALS[{obj.number}]}}" {values}'


def generate_when_conditions(ctxt, query, when_):
    '''Generate when condition code.'''

    tokens = when.parse_when(when_)
    return _generate(ctxt, query, tokens)
