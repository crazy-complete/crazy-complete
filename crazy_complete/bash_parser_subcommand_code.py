'''Code for creating the subcommand call code in Bash'''

from . import utils

def get_subcommand_path(commandline):
    commandlines = commandline.get_parents(include_self=True)[1:]
    prognames = ['root'] + [c.prog for c in commandlines]
    return ':'.join(prognames)

def make_subcommand_call_code(commandline):
    assert commandline.parent is None, \
        "This function should only be used on top-level command lines"

    code = []

    for cmdline in commandline.get_all_commandlines():
        if cmdline.get_subcommands_option():
            positional_num = cmdline.get_subcommands_option().get_positional_num()

            r = 'if [[ "$cmd" == "%s" ]] &&'            % get_subcommand_path(cmdline)
            r += ' (( POSITIONAL_NUM == %d )); then\n'  % positional_num
            r += '  case "$arg" in\n'
            for subcommand in cmdline.get_subcommands_option().subcommands:
                commands = utils.get_all_command_variations(subcommand)
                commands.remove(subcommand.prog)
                if commands:
                    r += '    %s) cmd+=":%s";;\n' % ('|'.join(commands), subcommand.prog)
            r += '    *) cmd+=":$arg";;\n'
            r += '  esac\n'
            r += 'fi'
            code.append(r)

    return '\n\n'.join(code)
