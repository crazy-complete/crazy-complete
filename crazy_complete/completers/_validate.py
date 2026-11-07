# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2025-2026 Benjamin Abendroth <braph93@gmx.de>

'''Shared validators used by more than one completer.'''

from ..errors import CrazySchemaValidationError
from ..pattern import bash_glob_to_regex, bash_glob_to_zsh_glob
from ..scheme_validator import (
    check_char, check_dictionary, check_non_empty_dict,
    check_non_empty_list, check_non_empty_string,
    check_no_spaces, check_type, has_set)

_error = CrazySchemaValidationError


def check_filedir(_ctxt, arguments, with_file_opts=False, with_list_opts=False):
    options = arguments.get_optional_arg({})
    check_type(options, (dict,), 'options')
    arguments.require_no_more()

    spec = {'directory': (False, (str,), check_non_empty_string)}

    if with_file_opts:
        spec['extensions'] = (False, (list,), check_non_empty_list)
        spec['fuzzy'] = (False, (bool,), None)
        spec['ignore_globs'] = (False, (list,), check_non_empty_list)

    if with_list_opts:
        spec['separator'] = (False, (str,), check_char)
        spec['duplicates'] = (False, (bool,), None)

    check_dictionary(options, spec)

    if has_set(options, 'extensions'):
        for i, extension in enumerate(options.value['extensions'].value):
            check_type(extension, (str,), f'extensions[{i}]')
            check_non_empty_string(extension, f'extensions[{i}]')
            check_no_spaces(extension, f'extensions[{i}]')

    if has_set(options, 'ignore_globs'):
        for pattern in options.value['ignore_globs'].value:
            check_type(pattern, (str,), 'pattern')
            check_non_empty_string(pattern, 'pattern')
            try:
                bash_glob_to_regex(pattern.value)
                bash_glob_to_zsh_glob(pattern.value)
            except ValueError as e:
                raise _error('%s: %s' % ('pattern', e), pattern) from e


def check_exec(_ctxt, arguments):
    command = arguments.get_required_arg("command")
    check_type(command, (str,), "command")
    arguments.require_no_more()


def _check_integer_float(_ctxt, arguments, types):
    options = arguments.get_optional_arg({})
    arguments.require_no_more()
    check_type(options, (dict,), "options")

    check_dictionary(options, {
        'min':      (False, types, None),
        'max':      (False, types, None),
        'help':     (False, (str,), check_non_empty_string),
        'suffixes': (False, (dict,), check_non_empty_dict),
    })

    if has_set(options, 'min') and has_set(options, 'max'):
        min_ = options.value['min'].value
        max_ = options.value['max'].value

        if min_ > max_:
            raise _error(f'min > max ({min_} > {max_})', options)

    if has_set(options, 'suffixes'):
        for suffix, description in options.value['suffixes'].value.items():
            check_type(suffix, (str,), "suffix")
            check_type(description, (str,), "description")
            check_non_empty_string(suffix, "suffix")
            check_non_empty_string(description, "description")


def check_integer(ctxt, arguments):
    _check_integer_float(ctxt, arguments, (int,))


def check_float(ctxt, arguments):
    _check_integer_float(ctxt, arguments, (int, float))
