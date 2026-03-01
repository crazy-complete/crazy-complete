# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2025-2026 Benjamin Abendroth <braph93@gmx.de>

'''This module contains code for completing option strings in Bash.'''

from collections import namedtuple

from . import cli
from . import algo
from . import shell
from . import bash_when
from .str_utils import indent


_Option = namedtuple('_Option', ('option', 'conditions', 'when'))


def _make_option_strings(ctxt, options):
    opt_strings = []

    for opt in options:
        opt_strings.extend(opt.get_short_option_strings())

        add_equal_sign = (
            opt.has_optional_arg() or
            (opt.has_required_arg() and ctxt.config.long_options_append_equal)
        )

        if add_equal_sign:
            opt_strings.extend(f'{s}=' for s in opt.get_long_option_strings())
            opt_strings.extend(f'{s}=' for s in opt.get_old_option_strings())
        else:
            opt_strings.extend(opt.get_long_option_strings())
            opt_strings.extend(opt.get_old_option_strings())

    return shell.join_quoted(opt_strings)


def _get_option_full_condition(option):
    if option.conditions and option.when:
        return '(( %s )) && %s' % (' && '.join(option.conditions), option.when)
    if option.conditions:
        return '(( %s ))' % (' && '.join(option.conditions))
    if option.when:
        return '%s' % option.when

    return ''


def _generate_option_strings_completion(ctxt, options):
    r = []

    grouped_by_condition = algo.group_by(options, _get_option_full_condition)
    for condition, opts in grouped_by_condition.items():
        s = 'opts+=(%s)' % _make_option_strings(ctxt, [o.option for o in opts])
        if condition:
            s = '%s && %s' % (condition, s)
        r.append(s)

    return '\n'.join(r)


def _generate_final_check_with_options(ctxt, final_conditions, options):
    option_strings_completion = _generate_option_strings_completion(ctxt, options)

    if not final_conditions:
        return option_strings_completion

    r  = 'if (( %s )); then\n' % ' && '.join(final_conditions)
    r += '%s\n' % indent(option_strings_completion, 2)
    r += 'fi'
    return r


def generate(generator):
    '''Generate option strings completion code.'''

    if len(generator.options) == 0:
        return None

    ctxt = generator.ctxt
    commandline = generator.commandline
    variable_manager = generator.variable_manager
    options = []
    final_conditions = []

    for final_option in commandline.get_final_options():
        final_conditions += ["! ${#%s[@]}" % variable_manager.capture_variable(final_option)]

    for option in commandline.options:
        if option.hidden:
            continue

        conditions = []

        for exclusive_option in option.get_conflicting_options():
            conditions += ["! ${#%s[@]}" % variable_manager.capture_variable(exclusive_option)]

        if not option.repeatable:
            conditions += ["! ${#%s[@]}" % variable_manager.capture_variable(option)]

        for final_condition in final_conditions:
            try:
                conditions.remove(final_condition)
            except ValueError:
                pass

        conditions = algo.uniq(sorted(conditions))

        when = None
        if option.when is not None:
            when = bash_when.generate_when_conditions(commandline, variable_manager, option.when)

        options.append(_Option(option, conditions, when))

    r  = 'if (( ! END_OF_OPTIONS )) && [[ "$cur" = -* ]]; then\n'
    r += '  local -a opts\n'
    r += '%s\n' % indent(_generate_final_check_with_options(ctxt, final_conditions, options), 2)
    r += '  COMPREPLY+=($(compgen -W "${opts[*]}" -- "$cur"))\n'
    r += '  [[ ${COMPREPLY-} == *= ]] && compopt -o nospace\n'
    r += '  return 1\n'
    r += 'fi'

    return r
