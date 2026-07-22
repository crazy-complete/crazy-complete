# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2025-2026 Benjamin Abendroth <braph93@gmx.de>

'''Code for creating when conditions in Bash.'''

from . import when
from . import shell


class ConditionGenerator:
    '''Class for generating conditions.'''

    def __init__(self, ctxt, commandline, variable_manager):
        self.ctxt = ctxt
        self.commandline = commandline
        self.variable_manager = variable_manager

    def generate(self, tokens):
        '''Turn tokens/objects into condition code.'''

        r = []

        for obj in tokens:
            if isinstance(obj, when.OptionIs):
                r.append(self._gen_option_is(obj))

            elif isinstance(obj, when.OptionMatch):
                r.append(self._gen_option_match(obj))

            elif isinstance(obj, when.HasOption):
                r.append(self._gen_has_option(obj))

            elif isinstance(obj, when.PositionalCount):
                r.append(self._gen_positional_count(obj))

            elif isinstance(obj, when.PositionalContains):
                r.append(self._gen_positional_contains(obj))

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
        variables = []
        conditions = []

        if obj.ignore_case:
            func = self.ctxt.helpers.use_function('array_contains_nocase')
        else:
            func = self.ctxt.helpers.use_function('array_contains')

        for o in self.commandline.get_options_by_option_strings(obj.options):
            variables.append(self.variable_manager.capture_variable(o))

        variables = ' '.join('"${%s[@]}"' % v for v in variables)

        for value in obj.values:
            value = shell.quote(value)
            conditions.append(f'{func} {value} {variables}')

        if len(conditions) == 1:
            return conditions[0]

        return '{ %s; }' % ' || '.join(conditions)

    def _gen_option_match(self, obj):
        variables = []
        regex = shell.quote(obj.regex)
        func = self.ctxt.helpers.use_function('array_match')

        for o in self.commandline.get_options_by_option_strings(obj.options):
            variables.append(self.variable_manager.capture_variable(o))

        variables = ' '.join('"${%s[@]}"' % v for v in variables)

        if obj.ignore_case:
            return f'{func} -i -- {regex} {variables}'
        else:
            return f'{func} -- {regex} {variables}'

    def _gen_has_option(self, obj):
        conditions = []

        for o in self.commandline.get_options_by_option_strings(obj.options):
            cond = '${#%s[@]}' % self.variable_manager.capture_variable(o)
            conditions.append(cond)

        return f'(( {" + ".join(conditions)} ))'

    def _gen_positional_count(self, obj):
        return f'(( ${{#POSITIONALS[@]}} {obj.operator} {obj.number} ))'

    def _gen_positional_contains(self, obj):
        func = self.ctxt.helpers.use_function('array_contains')
        index = obj.number - 1
        values = shell.join_quoted(obj.values)
        return f'{func} "${{POSITIONALS[{index}]}}" {values}'


def generate_when_conditions(ctxt, commandline, variable_manager, when_):
    '''Generate when condition code.'''

    tokens = when.parse_when(when_)
    generator = ConditionGenerator(ctxt, commandline, variable_manager)
    return generator.generate(tokens)
