# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2025-2026 Benjamin Abendroth <braph93@gmx.de>

'''Conditions for Fish.'''

import re

from . import cli
from . import when
from . import shell
from .errors import InternalError
from .type_utils import is_list_type


def escape_in_double(string):
    '''Escape special characters in a double quoted string.'''

    return re.sub(r'(["$`\\])', r'\\\1', string)


def make_condition_command(prefix, args):
    '''Make a condition command.

    In our completion scripts, we use variables like $has_option,
    $positional_contains, $num_of_positionals etc.

    We generate code like this:

        complete -n "$has_option -f --foo"

    This function generates such a condition command.

    We have to ensure proper escaping inside the double quotes.
    '''

    args_quoted = [shell.quote(arg) for arg in args]
    args_quoted = [escape_in_double(arg) for arg in args_quoted]
    return '%s %s' % (prefix, ' '.join(args_quoted))


class Condition:
    '''Base class for conditions.'''

    def get_code(self, ctxt):
        '''Returns the condition code.'''
        raise NotImplementedError


class Not(Condition):
    '''Logical not.'''

    def __init__(self, conditional):
        self.conditional = conditional

    def get_code(self, ctxt):
        return 'not %s' % self.conditional.get_code(ctxt)


class HasOption(Condition):
    '''Checks if an option is present on command line.'''

    def __init__(self, option_strings):
        if not is_list_type(option_strings):
            raise InternalError('option_strings: Invalid type')

        self.option_strings = option_strings

    def get_code(self, ctxt):
        ctxt.helpers.use_function('has_option')
        return make_condition_command('$has_option', self.option_strings)


class HasHiddenOption(Condition):
    '''Checks if an incomplete option is present on command line.'''

    def __init__(self, option_strings):
        if not is_list_type(option_strings):
            raise InternalError('option_strings: Invalid type')

        self.option_strings = option_strings

    def get_code(self, ctxt):
        ctxt.helpers.use_function('has_option')
        ctxt.helpers.use_function('has_option', 'with_incomplete')
        options = self.option_strings
        return make_condition_command('$has_option', ['WITH_INCOMPLETE'] + options)


class OptionIs(Condition):
    '''Checks if an option has a specific value.'''

    def __init__(self, option_strings, values, ignore_case, any_options):
        if not is_list_type(option_strings):
            raise InternalError('option_strings: Invalid type')

        if not is_list_type(values):
            raise InternalError('values: Invalid type')

        self.option_strings = option_strings
        self.values = values
        self.ignore_case = ignore_case
        self.any_options = any_options

    def get_code(self, ctxt):
        args = ['--', *self.option_strings, '--', *self.values]
        ctxt.helpers.use_function('option_is')

        if self.any_options:
            ctxt.helpers.use_function('option_is', 'any')
            args.insert(0, '-a')

        if self.ignore_case:
            ctxt.helpers.use_function('option_is', 'nocase')
            args.insert(0, '-i')

        return make_condition_command('$option_is', args)


class OptionMatch(Condition):
    '''Checks if an option's value matches a regex'''

    def __init__(self, option_strings, regex, ignore_case, any_options):
        if not is_list_type(option_strings):
            raise InternalError('option_strings: Invalid type')

        if not isinstance(regex, str):
            raise InternalError('regex: Invalid type')

        self.option_strings = option_strings
        self.regex = regex
        self.ignore_case = ignore_case
        self.any_options = any_options

    def get_code(self, ctxt):
        ctxt.helpers.use_function('option_match')
        args = ['--', *self.option_strings, '--', self.regex]

        if self.any_options:
            ctxt.helpers.use_function('option_match', 'any')
            args.insert(0, '-a')

        if self.ignore_case:
            ctxt.helpers.use_function('option_match', 'nocase')
            args.insert(0, '-i')

        return make_condition_command('$option_match', args)


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

    def get_code(self, ctxt):
        ctxt.helpers.use_function('num_of_positionals')
        op = self.TEST_OPERATORS[self.operator]
        return make_condition_command('$num_of_positionals', [op, str(self.number)])


class PositionalContains(Condition):
    '''Checks if a positional contains a specific value.'''

    def __init__(self, number, values, ignore_case=False):
        if not isinstance(number, int):
            raise InternalError(f'number: Invalid type: {number}')

        if not is_list_type(values):
            raise InternalError(f'values: Invalid type: {values}')

        self.number = number
        self.values = values
        self.ignore_case = ignore_case

    def get_code(self, ctxt):
        ctxt.helpers.use_function('positional_contains')
        args = [str(self.number), *self.values]

        if self.ignore_case:
            ctxt.helpers.use_function('positional_contains', 'nocase')
            args.insert(0, '-i')

        return make_condition_command('$positional_contains', args)


def replace_commands(tokens):
    '''Replace when objects by own condition objects.'''

    r = []

    for obj in tokens:
        if isinstance(obj, when.OptionIs):
            r.append(OptionIs(obj.options, obj.values, obj.ignore_case, obj.any))

        elif isinstance(obj, when.OptionMatch):
            r.append(OptionMatch(obj.options, obj.regex, obj.ignore_case, obj.any))

        elif isinstance(obj, when.HasOption):
            r.append(HasOption(obj.options))

        elif isinstance(obj, when.PositionalCount):
            r.append(PositionalNum(obj.operator, obj.number))

        elif isinstance(obj, when.PositionalContains):
            r.append(PositionalContains(obj.number, obj.values, obj.ignore_case))

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

    def get_conditions(self, ctxt):
        conditions = []

        for condition in self._optimized_conditions():
            conditions.append('"%s"' % condition.get_code(ctxt))

        if self.when:
            r = []
            for obj in self.when:
                if obj == '(':
                    r.append('begin')
                elif obj == ')':
                    r.append(';end')
                elif obj in ('!', '&&', '||'):
                    r.append(obj)
                else:
                    r.append(obj.get_code(ctxt))
            conditions.append('"%s"' % ' '.join(r))

        return conditions

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
