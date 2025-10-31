'''Conditions for Fish.'''

from . import when
from . import shell_parser
from .errors import InternalError
from .type_utils import is_list_type


class Condition:
    '''Base class for conditions.'''

    def query_code(self, ctxt):
        '''Returns code using the `query` function.'''
        raise NotImplementedError

    def unsafe_code(self, ctxt):
        '''Returns code using Fish's internal functions.'''
        raise NotImplementedError


class And(Condition):
    '''Logical and.'''

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def query_code(self, ctxt):
        left = self.left.query_code(ctxt)
        right = self.right.query_code(ctxt)
        return f'begin {left} && {right}; end'

    def unsafe_code(self, ctxt):
        left = self.left.unsafe_code(ctxt)
        right = self.right.unsafe_code(ctxt)
        return f'begin {left} && {right}; end'


class Or(Condition):
    '''Logical or.'''

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def query_code(self, ctxt):
        left = self.left.query_code(ctxt)
        right = self.right.query_code(ctxt)
        return f'begin {left} || {right}; end'

    def unsafe_code(self, ctxt):
        left = self.left.unsafe_code(ctxt)
        right = self.right.unsafe_code(ctxt)
        return f'begin {left} || {right}; end'


class Not(Condition):
    '''Logical not.'''

    def __init__(self, conditional):
        self.conditional = conditional

    def query_code(self, ctxt):
        return 'not %s' % self.conditional.query_code(ctxt)

    def unsafe_code(self, ctxt):
        return 'not %s' % self.conditional.unsafe_code(ctxt)


class HasOption(Condition):
    '''Checks if an option is present on command line.'''

    def __init__(self, option_strings):
        if not is_list_type(option_strings):
            raise InternalError('option_strings: Invalid type')

        self.option_strings = option_strings

    def query_code(self, ctxt):
        ctxt.helpers.use_function('query', 'has_option')
        options = ' '.join(self.option_strings)
        r = "$query '$opts' has_option %s" % options
        return r

    def unsafe_code(self, _ctxt):
        r = "__fish_seen_argument"

        for opt in self.option_strings:
            if opt.startswith('--'):
                r += ' -l %s' % opt.lstrip('-')
            elif len(opt) == 2:
                r += ' -s %s' % opt[1]
            else:
                r += ' -o %s' % opt.lstrip('-')

        return r


class HasHiddenOption(Condition):
    '''Checks if an incomplete option is present on command line.'''

    def __init__(self, option_strings):
        if not is_list_type(option_strings):
            raise InternalError('option_strings: Invalid type')

        self.option_strings = option_strings

    def query_code(self, ctxt):
        ctxt.helpers.use_function('query', 'has_option')
        ctxt.helpers.use_function('query', 'with_incomplete')
        options = ' '.join(self.option_strings)
        r = "$query '$opts' has_option WITH_INCOMPLETE %s" % options
        return r

    def unsafe_code(self, ctxt):
        return self.query_code(ctxt)


class OptionIs(Condition):
    '''Checks if an option has a specific value.'''

    def __init__(self, option_strings, values):
        if not is_list_type(option_strings):
            raise InternalError('option_strings: Invalid type')

        if not is_list_type(values):
            raise InternalError('values: Invalid type')

        self.option_strings = option_strings
        self.values = values

    def query_code(self, ctxt):
        ctxt.helpers.use_function('query', 'option_is')
        options = ' '.join(self.option_strings)
        values = ' '.join(self.values)
        r = "$query '$opts' option_is %s -- %s" % (options, values)
        return r

    def unsafe_code(self, ctxt):
        return self.query_code(ctxt)


class PositionalNum(Condition):
    '''Check the number of positionals.'''

    TEST_OPERATORS = {
        '==': '-eq',
        '!=': '-ne',
        '<=': '-le',
        '>=': '-ge',
        '<':  '-lt',
        '>':  '-gt',
    }

    def __init__(self, operator, number):
        if operator not in ('==', '!=', '<', '<=', '>', '>='):
            raise InternalError(f'operator: Invalid value: {operator}')

        if not isinstance(number, int):
            raise InternalError(f'number: Invalid type: {number}')

        self.operator = operator
        self.number = number

    def query_code(self, ctxt):
        ctxt.helpers.use_function('query', 'num_of_positionals')
        op = self.TEST_OPERATORS[self.operator]
        r = "$query '$opts' num_of_positionals %s %d" % (op, self.number - 1)
        return r

    def unsafe_code(self, _ctxt):
        op = self.TEST_OPERATORS[self.operator]
        r = "test (__fish_number_of_cmd_args_wo_opts) %s %d" % (op, self.number)
        return r


class PositionalContains(Condition):
    '''Checks if a positional contains a specific value.'''

    def __init__(self, number, values):
        if not isinstance(number, int):
            raise InternalError(f'number: Invalid type: {number}')

        if not is_list_type(values):
            raise InternalError(f'values: Invalid type: {values}')

        self.number = number
        self.values = values

    def query_code(self, ctxt):
        ctxt.helpers.use_function('query', 'positional_contains')
        values = ' '.join(self.values)
        r = "$query '$opts' positional_contains %d %s" % (self.number, values)
        return r

    def unsafe_code(self, _ctxt):
        values = ' '.join(self.values)
        r = "__fish_seen_subcommand_from %s" % values
        return r


def replace_commands(obj):
    '''Replace shell_parser/when objects by own condition objects.'''

    if isinstance(obj, shell_parser.And):
        left  = replace_commands(obj.left)
        right = replace_commands(obj.right)
        return And(left, right)

    if isinstance(obj, shell_parser.Or):
        left  = replace_commands(obj.left)
        right = replace_commands(obj.right)
        return Or(left, right)

    if isinstance(obj, shell_parser.Not):
        expr = replace_commands(obj.expr)
        return Not(expr)

    if isinstance(obj, when.OptionIs):
        return OptionIs(obj.options, obj.values)

    if isinstance(obj, when.HasOption):
        return HasOption(obj.options)

    raise AssertionError("Not reached")


class Conditions(Condition):
    '''Holds a list of conditions.'''

    def __init__(self):
        self.conditions = []

    def _optimized_conditions(self):
        positional_contains = []
        positional_num = []
        has_option = []
        other = []

        for condition in self.conditions:
            if isinstance(condition, PositionalContains):
                positional_contains.append(condition)
            elif isinstance(condition, PositionalNum):
                positional_num.append(condition)
            elif isinstance(condition, (HasHiddenOption, HasOption)):
                has_option.append(condition)
            else:
                other.append(condition)

        # positional_num is fastest, followed by positional_contains
        r = []
        r.extend(positional_num)
        r.extend(positional_contains)
        r.extend(has_option)
        r.extend(other)
        return r

    def query_code(self, ctxt):
        r = []
        for cond in self._optimized_conditions():
            r.append(cond.query_code(ctxt))
        return '"%s"' % ' && '.join(r)

    def unsafe_code(self, ctxt):
        r = []
        for cond in self._optimized_conditions():
            r.append(cond.unsafe_code(ctxt))
        return '"%s"' % ' && '.join(r)

    def add(self, condition):
        '''Add a condition.'''

        self.conditions.append(condition)

    def extend(self, conditions):
        '''Add many conditions.'''

        self.conditions.extend(conditions)

    def add_when(self, obj):
        '''Add when objects.'''

        if obj is None:
            return

        condition = replace_commands(obj)

        self.conditions.append(condition)
