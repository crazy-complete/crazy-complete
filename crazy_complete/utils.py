'''This module contains utility functions.'''

import sys
from collections import namedtuple
from .type_utils import is_list_type


def warn(*a):
    '''Print a warning.'''

    print('WARNING:', *a, file=sys.stderr)


def print_err(*a):
    '''Print to STDERR.'''

    print(*a, file=sys.stderr)


class GeneralAbbreviationGenerator:
    '''A class for generating abbreviations from a list of words.

    Attributes:
        min_abbreviated_length (int): The minimum length of an abbreviation.
        abbreviations (dict): A dictionary mapping each word to its list of abbreviations.
        min_lengths (dict): A dictionary mapping each word to its minimum abbreviation length.
    '''

    def __init__(self, min_abbreviated_length, words):
        '''Initialize the GeneralAbbreviationGenerator instance.

        Args:
            min_abbreviated_length (int): The minimum length of an abbreviation.
            words (iterable of str): The list of words from which to generate abbreviations.
        '''
        assert isinstance(min_abbreviated_length, int), \
            "GeneralAbbreviationGenerator: min_abbreviated_length: expected int, got %r" % min_abbreviated_length

        assert is_list_type(words), \
            "GeneralAbbreviationGenerator: words: expected iterable, got %r" % words

        self.min_abbreviated_length = min_abbreviated_length
        self.abbreviations = {}
        self.min_lengths = {}

        for word in words:
            self.abbreviations[word] = []
            self.min_lengths[word] = len(word)

            for length in range(len(word), self.min_abbreviated_length - 1, -1):
                abbrev = word[0:length]

                can_abbreviate = True
                for other_word in filter(lambda w: w != word, words):
                    if other_word.startswith(abbrev):
                        can_abbreviate = False
                        break

                if can_abbreviate or abbrev == word:
                    self.abbreviations[word].append(abbrev)
                    self.min_lengths[word] = length

    def get_abbreviations(self, word):
        '''Get the list of abbreviations for a given word.

        Args:
            word (str): The word for which to retrieve abbreviations.

        Returns:
            list: A list of abbreviations for the given word.
        '''

        assert isinstance(word, str), \
            "GeneralAbbreviationGenerator.get_abbreviations: word: expected str, got %r" % word

        return self.abbreviations[word]

    def get_many_abbreviations(self, words):
        '''Get the list of abbreviations for multiple words.

        Args:
            words (iterable of str): The words for which to retrieve abbreviations.

        Returns:
            list: A list of abbreviations for the given words.
        '''

        assert is_list_type(words), \
            "GeneralAbbreviationGenerator.get_many_abbreviations: words: expected iterable, got %r" % words

        r = []
        for word in words:
            r.extend(self.get_abbreviations(word))
        return r


class OptionAbbreviationGenerator(GeneralAbbreviationGenerator):
    '''AbbreviationGenerator for abbreviating long and old-style options.'''

    def __init__(self, words):
        assert is_list_type(words), \
            "OptionAbbreviationGenerator.get_many_abbreviations: words: expected iterable, got %r" % words

        words = list(words)

        for word in words:
            if word.startswith('--') and len(word) > 3:
                pass
            elif word.startswith('-') and len(word) > 2:
                pass
            else:
                raise ValueError('Not a long or old-style option: %r' % word)

        super().__init__(3, words)


class CommandAbbreviationGenerator(GeneralAbbreviationGenerator):
    '''AbbreviationGenerator for abbreviating commands.'''

    def __init__(self, words):
        super().__init__(1, words)


class DummyAbbreviationGenerator:
    '''A dummy abbreviation generator that returns the original word as the abbreviation.

    This class is used as a placeholder when abbreviation generation is not required.
    '''

    def __init__(self):
        pass

    def get_abbreviations(self, word):
        '''Don't abbreviate, just return the input.'''

        assert isinstance(word, str), \
            "DummyAbbreviationGenerator.get_abbreviations: word: expected str, got %r" % word

        return [word]

    def get_many_abbreviations(self, words):
        '''Don't abbreviate, just return the input.'''

        assert is_list_type(words), \
            "DummyAbbreviationGenerator.get_many_abbreviations: words: expected iterable, got %r" % words

        return words


