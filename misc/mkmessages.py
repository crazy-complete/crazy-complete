#!/usr/bin/python3

import re
import os
import yaml

INFILE = 'messages.in.py'
OUTFILE = '../crazy_complete/messages.py'
TRANSLATIONS_INFILE = 'translations.yaml'

os.chdir(os.path.dirname(os.path.abspath(__file__)))


def get_fstring(translation, params):
    if not params:
        return f"'{translation}'"

    return f"f'{translation}'"


def make_function(args):
    msgid = args.pop('msgid')
    params = ', '.join(args.pop('parameters'))
    en = args.pop('en')

    r = f'def {msgid}({params}):\n'
    for lang, translation in args.items():
        r += f"    if LANG == '{lang}':\n"
        r += f"        return {get_fstring(translation, params)}\n"
    r += f"    return {get_fstring(en, params)}"
    return r


def make_functions():
    with open(TRANSLATIONS_INFILE, 'r', encoding='UTF-8') as fh:
        all_definitions = list(yaml.safe_load_all(fh))

    by_lang = {}

    for definition in all_definitions:
        by_lang[definition.pop('lang')] = definition

    specification = by_lang.pop('spec')

    for lang, defintions in by_lang.items():
        for key, translation in defintions.items():
            if not key in specification:
                raise Exception(f'{lang}: Invalid key: {key}')

    functions = []

    for msgid in sorted(specification.keys()):
        args = {'msgid': msgid, 'parameters': specification[msgid]}

        for lang, defintion in by_lang.items():
            try:
                args[lang] = defintion[msgid]
            except KeyError:
                raise Exception(f'{lang}: Missing translation: {msgid}')

        functions.append(make_function(args))

    return '\n\n\n'.join(functions)


with open(INFILE, 'r', encoding='UTF-8') as fh:
    content = fh.read()

with open(OUTFILE, 'w', encoding='UTF-8') as fh:
    fh.write(content)
    fh.write('\n')
    fh.write(make_functions())
    fh.write('\n')
