'''Module for generating conditional code in Zsh.'''

from . import when
from . import shell


class ConditionGenerator:
    '''Class for generating conditions.'''

    def __init__(self, query):
        self.query = query

    def generate(self, tokens):
        '''Turn tokens/objects into condition code.'''

        r = []

        for obj in tokens:
            if isinstance(obj, when.OptionIs):
                r.append(self._gen_option_is(obj))

            elif isinstance(obj, when.HasOption):
                r.append(self._gen_has_option(obj))

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

    def _gen_option_is(self, obj):
        func = self.query.use('option_is')
        args = [func, 'option_is', *obj.options, '--', *obj.values]
        return ' '.join(shell.escape(a) for a in args)

    def _gen_has_option(self, obj):
        func = self.query.use('has_option')
        args = [func, 'has_option', *obj.options]
        return ' '.join(shell.escape(a) for a in args)


def generate_when_conditions(query, when_):
    '''Generate when condition code.'''

    tokens = when.parse_when(when_)
    generator = ConditionGenerator(query)
    return generator.generate(tokens)
