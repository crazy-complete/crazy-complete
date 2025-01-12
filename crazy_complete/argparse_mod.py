"""
This module extends Python's built-in argparse library by adding several
custom methods.
"""

import argparse

from .cli import ExtendedBool

# We have to use implementation details of the argparse module...
# pylint: disable=protected-access

def _action_complete(self, command, *args):
    setattr(self, '_complete', (command, *args))
    return self


def _action_get_complete(self):
    return getattr(self, '_complete', None)


def _action_when(self, when):
    setattr(self, '_when', when)
    return self


def _action_get_when(self):
    return getattr(self, '_when', None)


def _action_set_repeatable(self, enable=True):
    setattr(self, '_repeatable', enable)
    return self


def _action_get_repeatable(self):
    return getattr(self, '_repeatable', ExtendedBool.INHERIT)


def _action_set_final(self, enable=True):
    setattr(self, '_final', enable)
    return self


def _action_get_final(self):
    return getattr(self, '_final', False)


def _parser_alias(self, alias):
    setattr(self, '_aliases', [alias])
    return self


def _parser_aliases(self, aliases):
    setattr(self, '_aliases', list(aliases))
    return self


def _parser_get_aliases(self):
    return getattr(self, '_aliases', [])


def _parser_remove_help(self):
    self._actions.pop(0)
    self._option_string_actions.pop('-h')
    self._option_string_actions.pop('--help')


argparse.Action.complete = _action_complete
argparse.Action.get_complete = _action_get_complete
argparse.Action.when = _action_when
argparse.Action.get_when = _action_get_when
argparse.Action.set_repeatable = _action_set_repeatable
argparse.Action.get_repeatable = _action_get_repeatable
argparse.Action.set_final = _action_set_final
argparse.Action.get_final = _action_get_final
argparse.ArgumentParser.alias = _parser_alias
argparse.ArgumentParser.aliases = _parser_aliases
argparse.ArgumentParser.get_aliases = _parser_get_aliases
argparse.ArgumentParser.remove_help = _parser_remove_help
