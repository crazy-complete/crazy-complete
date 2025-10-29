'''Translations.'''

import os
import locale

# flake8: noqa: E501
# pylint: disable=line-too-long
# pylint: disable=missing-function-docstring


def normalize_lang(lang_code):
    '''Normalize locale code to short language like `de`.'''

    if not lang_code:
        return 'en'

    return lang_code.split('_')[0].split('.')[0].lower()


def get_lang():
    '''Get system language.'''

    lang = (
        os.environ.get("LANGUAGE") or
        os.environ.get("LC_ALL") or
        os.environ.get("LC_MESSAGES") or
        os.environ.get("LANG")
    )

    if not lang:
        lang, _ = locale.getdefaultlocale()

    return normalize_lang(lang)


LANG = get_lang()

