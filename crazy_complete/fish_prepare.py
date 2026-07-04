# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2025-2026 Benjamin Abendroth <braph93@gmx.de>

'''Code for generating the "prepare" function.'''

import re

from . import algo
from . import utils
from . import shell
from . import helpers


def _get_positional_pattern(commandline):
    '''Return a regex matching the command's positional path.

    Example output:
        '(command|alias)>(subcommand)'
    '''

    commandlines = commandline.get_parents(include_self=True)
    del commandlines[0]

    r = algo.SparseList([], default='.*')

    for cmdline in commandlines:
        cmds = utils.get_all_command_variations(cmdline)
        index = cmdline.parent.get_subcommands().get_positional_index()
        r[index] = f'({"|".join(re.escape(cmd) for cmd in cmds)})'

    return '>'.join(r)


def _get_cmdline_definitions(commandline):
    '''Return a list of command line definitions.

    Example output:
        [ '=>--help --version', '(command)=>--option=' ]
    '''

    r = []

    for cmdline in commandline.get_all_commandlines():
        query_options = utils.get_query_option_strings(cmdline, False)
        if not query_options:
            continue

        positional_pattern = _get_positional_pattern(cmdline)
        r.append(f"{positional_pattern}=>{query_options}")

    return r


def _get_capture_code(commandline, ctxt):
    '''Return code for capturing options.

    Example output:
        '_my_program__capture_option MY_VARIABLE -o --option'
    '''

    r = []

    for cmdline in commandline.get_all_commandlines():
        for option in cmdline.get_options():
            if option.capture is not None:
                capture_func = ctxt.helpers.use_function('capture_option')
                opts = ' '.join(option.option_strings)
                r.append(f'{capture_func} {option.capture} {opts}')

    return '\n'.join(r)


def get_prepare_function(commandline, ctxt):
    '''Generate the prepare function.

    The prepare function:
        - Calls the `query_init` function
        - Captures arguments of options

    Returns the function name of the generated function.
    '''

    query_init = ctxt.helpers.use_function('query_init')
    definitions = _get_cmdline_definitions(commandline)

    code = f'{query_init}'
    if definitions:
        code += ' \\\n  %s' % (' \\\n  '.join(shell.quote(d) for d in definitions))

    capture_code = _get_capture_code(commandline, ctxt)
    if capture_code:
        code += f'\n{capture_code}'

    code += '\nreturn 0'

    func = helpers.FishFunction('prepare', code)
    ctxt.helpers.add_function(func)
    return ctxt.helpers.use_function('prepare')
