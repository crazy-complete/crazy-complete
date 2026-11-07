# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2025-2026 Benjamin Abendroth <braph93@gmx.de>

'''Colorizer for the example definitions embedded in the completer modules.'''

import re

from . import console

_TOKEN = re.compile(
    r"(?P<string>'[^'\n]*'|\"[^\"]*\")"
    r"|(?P<word>\b[A-Za-z_][A-Za-z0-9_]*\b)"
    r"|(?P<symbol>[-:,\[\]{}])"
    r"|(?P<ws>\s+)"
    r"|(?P<other>.)"
)


def _wrap(color, text):
    return f'{color}{text}{console.RESET}'


def is_key(tokens, index):
    follow = index + 1
    while follow < len(tokens) and tokens[follow][0] == 'ws':
        follow += 1
    return follow < len(tokens) and tokens[follow][1] == ':'


def colorize(text):
    """Return ``text`` with keys, strings and syntax characters colorized."""
    tokens = [(m.lastgroup, m.group()) for m in _TOKEN.finditer(text)]
    parts = []
    for index, (kind, token) in enumerate(tokens):
        if kind == 'ws':
            parts.append(token)
        elif kind in ('word', 'string') and is_key(tokens, index):
            parts.append(_wrap(console.BOLD_CYAN, token))
        elif kind == 'string':
            parts.append(_wrap(console.BOLD_GREEN, token))
        elif kind in ('symbol', 'other'):
            parts.append(_wrap(console.BOLD_BLACK, token))
        else:
            parts.append(token)
    return ''.join(parts)


if __name__ == '__main__':
    example = """prog: 'example'
options:
  - option_strings: ['--prefix']
    complete: ['integer', {'suffixes': {'s': 'seconds', 'm': 'minutes'}}]"""
    print(colorize(example))
