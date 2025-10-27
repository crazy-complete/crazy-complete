'''Conditions for Fish.'''

from . import when
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


class HasOption(Condition):
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


class Not(Condition):
    def __init__(self, conditional):
        self.conditional = conditional

    def query_code(self, ctxt):
        return 'not %s' % self.conditional.query_code(ctxt)

    def unsafe_code(self, ctxt):
        return 'not %s' % self.conditional.unsafe_code(ctxt)


class Conditions(Condition):
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
            elif isinstance(condition, HasOption):
                has_option.append(condition)
            else:
                other.append(condition)

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
        self.conditions.append(condition)

    def extend(self, conditions):
        self.conditions.extend(conditions)

    def add_when(self, obj):
        if obj is None:
            return

        if isinstance(obj, when.OptionIs):
            condition = OptionIs(obj.options, obj.values)
        elif isinstance(obj, when.HasOption):
            condition = HasOption(obj.options)
        else:
            raise AssertionError(f"Should not be reached: {obj}")

        self.conditions.append(condition)
