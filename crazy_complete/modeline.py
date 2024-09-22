#!/usr/bin/python3

def get_vim_modeline(filetype):
    return '# vim: ft=%s ts=2 sts=2 sw=2 et' % filetype
