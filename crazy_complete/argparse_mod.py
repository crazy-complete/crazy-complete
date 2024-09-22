#!/usr/bin/python3

import argparse

from .commandline import *


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


def _action_set_multiple_option(self, enable=True):
    setattr(self, '_multiple_option', enable)
    return self


def _action_get_multiple_option(self):
    return getattr(self, '_multiple_option', ExtendedBool.INHERIT)


def _parser_alias(self, alias):
    setattr(self, '_aliases', [alias])
    return self


def _parser_aliases(self, aliases):
    setattr(self, '_aliases', aliases)
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
argparse.Action.set_multiple_option = _action_set_multiple_option
argparse.Action.get_multiple_option = _action_get_multiple_option
argparse.ArgumentParser.aliases = _parser_aliases
argparse.ArgumentParser.alias = _parser_alias
argparse.ArgumentParser.get_aliases = _parser_get_aliases
argparse.ArgumentParser.remove_help = _parser_remove_help
