'''Module for generating conditional code in Zsh.'''

from . import when
from . import shell
from . import shell_parser


class ConditionGenerator:
    '''Class for generating conditions.'''

    def __init__(self, query):
        self.query = query

    def generate(self, obj):
        '''Turn object into condition code.'''

        if isinstance(obj, when.OptionIs):
            return self._gen_option_is(obj)

        if isinstance(obj, when.HasOption):
            return self._gen_has_option(obj)

        if isinstance(obj, shell_parser.And):
            left = self.generate(obj.left)
            right = self.generate(obj.right)
            return f'{{ {left} && {right}; }}'

        if isinstance(obj, shell_parser.Or):
            left = self.generate(obj.left)
            right = self.generate(obj.right)
            return f'{{ {left} || {right}; }}'

        if isinstance(obj, shell_parser.Not):
            expr = self.generate(obj.expr)
            return f'! {expr}'

        raise AssertionError("Not reached")

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

    parsed = when.parse_when(when_)
    generator = ConditionGenerator(query)
    return generator.generate(parsed)
