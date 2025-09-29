'''Code for creating the subcommand switch code in Bash'''

from . import utils
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

    code = []

    for cmdline in commandline.get_all_commandlines():
        if cmdline.get_subcommands():
            positional_num = cmdline.get_subcommands().get_positional_num()

            r = 'if [[ "$cmd" == "%s" ]] &&'            % get_subcommand_path(cmdline)
            r += ' (( POSITIONAL_NUM == %d )); then\n'  % positional_num
            r += '%s\n' % indent(_make_switch_case(cmdline), 2)
            r += 'fi'
            code.append(r)

    return '\n\n'.join(code)

def _make_switch_case(cmdline):
    subcommand_aliases = {}

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
        r += '  %s) cmd+=":%s";;\n' % ('|'.join(aliases), command)
    r += '  *) cmd+=":$arg";;\n'
    r += 'esac'
    return r
