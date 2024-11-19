#!/usr/bin/env python3

import re
import sys

import crazy_complete

FPM_HELP_FILE = 'fpm.help.txt'

INPUT_TYPES = ['apk', 'cpan', 'deb', 'dir', 'empty', 'freebsd', 'gem',
               'npm', 'osxpkg', 'p5p', 'pacman', 'pear', 'pkgin', 'pleaserun',
               'puppet', 'python', 'rpm', 'sh', 'snap', 'solaris', 'tar',
               'virtualenv', 'zip']

OUTPUT_TYPES = ['apk', 'cpan', 'deb', 'dir', 'empty', 'freebsd', 'gem',
               'npm', 'osxpkg', 'p5p', 'pacman', 'pear', 'pkgin', 'pleaserun',
               'puppet', 'python', 'rpm', 'sh', 'snap', 'solaris', 'tar',
               'virtualenv', 'zip']

COMPLETE = {
    '-t': {"complete": ['choices', OUTPUT_TYPES]},

    '-s': {"complete": ['choices', INPUT_TYPES]},

    '-C': {"complete": ['directory']},

    '--log': {"complete": ['choices', ['error', 'warn', 'info', 'debug']]},

    '--exclude-file': {"complete": ['file']},

    '--inputs': {"complete": ['file']},

    '--post-install':   {"complete": ['file']},
    '--pre-install':    {"complete": ['file']},
    '--post-uninstall': {"complete": ['file']},
    '--pre-uninstall':  {"complete": ['file']},
    '--after-install':  {"complete": ['file']},
    '--before-install': {"complete": ['file']},
    '--after-remove':   {"complete": ['file']},
    '--before-remove':  {"complete": ['file']},
    '--after-upgrade':  {"complete": ['file']},
    '--before-upgrade': {"complete": ['file']},

    '--workdir': {"complete": ['directory']},

    '--fpm-options-file': {"complete": ['file']},

    '--cpan-perl-bin':   {"complete": ["command"]},
    '--cpan-cpanm-bin':  {"complete": ["command"]},

    '--deb-custom-control':     {"complete": ['file']},
    '--deb-config':             {"complete": ['file']},
    '--deb-templates':          {"complete": ['file']},
    '--deb-changelog':          {"complete": ['file']},
    '--deb-upstream-changelog': {"complete": ['file']},
    '--deb-meta-file':          {"complete": ['file']},
    '--deb-init':               {"complete": ['file']},
    '--deb-default':            {"complete": ['file']},
    '--deb-upstart':            {"complete": ['file']},
    '--deb-systemd':            {"complete": ['file']},
    '--deb-after-purge':        {"complete": ['file']},
    '--deb-compression':        {"complete": ['choices', ['gz','bzip2','xz','none']]},
    '--deb-user':               {"complete": ['user']},
    '--deb-group':              {"complete": ['group']},

    '--npm-bin': {"complete": ["command"]},

    '--rpm-changelog':          {"complete": ['file']},
    '--rpm-init':               {"complete": ['file']},
    '--rpm-verifyscript':       {"complete": ['file']},
    '--rpm-pretrans':           {"complete": ['file']},
    '--rpm-posttrans':          {"complete": ['file']},
    '--rpm-digest': {"complete": ['choices', ['md5','sha1','sha256','sha384','sha512']]},
    '--rpm-compression-level':  {"complete": ['range', 0, 9]}, # TODO?
    '--rpm-compression':        {"complete": ['choices', ['none','xz','xzmt','gzip','bzip2']]},
    '--rpm-user':  {"complete": ['user']},
    '--rpm-group': {"complete": ['group']},

    '--python-bin':                 {'complete': ['command']},
    '--python-easyinstall':         {'complete': ['command']},
    '--python-pip':                 {'complete': ['command']},
    '--python-scripts-executable':  {'complete': ['command']},

    '--osxpkg-postinstall-action': {'complete': ['choices', ['logout', 'restart', 'shutdown']]},

    '--solaris-user':  {"complete": ['user']},
    '--solaris-group': {"complete": ['group']},

    '--snap-yaml': {'complete': ['file']},

    '--pacman-compression': {"complete": ['choices', ['gz','bzip2','xz','zstd','none']]},
    '--pacman-user':  {"complete": ['user']},
    '--pacman-group': {"complete": ['group']},

    '--pleaserun-chdir': {'complete': ['directory']},
}

COMMANDLINE = crazy_complete.cli.CommandLine('fpm', help="Effing package management")

COMMANDLINE.add_positional(1, complete=['file'], repeatable=True)

def find_complete_by_opts(opts):
    for opt in opts:
        if opt in COMPLETE:
            return COMPLETE.pop(opt)
    return None

def process(line):
    line = line.strip()
    if not line:
        return

    words = line.split(' ')
    opts = []
    metavar = None
    when = None
    repeatable = crazy_complete.cli.ExtendedBool.INHERIT
    complete = None

    while words[0].startswith('-'):
        opts.append(words[0].replace(',', ''))
        del words[0]

    if words[0].isupper():
        metavar = words[0]
        del words[0]

    description = ' '.join(words).strip()

    m = re.match(r'\((\w+) only\)', description)
    if m:
        when = m[1]
        description = re.sub(r'\((\w+) only\) ', '', description)

    if 'multiple times' in description:
        repeatable = True

    compl = find_complete_by_opts(opts)
    if compl:
        complete = compl['complete']
    elif metavar:
        complete = ["none"]

    if '[no-]' not in opts[0]:
        add_option(opts, metavar, description, complete, when, repeatable)
    else:
        opts_without_no = [opts[0].replace('[no-]', '')]
        opts_with_no = [opts[0].replace('[no-]', 'no-')]
        add_option(opts_without_no, metavar, description, complete, when, repeatable)
        add_option(opts_with_no, metavar, description, complete, when, repeatable)

def add_option(opts, metavar, description, complete, when, repeatable):
    if when:
        when = 'option_is -t --output-type -s --input-type -- %s' % when

    COMMANDLINE.add_option(opts,
                           metavar=metavar,
                           help=description,
                           complete=complete,
                           when=when,
                           repeatable=repeatable)

# =============================================================================
# Main
# =============================================================================

with open(FPM_HELP_FILE, 'r') as fh:
    help_text = fh.read()
lines = help_text.split('\n')

have_options = False
for line in lines:
    if line == 'Options:':
        have_options = True
    elif have_options:
        process(line)

print(crazy_complete.yaml_source.commandline_to_yaml(COMMANDLINE))

if len(COMPLETE):
    print("Warning, not everything in COMPLETE has been consumed:", file=sys.stderr)
    print(list(COMPLETE.keys()), file=sys.stderr)

