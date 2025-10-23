'''Version-dependent Bash code.'''


def filedir(ctxt):
    if ctxt.config.bash_completions_version >= (2, 12):
        return '_comp_compgen_filedir'
    
    return '_filedir'


def init_completion(ctxt):
    if ctxt.config.bash_completions_version >= (2, 12):
        return '_comp_initialize'
    
    return '_init_completion'


def completion_loader(ctxt):
    if ctxt.config.bash_completions_version >= (2, 12):
        return '_comp_complete_load'
    
    return '_completion_loader'


def pids(ctxt):
    if ctxt.config.bash_completions_version >= (2, 12):
        return '_comp_compgen_pids'
    
    return '_pids'


def pnames(ctxt):
    if ctxt.config.bash_completions_version >= (2, 12):
        return '_comp_compgen_pnames'
    
    return '_pnames'


def uids(ctxt):
    if ctxt.config.bash_completions_version >= (2, 12):
        return '_comp_compgen_uids'

    return '_uids'


def gids(ctxt):
    if ctxt.config.bash_completions_version >= (2, 12):
        return '_comp_compgen_gids'

    return '_gids'


def shells(ctxt):
    if ctxt.config.bash_completions_version >= (2, 12):
        return '_comp_compgen -a shells'

    return '_shells'


def signals(ctxt):
    if ctxt.config.bash_completions_version >= (2, 12):
        return '_comp_compgen_signals'

    return '_signals'
