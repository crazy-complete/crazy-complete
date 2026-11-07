# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2025-2026 Benjamin Abendroth <braph93@gmx.de>

'''This package contains completer plugins.

Each completer lives in its own file (`completers/<name>.py`) providing
the function `validate()` and one function per supported shell (`bash()`,
`fish()`, and/or `zsh()`).

Use `load(name)` to load a completer on demand.
'''

import re

import importlib

from pathlib import Path


_NAME_PATTERN = re.compile(r'^[A-Za-z_][A-Za-z0-9_]*$')


def load(name):
    '''Load the completer plugin `completers/<name>.py`.

    Raises:
        ModuleNotFoundError: If there is no completer with `name`
            or `name` is not a valid module name.
    '''

    if not _NAME_PATTERN.match(name):
        raise ModuleNotFoundError(f'Not a valid completer name: {name}')

    return importlib.import_module(f'.{name}', __name__)


def load_all():
    '''Load all completer plugins.

    Returns:
        dict[str, module]: A mapping of completer names to their modules.
    '''

    modules = {}
    for path in sorted(Path(__file__).parent.glob('*.py')):
        name = path.stem
        if name.startswith('_'):
            continue
        modules[name] = load(name)

    return modules
