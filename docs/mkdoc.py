#!/usr/bin/python3

import os
import yaml
from collections import defaultdict

os.chdir(os.path.dirname(os.path.abspath(__file__)))

COMMANDS_INFILE = 'commands.yaml'
COMMANDS_OUTFILE = 'commands.md'
DOCUMENTATION_INFILE = 'documentation.md.in'
DOCUMENTATION_OUTFILE = 'documentation.md'
COMMANDS = []
BY_CATEGORY = defaultdict(list)

def escape_underscore(s):
    return s.replace('_', '\\_')

class Command:
    def __init__(self, dictionary):
        self.command = None
        self.category = None
        self.short = None
        self.long = None
        self.notes = []
        self.definition = None
        self.output = None
        self.also = None
        self.implemented = None

        for key, value in dictionary.items():
            if key == 'command':
                assert isinstance(value, str), key
                self.command = value
            elif key == 'short':
                assert isinstance(value, str), key
                self.short = value
            elif key == 'long':
                assert isinstance(value, str), key
                self.long = value
            elif key == 'definition':
                assert isinstance(value, str), key
                self.definition = value
            elif key == 'category':
                assert isinstance(value, str), key
                self.category = value
            elif key == 'output':
                assert isinstance(value, str), key
                self.output = value
            elif key == 'notes':
                assert isinstance(value, list), key
                self.notes = value
            elif key == 'also':
                assert isinstance(value, dict), key
                self.also = value
            elif key == 'implemented':
                assert isinstance(value, list), key
                self.implemented = value
            else:
                raise Exception(f"Unknown key: {key}")

        if self.command is None:
            raise Exception("No command")

        if self.category is None:
            raise Exception(f"No category: {self.command}")

        if self.category not in ('meta', 'custom', 'basic', 'bonus'):
            raise Exception(f"No such category: {self.category}")

        if self.short is None:
            raise Exception(f"No short: {self.command}")

        if self.short.endswith('.'):
            raise Exception(f"short ends with '.': {self.command}")

        if self.definition is None:
            raise Exception(f"No definition: {self.command}")

        if self.output is None:
            raise Exception(f"No output: {self.command}")

        if '<TAB>' not in self.output:
            raise Exception(f"No <TAB> in output: {self.command}")

        if self.implemented:
            for implemented in self.implemented:
                if not implemented in ('Bash', 'Fish', 'Zsh'):
                    raise Exception(f"Implemented: Wrong shell {implemented}")

def make_markup_table(header, rows):
    # Ensure everything is string
    header = [str(h) for h in header]
    rows = [[str(c) for c in row] for row in rows]

    # Determine column widths (max of header + rows)
    num_cols = len(header)
    col_widths = [
        max(len(header[i]), max((len(row[i]) for row in rows), default=0))
        for i in range(num_cols)
    ]

    # Helper to format a row
    def fmt_row(row):
        return "| " + " | ".join(
            row[i].ljust(col_widths[i]) for i in range(num_cols)
        ) + " |"

    # Header separator
    separator = "| " + " | ".join("-" * col_widths[i] for i in range(num_cols)) + " |"

    # Build table
    table_lines = [fmt_row(header), separator]
    for row in rows:
        table_lines.append(fmt_row(row))

    return "\n".join(table_lines)

def make_english_listing(words):
    if len(words) == 1:
        return words[0]
    elif len(words) == 2:
        return f'{words[0]} and {words[1]}'
    elif len(words) == 3:
        return f'{words[0]}, {words[1]} and {words[2]}'

    raise AssertionError("Not reached")

def make_implemented_sentence(shells):
    shells_formatted = [f'**{w}**' for w in sorted(shells)]
    r = f'This completer is currently only implemented in {make_english_listing(shells_formatted)}.'
    return r

def make_markup_link(text, link):
    return f'[{escape_underscore(text)}](#{link})'

def make_markup_summary_table(header, commands, pre_text=None):
    r = [f'### {escape_underscore(header)}']

    if pre_text:
        r += [pre_text]

    header = ['Command', 'Description']
    rows = []
    for c in commands:
        rows.append([make_markup_link(c.command, c.command), escape_underscore(c.short)])

    r += [make_markup_table(header, rows)]

    return '\n\n'.join(r)

def make_markup_command(command):
    r =  [f'### {escape_underscore(command.command)}']
    r += [f'> {command.short}']
    if command.long:
        r += [command.long]

    notes = list(command.notes)
    if command.implemented:
        notes += [make_implemented_sentence(command.implemented)]

    if notes:
        r += ['**NOTES**']
        r += [f'- {l}' for l in notes]

    r += [f'```yaml\n{command.definition.strip()}\n```']
    if command.output:
        r += [f'```\n{command.output.strip()}\n```']
    if command.also:
        r += ['**SEE ALSO**']
        r += [f'- {make_markup_link(cmd, cmd)}: {desc}' for cmd, desc in command.also.items()]

    return '\n\n'.join(r)

def make_markup(by_category):
    r = []
    r = []
    r += [make_markup_summary_table('Meta commands', BY_CATEGORY['meta'])]
    r += [make_markup_summary_table('Built-in commands', BY_CATEGORY['basic'])]
    r += [make_markup_summary_table('User-defined commands', BY_CATEGORY['custom'])]
    r += [make_markup_summary_table('Bonus commands', BY_CATEGORY['bonus'])]

    for commands in by_category.values():
        for command in commands:
            r += [make_markup_command(command)]

    return '\n\n'.join(r)

with open(COMMANDS_INFILE, 'r', encoding='utf-8') as fh:
    for command_def in yaml.safe_load_all(fh):
        COMMANDS.append(Command(command_def))

COMMANDS = sorted(COMMANDS, key=lambda c: c.command)

for command in COMMANDS:
    BY_CATEGORY[command.category].append(command)

commands_markup = make_markup(BY_CATEGORY)

with open(COMMANDS_OUTFILE, 'w', encoding='utf-8') as fh:
    fh.write(commands_markup)

with open(DOCUMENTATION_INFILE, 'r', encoding='utf-8') as fh:
    content = fh.read()

content = content.replace('%COMMANDS%', commands_markup)

with open(DOCUMENTATION_OUTFILE, 'w', encoding='utf-8') as fh:
    fh.write(content)
