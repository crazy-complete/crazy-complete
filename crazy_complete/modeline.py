'''Vim modeline string.'''

def get_vim_modeline(filetype):
    '''Return a vim modeline string.'''

    return f'# vim: ft={filetype} ts=2 sts=2 sw=2 et'
