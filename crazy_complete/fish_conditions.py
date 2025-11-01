'''Conditions for Fish.'''

import re

from . import when
from . import shell
from .errors import InternalError
from .type_utils import is_list_type


def escape_in_double(string):
    '''Escape special characters in a double quoted string.'''

    return re.sub(r'(["$`\\])', r'\\\1', string)


def make_condition_command(prefix, args):
    '''Make a condition command.

    In our completion scripts, we use the variables $query and $opts.

    We generate code like this:

        complete -n "$query '$opts' has_option --foo"

    This function generates such a condition command.

    We have to ensure proper escaping inside the double quotes.
    '''

    args_escaped = [shell.escape(arg) for arg in args]
    args_escaped = [escape_in_double(arg) for arg in args_escaped]
    return '%s %s' % (prefix, ' '.join(args_escaped))


def make_query(args):
    '''Make a query command.'''

    return make_condition_command("$query '$opts'", args)



class Condition:
    '''Base class for conditions.'''

    def query_code(self, ctxt):
        '''Returns code using the `query` function.'''
        raise NotImplementedError

    def unsafe_code(self, ctxt):
        '''Returns code using Fish's internal functions.'''
        raise NotImplementedError


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
        return make_query(['has_option'] + self.option_strings)

    def unsafe_code(self, _ctxt):
        args = []

        for opt in self.option_strings:
            if opt.startswith('--'):
                args += ['-l', opt.lstrip('-')]
            elif len(opt) == 2:
                args += ['-s', opt[1]]
            else:
                args += ['-o', opt.lstrip('-')]

        return make_condition_command('__fish_seen_argument', args)


class HasHiddenOption(Condition):
    '''Checks if an incomplete option is present on command line.'''

    def __init__(self, option_strings):
        if not is_list_type(option_strings):
            raise InternalError('option_strings: Invalid type')

        self.option_strings = option_strings

    def query_code(self, ctxt):
        ctxt.helpers.use_function('query', 'has_option')
        ctxt.helpers.use_function('query', 'with_incomplete')
        options = self.option_strings
        return make_query(['has_option', 'WITH_INCOMPLETE'] + options)

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
        options = self.option_strings
        values = self.values
        return make_query(['option_is', *options, '--', *values])

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
        return make_query(['num_of_positionals', op, str(self.number - 1)])

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
        values = self.values
        number = str(self.number)
        return make_query(['positional_contains', number, *values])

    def unsafe_code(self, _ctxt):
        values = self.values
        return make_condition_command('__fish_seen_subcommand_from', values)


def replace_commands(tokens):
    '''Replace when objects by own condition objects.'''

    r = []

    for obj in tokens:
        if isinstance(obj, when.OptionIs):
            r.append(OptionIs(obj.options, obj.values))

        elif isinstance(obj, when.HasOption):
            r.append(HasOption(obj.options))

        elif isinstance(obj, str):
            r.append(obj)

        else:
            raise AssertionError("Not reached")

    return r


class Conditions(Condition):
    '''Holds a list of conditions.'''

    def __init__(self):
        self.conditions = []
        self.when = None

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

    def _get_tokens(self):
        r = []

        for condition in self._optimized_conditions():
            r.append(condition)
            r.append('&&')

        if self.when:
            if r and when.needs_braces(self.when):
                r += ['(', *self.when, ')']
            else:
                r += self.when

        if r and r[-1] == '&&':
            r.pop(-1)

        return r

    def query_code(self, ctxt):
        r = []
        for obj in self._get_tokens():
            if obj == '(':
                r.append('begin')
            elif obj == ')':
                r.append(';end')
            elif obj in ('!', '&&', '||'):
                r.append(obj)
            else:
                r.append(obj.query_code(ctxt))
        return '"%s"' % ' '.join(r)

    def unsafe_code(self, ctxt):
        r = []
        for obj in self._get_tokens():
            if obj == '(':
                r.append('begin')
            elif obj == ')':
                r.append(';end')
            elif obj in ('!', '&&', '||'):
                r.append(obj)
            else:
                r.append(obj.unsafe_code(ctxt))
        return '"%s"' % ' '.join(r)

    def add(self, condition):
        '''Add a condition.'''

        self.conditions.append(condition)

    def extend(self, conditions):
        '''Add many conditions.'''

        self.conditions.extend(conditions)

    def add_when(self, tokens):
        '''Add when objects.'''

        if not tokens:
            return

        self.when = replace_commands(tokens)
