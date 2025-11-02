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


def completer_not_allowed_in(completer, completer2):
    if LANG == 'de':
        return f'Vervollständiger `{completer}` nicht in `{completer2}` erlaubt'
    return f'Completer `{completer}` not allowed in `{completer2}`'


def completer_not_allowed_in_option(completer):
    if LANG == 'de':
        return f'Vervollständiger `{completer}` nicht erlaubt in einer Option'
    return f'Completer `{completer}` not allowed inside an option'


def completer_requires_repeatable(completer):
    if LANG == 'de':
        return f'Vervollständiger `{completer}` benötigt `repeatable=True`'
    return f'Completer `{completer}` requires `repeatable=true`'


def dict_cannot_be_empty():
    if LANG == 'de':
        return 'Dictionary darf nicht leer sein'
    return 'Dictionary cannot be empty'


def integer_cannot_be_zero():
    if LANG == 'de':
        return 'Ganzzahl darf nicht Null sein'
    return 'Integer cannot be zero'


def integer_must_be_greater_than_zero():
    if LANG == 'de':
        return 'Ganzzahl muss größer als Null sein'
    return 'Integer must be greater than zero'


def invalid_type_expected_types(types):
    if LANG == 'de':
        return f'Ungültiger Typ. Erwartet: {types}'
    return f'Invalid type. Expected: {types}'


def invalid_value(values):
    if LANG == 'de':
        return f'Ungültiger Wert. Erwartet: {values}'
    return f'Invalid value. Expected: {values}'


def list_cannot_be_empty():
    if LANG == 'de':
        return 'Liste darf nicht leer sein'
    return 'List cannot be empty'


def list_must_contain_at_least_two_items():
    if LANG == 'de':
        return 'Liste muss mindestens zwei Elemente enthalten'
    return 'List must contain at least two items'


def missing_arg():
    if LANG == 'de':
        return 'Fehlendes benötigtes Argument'
    return 'Missing required argument'


def missing_definition_of_program(program):
    if LANG == 'de':
        return f'Fehlende Definition des Programms `{program}`'
    return f'Missing definition of program `{program}`'


def multiple_definition_of_program(program):
    if LANG == 'de':
        return f'Mehrfache Definition des Programms `{program}`'
    return f'Multiple definition of program `{program}`'


def no_programs_defined():
    if LANG == 'de':
        return 'Keine Programme definiert'
    return 'No programs defined'


def not_a_variable_name():
    if LANG == 'de':
        return 'Ungültiger Variablenname'
    return 'Not a valid variable name'


def not_an_absolute_path():
    if LANG == 'de':
        return 'Kein absoluter Pfad'
    return 'Not an absolute path'


def not_an_extended_regex():
    if LANG == 'de':
        return 'Ungültiger regulärer Ausdruck'
    return 'Not an extended regular expression'


def parameter_not_allowed_in_subcommand(parameter):
    if LANG == 'de':
        return f'Parameter `{parameter}` ist nicht erlaub einem Unterkommando'
    return f'Parameter `{parameter}` not allowed in subcommand'


def single_character_expected():
    if LANG == 'de':
        return 'Ungültige Länge. Einzelner Buchstabe erwartet'
    return 'Invalid length. Single character expected'


def string_cannot_be_empty():
    if LANG == 'de':
        return 'Zeichenkette darf nicht leer sein'
    return 'String cannot be empty'


def string_cannot_contain_space():
    if LANG == 'de':
        return 'Zeichenkette darf keine Leerzeichen enthalten'
    return 'String cannot contain spaces'


def too_many_arguments():
    if LANG == 'de':
        return 'Zu viele Argumente'
    return 'Too many arguments'


def too_many_programs_defined():
    if LANG == 'de':
        return 'Zu viele Programme definiert'
    return 'Too many programs defined'


def unknown_completer():
    if LANG == 'de':
        return 'Unbekannter Vervollständiger'
    return 'Unknown completer'


def unknown_parameter():
    if LANG == 'de':
        return 'Unbekannter Parameter'
    return 'Unknown parameter'