def get_option_abbreviator(commandline):
    '''Return an OptionAbbreviationGenerator for options in `commandline`.'''

    if not commandline.abbreviate_options:
        return DummyAbbreviationGenerator()

    options = commandline.get_options(with_parent_options=commandline.inherit_options)
    option_strings = []

    for option in options:
        option_strings.extend(option.get_long_option_strings())
        option_strings.extend(option.get_old_option_strings())

    return OptionAbbreviationGenerator(option_strings)


def get_all_command_variations(commandline):
    '''Return all possible names for this command.

    If `commandline.abbreviate_commands` is True, also return abbreviated forms.
    '''

    if commandline.parent is None:
        return [commandline.prog] + commandline.aliases

    if commandline.abbreviate_commands:
        all_commands = []
        for subcommand in commandline.parent.subcommands.subcommands:
            all_commands.append(subcommand.prog)
        abbrevs = CommandAbbreviationGenerator(all_commands)
    else:
        abbrevs = DummyAbbreviationGenerator()

    return abbrevs.get_abbreviations(commandline.prog) + commandline.aliases


def get_defined_option_types(commandline):
    '''Return a tuple of defined option types.'''

    short_required = False
    short_optional = False
    short_flag     = False
    long_required  = False
    long_optional  = False
    long_flag      = False
    old_required   = False
    old_optional   = False
    old_flag       = False
    positionals    = False

    for cmdline in commandline.get_all_commandlines():
        if len(cmdline.get_positionals()) > 0:
            positionals = True

        if cmdline.get_subcommands() and len(cmdline.get_subcommands().subcommands) > 0:
            positionals = True

        for option in cmdline.options:
            if option.get_long_option_strings():
                if option.complete and option.optional_arg is True:
                    long_optional = True
                elif option.complete:
                    long_required = True
                else:
                    long_flag = True

            if option.get_old_option_strings():
                if option.complete and option.optional_arg is True:
                    old_optional = True
                elif option.complete:
                    old_required = True
                else:
                    old_flag = True

            if option.get_short_option_strings():
                if option.complete and option.optional_arg is True:
                    short_optional = True
                elif option.complete:
                    short_required = True
                else:
                    short_flag = True

    return namedtuple('Types', (
        'positionals',
        'short_required', 'short_optional', 'short_flag', 'short',
        'long_required',  'long_optional',  'long_flag',  'long',
        'old_required',   'old_optional',   'old_flag',   'old'))(
        positionals,
        short_required,    short_optional,   short_flag,
        short_required or  short_optional or short_flag,
        long_required,     long_optional,    long_flag,
        long_required  or  long_optional  or long_flag,
        old_required,      old_optional,     old_flag,
        old_required   or  old_optional   or old_flag)


def get_query_option_strings(commandline, with_parent_options=True):
    '''Return a string that can be used by {fish,zsh}_query functions.

    Returns something like:
        "-f,--flag,-a=,--argument=,-o=?,--optional=?"
    '''

    r = []

    for option in commandline.get_options(with_parent_options=with_parent_options):
        if option.complete and option.optional_arg is True:
            r.extend('%s=?' % s for s in option.option_strings)
        elif option.complete:
            r.extend('%s=' % s for s in option.option_strings)
        else:
            r.extend(option.option_strings)

    return ','.join(r)


def is_worth_a_function(commandline):
    '''Check if a commandline "is worth a function".

    This means that a commandline has on of:
        - Subcommands
        - Positionals (that have meaningful completion)
        - Options (that aren't --help or --version)
    '''

    if commandline.get_subcommands():
        return True

    for positional in commandline.get_positionals():
        if positional.complete[0] not in ('none', 'integer', 'float'):
            return True

    options = commandline.get_options()
    options = list(filter(lambda o: '--help' not in o.option_strings and
                                    '--version' not in o.option_strings, options))
    if len(options) > 0:
        return True

    return False


def key_value_list_normalize_values(values):
    '''Normalize the `values` parameter of `key_value_list`.'''

    if is_list_type(values):
        return values

    return [[key, None, func] for key, func in values.items()]
