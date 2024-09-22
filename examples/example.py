#!/usr/bin/python3

import argparse

from crazy_complete import argparse_mod

argp = argparse.ArgumentParser(prog='example', description='Example program')

argp.add_argument('--version', action='version')

subp = argp.add_subparsers(description='commands')

cmdp = subp.add_parser('start',       help='Start a process').aliases(['launch'])
cmdp.add_argument('command',          help='Specify a command that shall be run').complete('command')
cmdp.add_argument('--change-dir',     help='Change to directory').complete('directory')
cmdp.add_argument('--mode', '-m',     help='Specify mode', choices=['auto', 'manual', 'debug'])

cmdp = subp.add_parser('stop',        help='Stop a process').aliases(['kill'])
cmdp.add_argument('--force', '-f',    help='Force stopping the process', action='store_true')
