'''Module for generating conditional code in Zsh.'''

from . import when
from . import shell


def _generate(query, tokens):
    '''Turn tokens/objects into condition code.'''

    r = []

    for obj in tokens:
        if isinstance(obj, when.OptionIs):
            r.append(_generate_option_is(query, obj))

        elif isinstance(obj, when.HasOption):
            r.append(_generate_has_option(query, obj))

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


def _generate_option_is(query, obj):
    func = query.use('option_is')
    args = [func, 'option_is', *obj.options, '--', *obj.values]
    return shell.join_quoted(args)


def _generate_has_option(query, obj):
    func = query.use('has_option')
    args = [func, 'has_option', *obj.options]
    return shell.join_quoted(args)


def generate_when_conditions(query, when_):
    '''Generate when condition code.'''

    tokens = when.parse_when(when_)
    return _generate(query, tokens)
