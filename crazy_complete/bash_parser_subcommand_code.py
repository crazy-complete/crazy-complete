'''Code for creating the subcommand switch code in Bash'''

from collections import OrderedDict

from . import utils
from . import shell
from . import bash_patterns
from .str_utils import indent


def get_subcommand_path(commandline):
    commandlines = commandline.get_parents(include_self=True)[1:]
    prognames = ['root'] + [c.prog for c in commandlines]
    return ':'.join(prognames)


def make_subcommand_switch_code(commandline):
    '''
    Generate Bash code that tracks and updates the current subcommand path.

    This function walks through all known command lines (starting from the given
    top-level `commandline`) and generates conditional Bash code that appends
    the currently matched subcommand to the `cmd` variable. This allows the
    generated completion script to keep track of the full subcommand hierarchy
    as the user types.

    While tracking, all variations of a subcommand are considered, including
    defined aliases and any supported abbreviations. This ensures that the
    resulting `cmd` variable always contains the canonical subcommand name,
    regardless of how the user typed it.
    '''

    assert commandline.parent is None, \
        "This function should only be used on top-level command lines"

    cases = []

    for cmdline in commandline.get_all_commandlines():
        if not cmdline.get_subcommands():
            continue

        positional_num = cmdline.get_subcommands().get_positional_num()
        command_path   = get_subcommand_path(cmdline)
        switch_code    = _make_switch_case(cmdline)

        cases.append(('%s|%d' % (command_path, positional_num), switch_code))

    if not cases:
        return None

    r  = 'case "$cmd|${#POSITIONALS[@]}" in\n'
    for case in cases:
        if '\n' not in case[1]:
            r += '  %s) %s;;\n' % (shell.escape(case[0]), case[1])
        else:
            r += '  %s)\n%s;;\n' % (shell.escape(case[0]), indent(case[1], 4))
    r += 'esac'

    return r


def _make_switch_case(cmdline):
    subcommand_aliases = OrderedDict()

    for subcommand in cmdline.get_subcommands().subcommands:
        aliases = utils.get_all_command_variations(subcommand)
        aliases.remove(subcommand.prog)

        if aliases:
            subcommand_aliases[subcommand.prog] = aliases

    # We have no aliases or abbreviations, just add $arg to $cmd
    if not subcommand_aliases:
        return 'cmd+=":$arg"'

    r  = 'case "$arg" in\n'
    for command, aliases in subcommand_aliases.items():
        r += '  %s) cmd+=":%s";;\n' % (bash_patterns.make_pattern(aliases), command)
    r += '  *) cmd+=":$arg";;\n'
    r += 'esac'
    return r
