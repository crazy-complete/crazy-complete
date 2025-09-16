'''Code for creating the subcommand call code in Bash'''

def get_subcommand_path(commandline):
    commandlines = commandline.get_parents(include_self=True)[1:]
    prognames = ['root'] + [c.prog for c in commandlines]
    return ':'.join(prognames)

def make_subcommand_call_code(commandline):
    commandlines = []
    commandline.visit_commandlines(lambda o: commandlines.append(o))

    code = []

    for commandline in commandlines:
        if commandline.get_subcommands_option():
            positional_num = commandline.get_subcommands_option().get_positional_num()

            r = 'if [[ "$cmd" == "%s" ]] && (( POSITIONAL_NUM == %d )); then\n' % (get_subcommand_path(commandline), positional_num)
            r += '  case "$arg" in\n'
            for subcommand in commandline.get_subcommands_option().subcommands:
                if subcommand.aliases:
                    r += '    %s) cmd+=":%s";;\n' % ('|'.join(subcommand.aliases), subcommand.prog)
            r += '    *) cmd+=":$arg";;\n'
            r += '  esac\n'
            r += 'fi'
            code.append(r)

    return '\n\n'.join(code)
