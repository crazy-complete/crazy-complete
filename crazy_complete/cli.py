'''This module contains the CommandLine, Option and Positional classes.'''

from collections import OrderedDict
from types import NoneType

from .type_utils import validate_type
from .errors import CrazyError, CrazyTypeError
from .str_utils import (
    contains_space, is_valid_option_string,
    is_valid_variable_name, is_empty_or_whitespace
)

# pylint: disable=redefined-builtin
# pylint: disable=too-few-public-methods
# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-arguments
# pylint: disable=too-many-positional-arguments


class ExtendedBool:
    '''Class that holds an extended bool.'''

    TRUE    = True
    FALSE   = False
    INHERIT = 'INHERIT'


def is_extended_bool(obj):
    '''Check if `obj` an instance of `ExtendedBool`.'''

    return obj in (True, False, ExtendedBool.INHERIT)


class CommandLine:
    '''Represents a command line with options, positionals, and subcommands.'''

    def __init__(self,
                 prog,
                 parent=None,
                 help=None,
                 aliases=None,
                 wraps=None,
                 abbreviate_commands=ExtendedBool.INHERIT,
                 abbreviate_options=ExtendedBool.INHERIT,
                 inherit_options=ExtendedBool.INHERIT):
        '''Initializes a CommandLine object with the specified parameters.

        Args:
            prog (str):
                The name of the program (or subcommand).

            help (str):
                The help message for the program (or subcommand).

            parent (CommandLine or None):
                The parent command line object, if any.

            aliases (list of str or None):
                Aliases for this command.

            wraps (str or None):
                Specify the command to inherit options from.

            abbreviate_commands (ExtendedBool):
                Specifies if commands can be abbreviated.

            abbreviate_options (ExtendedBool):
                Specifies if options can be abbreviated.

            inherit_options (ExtendedBool):
                Specifies if options are visible to subcommands.
        '''
        if aliases is None:
            aliases = []

        validate_type(prog, (str,), 'prog')
        validate_type(parent, (CommandLine, NoneType), 'parent')
        validate_type(help, (str, NoneType), 'help')
        validate_type(aliases, (list,), 'aliases')
        validate_type(wraps, (str, NoneType), 'wraps')

        if wraps is not None:
            if is_empty_or_whitespace(wraps):
                raise CrazyError('wraps is empty')

            if contains_space(wraps):
                raise CrazyError('wraps: cannot contain space')

        for index, alias in enumerate(aliases):
            if not isinstance(alias, str):
                raise CrazyTypeError(f'aliases[{index}]', 'str', alias)

            if contains_space(alias):
                raise CrazyError(f'aliases[{index}]: cannot contain space')

        if not is_extended_bool(abbreviate_commands):
            raise CrazyTypeError('abbreviate_commands', 'ExtendedBool', abbreviate_commands)

        if not is_extended_bool(abbreviate_options):
            raise CrazyTypeError('abbreviate_options', 'ExtendedBool', abbreviate_options)

        if not is_extended_bool(inherit_options):
            raise CrazyTypeError('inherit_options', 'ExtendedBool', inherit_options)

        self.prog = prog
        self.parent = parent
        self.help = help
        self.aliases = aliases
        self.wraps = wraps
        self.abbreviate_commands = abbreviate_commands
        self.abbreviate_options = abbreviate_options
        self.inherit_options = inherit_options
        self.options = []
        self.positionals = []
        self.subcommands = None

    def add_option(self, option_strings, **parameters):
        '''Adds a new option to the command line.

        For a list of valid parameters, see `class Option`.

        Returns:
            Option: The newly added Option object.
        '''

        o = Option(self, option_strings, **parameters)
        self.options.append(o)
        return o

    def add_positional(self, number, **parameters):
        '''Adds a new positional argument to the command line.

        For a list of valid parameters, see `class Positional`.

        Returns:
            Positional: The newly added Positional object.
        '''

        p = Positional(self, number, **parameters)
        self.positionals.append(p)
        return p

    def add_mutually_exclusive_group(self, group):
        '''Adds a new mutually exclusive group.

        Returns:
            MutuallyExclusiveGroup: The newly created mutually exclusive group.
        '''

        return MutuallyExclusiveGroup(self, group)

    def add_subcommands(self):
        '''Adds a subcommands option to the command line.

        Returns:
            SubCommandsOption: The newly created subcommands option.

        Raises:
            CrazyError: If the command line object already has subcommands.
        '''

        if self.subcommands:
            raise CrazyError('CommandLine object already has subcommands')

        self.subcommands = SubCommandsOption(self)
        return self.subcommands

    class OptionsGetter:
        '''A class for getting options from a CommandLine object.'''

        def __init__(self, commandline, with_parent_options=False, only_with_arguments=False):
            self.options = OrderedDict()

            if with_parent_options:
                commandlines = commandline.get_parents(include_self=True)
            else:
                commandlines = [commandline]

            for cmdline in reversed(commandlines):
                for option in cmdline.options:
                    if not only_with_arguments or option.complete:
                        self._add(option, cmdline)

        def _add(self, option, commandline):
            key = option.get_option_strings_key()

            if key not in self.options:
                self.options[key] = (commandline, [])

            if self.options[key][0] == commandline:
                self.options[key][1].append(option)

        def get(self):
            '''Return the result.'''
            r = []
            for _, options in self.options.values():
                for option in options:
                    r.append(option)
            return r

    def get_options(self, with_parent_options=False, only_with_arguments=False):
        '''Gets a list of options associated with the command line.

        Args:
            with_parent_options (bool):
                If True, include options from parent command lines.

            only_with_arguments (bool):
                If True, include only options that take arguments.

        Returns:
            list: A list of Option objects
        '''

        assert isinstance(with_parent_options, bool)
        assert isinstance(only_with_arguments, bool)

        getter = CommandLine.OptionsGetter(
            self,
            with_parent_options=with_parent_options,
            only_with_arguments=only_with_arguments)

        return getter.get()

    def get_option_strings(self, with_parent_options=False, only_with_arguments=False):
        '''Gets a list of option strings associated with the command line.

        Args:
            with_parent_options (bool):
                If True, include options from parent command lines.

            only_with_arguments (bool):
                If True, include only options that take arguments.

        Returns:
            list: A list of option strings
        '''

        assert isinstance(with_parent_options, bool)
        assert isinstance(only_with_arguments, bool)

        option_strings = []

        options = self.get_options(
            with_parent_options=with_parent_options,
            only_with_arguments=only_with_arguments)

        for o in options:
            option_strings.extend(o.option_strings)

        return option_strings

    def get_final_options(self):
        '''Gets a list of all final options.'''

        r = []
        cmdline = self

        while cmdline:
            for option in cmdline.options:
                if option.final:
                    r.append(option)
            cmdline = cmdline.parent

        return r

    def get_final_option_strings(self):
        '''Gets a list of all final option strings.'''

        r = []
        for option in self.get_final_options():
            r.extend(option.option_strings)
        return r

    def get_positionals(self):
        '''Gets a list of positional arguments associated with the command line.

        Note:
            SubCommandsOption objects are not considered positional arguments
            and are not included in the list.

        Returns:
            list: A list of positional arguments
        '''

        return list(self.positionals)

    def get_subcommands(self):
        '''Gets the subcommands of the command line.

        Returns:
            SubCommandsOption or None:
                The subcommands option if it exists, otherwise None.
        '''

        return self.subcommands

    def get_parents(self, include_self=False):
        '''Gets a list of parent CommandLine objects.

        Args:
            include_self (bool):
                If True, includes the current CommandLine object in the list.

        Returns:
            list: A list of parent CommandLine objects.
        '''

        assert isinstance(include_self, bool)

        parents = []

        parent = self.parent
        while parent:
            parents.insert(0, parent)
            parent = parent.parent

        if include_self:
            parents.append(self)

        return parents

    def get_root_commandline(self):
        '''Return the root commandline.'''

        if not self.parent:
            return self

        return self.parent.get_root_commandline()

    def get_options_by_option_strings(self, option_strings):
        '''Return all options containing one option_strings.'''

        result = []

        for option_string in option_strings:
            found = False
            for option in self.options:
                if option_string in option.option_strings:
                    if option not in result:
                        result.append(option)
                    found = True
                    break
            if not found:
                raise CrazyError('Option %r not found' % option_string)

        return result

    def get_highest_positional_num(self):
        '''Get the highest positional number.'''

        highest = 0
        for positional in self.positionals:
            highest = max(highest, positional.number)
        if self.subcommands:
            highest += 1
        return highest

    def get_program_name(self):
        '''Return the program name.'''

        commandlines = self.get_parents(include_self=True)
        return commandlines[0].prog

    def get_command_path(self, progname=None):
        '''Return the full command path.'''
        prognames = [c.prog for c in self.get_parents(include_self=True)]

        if progname is not None:
            prognames[0] = progname

        return ' '.join(prognames)

    def visit_commandlines(self, callback):
        '''Apply a callback to all CommandLine objects.'''

        callback(self)
        if self.get_subcommands():
            for sub in self.get_subcommands().subcommands:
                sub.visit_commandlines(callback)

    def get_all_commandlines(self):
        '''Get a list of all defined commandlines.'''

        result = []
        self.visit_commandlines(result.append)
        return result

    def copy(self):
        '''Make a deep copy of the current CommandLine object.'''

        copy = CommandLine(
            self.prog,
            parent              = None,
            help                = self.help,
            aliases             = self.aliases,
            wraps               = self.wraps,
            abbreviate_commands = self.abbreviate_commands,
            abbreviate_options  = self.abbreviate_options,
            inherit_options     = self.inherit_options)

        for option in self.options:
            copy.add_option(
                option.option_strings,
                metavar         = option.metavar,
                help            = option.help,
                complete        = option.complete,
                nosort          = option.nosort,
                optional_arg    = option.optional_arg,
                groups          = option.groups,
                repeatable      = option.repeatable,
                final           = option.final,
                hidden          = option.hidden,
                when            = option.when,
                capture         = option.capture
            )

        for positional in self.positionals:
            copy.add_positional(
                positional.number,
                metavar         = positional.metavar,
                help            = positional.help,
                repeatable      = positional.repeatable,
                nosort          = positional.nosort,
                complete        = positional.complete,
                when            = positional.when,
                capture         = positional.capture
            )

        if self.subcommands is not None:
            subcommands_option = copy.add_subcommands()
            for subparser in self.subcommands.subcommands:
                subcommands_option.add_commandline_object(subparser.copy())

        return copy

    def __eq__(self, other):
        return (
            isinstance(other, CommandLine)                        and
            self.prog                == other.prog                and
            self.aliases             == other.aliases             and
            self.help                == other.help                and
            self.wraps               == other.wraps               and
            self.abbreviate_commands == other.abbreviate_commands and
            self.abbreviate_options  == other.abbreviate_options  and
            self.inherit_options     == other.inherit_options     and
            self.options             == other.options             and
            self.positionals         == other.positionals         and
            self.subcommands         == other.subcommands
        )

    def __repr__(self):
        r = '{'
        r += f'\nprog: {self.prog!r},'
        r += f'\naliases: {self.aliases!r},'
        r += f'\nwraps: {self.wraps!r},'
        r += f'\nhelp: {self.help!r},'
        r += f'\nabbreviate_commands: {self.abbreviate_commands!r},'
        r += f'\nabbreviate_options: {self.abbreviate_options!r},'
        r += f'\ninherit_options: {self.inherit_options!r},'
        r += f'\noptions: {self.options!r},'
        r += f'\npositionals: {self.positionals!r},'
        r += f'\nsubcommands: {self.subcommands!r},'
        r += '\n}'
        return r


class Positional:
    '''Class representing a command line positional.'''

    def __init__(
            self,
            parent,
            number,
            metavar=None,
            help=None,
            complete=None,
            nosort=False,
            repeatable=False,
            when=None,
            capture=None):
        '''Initializes a Positional object with the specified parameters.

        Args:
            parent (CommandLine):
                The parent command line object, if any.

            number (int):
                The number of the positional argument (starting from 1)

            metavar (str):
                The metavar for the positional.

            help (str):
                The help message for the positional.

            repeatable (bool):
                Specifies if positional can be specified more times

            complete (list):
                The completion specification for the positional.

            nosort (bool):
                Do not sort the completion suggestions.

            when (str):
                Specifies a condition for showing this positional.

            capture (str):
                Specifies the variable name for capturing
        '''

        validate_type(parent, (CommandLine, NoneType), 'parent')
        validate_type(number, (int,), 'number')
        validate_type(metavar, (str, NoneType), 'metavar')
        validate_type(help, (str, NoneType), 'help')
        validate_type(complete, (list, tuple, NoneType), 'complete')
        validate_type(repeatable, (bool,), 'repeatable')
        validate_type(nosort, (bool,), 'nosort')
        validate_type(when, (str, NoneType), 'when')
        validate_type(capture, (str, NoneType), 'capture')

        if capture is not None and not is_valid_variable_name(capture):
            raise CrazyError(f"Invalid variable name: {capture!r}")

        if number <= 0:
            raise CrazyError(f'number: value ({number}) is invalid, number has to be >= 1')

        self.parent = parent
        self.number = number
        self.metavar = metavar
        self.help = help
        self.repeatable = repeatable
        self.complete = complete if complete else ['none']
        self.nosort = nosort
        self.when = when
        self.capture = capture

    def get_positional_index(self):
        '''Returns the index of the current positional argument within the
        current commandline, including parent commandlines.

        Returns:
            int: The index of the positional argument.
        '''

        positional_no = self.number - 1

        for commandline in self.parent.get_parents():
            highest = 0
            for positional in commandline.get_positionals():
                highest = max(highest, positional.number)
            positional_no += highest

            if commandline.get_subcommands():
                positional_no += 1

        return positional_no

    def get_positional_num(self):
        '''Returns the number of the current positional argument within the
        current commandline, including parent commandlines.

        Note:
            This is the same as `CommandLine.get_positional_index() + 1`.

        Returns:
            int: The number of the positional argument.
        '''

        return self.get_positional_index() + 1

    def __eq__(self, other):
        return (
            isinstance(other, Positional)       and
            self.number     == other.number     and
            self.metavar    == other.metavar    and
            self.help       == other.help       and
            self.repeatable == other.repeatable and
            self.complete   == other.complete   and
            self.nosort     == other.nosort     and
            self.when       == other.when       and
            self.capture    == other.capture
        )


def is_short_option_string(string):
    '''Return True if string is a short option string.'''
    return len(string) == 2


def is_long_option_string(string):
    '''Return True if string is a long option string.'''
    return string.startswith('--')


def is_old_option_string(string):
    '''Return True if string is an old option string.'''
    return not string.startswith('--') and len(string) > 2


class Option:
    '''Class representing a command line option.'''

    # pylint: disable=too-many-locals

    def __init__(
            self,
            parent,
            option_strings,
            metavar=None,
            help=None,
            complete=None,
            nosort=False,
            groups=None,
            optional_arg=False,
            repeatable=ExtendedBool.INHERIT,
            final=False,
            hidden=False,
            when=None,
            capture=None):
        '''Initializes an Option object with the specified parameters.

        Args:
            parent (CommandLine):
                The parent command line object, if any.

            option_strings (list of str):
                The list of option strings.

            metavar (str):
                The metavar for the option.

            help (str):
                The help message for the option.

            complete (tuple):
                The completion specification for the option.

            nosort (bool):
                Do not sort the completion suggestions.

            optional_arg (bool):
                Specifies if option's argument is optional.

            groups (list of str):
                Specify to which mutually exclusive groups this option
                belongs to.

            repeatable (ExtendedBool):
                Specifies if the option can be repeated.

            final (bool):
                If True, no more options are suggested after this one.

            hidden (bool):
                Specifies if this option is hidden.

            when (str):
                Specifies a condition for showing this option.

            capture (str):
                Specifies the variable name for capturing

        Returns:
            Option: The newly added Option object.
        '''

        validate_type(parent, (CommandLine, NoneType), 'parent')
        validate_type(option_strings, (list,), 'option_strings')
        validate_type(metavar, (str, NoneType), 'metavar')
        validate_type(help, (str, NoneType), 'help')
        validate_type(complete, (list, tuple, NoneType), 'complete')
        validate_type(groups, (list, NoneType), 'groups')

        if groups is not None:
            for index, group in enumerate(groups):
                if not isinstance(group, str):
                    raise CrazyTypeError(f'groups[{index}]', 'str', group)

        validate_type(optional_arg, (bool,), 'optional_arg')

        if not is_extended_bool(repeatable):
            raise CrazyTypeError('repeatable', 'ExtendedBool', repeatable)

        validate_type(final, (bool,), 'final')
        validate_type(hidden, (bool,), 'hidden')
        validate_type(nosort, (bool,), 'nosort')
        validate_type(when, (str, NoneType), 'when')
        validate_type(capture, (str, NoneType), 'capture')

        if not option_strings:
            raise CrazyError('Empty option strings')

        for index, option_string in enumerate(option_strings):
            if not isinstance(option_string, str):
                raise CrazyTypeError(f'option_strings[{index}]', 'str', option_string)

            if not is_valid_option_string(option_string):
                raise CrazyError(f"Invalid option string: {option_string!r}")

        if capture is not None and not is_valid_variable_name(capture):
            raise CrazyError(f"Invalid variable name: {capture!r}")

        if metavar and not complete:
            raise CrazyError(f'Option {option_strings} has metavar set, but has no complete')

        if optional_arg and not complete:
            raise CrazyError(f'Option {option_strings} has optional_arg=True, but has no complete')

        if hidden is True and repeatable is True:
            raise CrazyError(f'Option {option_strings} has both hidden and repeatable set to True')

        self.parent = parent
        self.option_strings = option_strings
        self.metavar = metavar
        self.help = help
        self.complete = complete
        self.nosort = nosort
        self.groups = groups
        self.optional_arg = optional_arg
        self.repeatable = repeatable
        self.final = final
        self.hidden = hidden
        self.when = when
        self.capture = capture

    def get_option_strings(self):
        '''Returns the option strings associated with the Option object.

        Returns:
            list: A list of strings representing the option strings.
        '''

        return self.option_strings

    def get_option_strings_key(self, delimiter=' '):
        '''Returns a key with consisting of all option strings.'''

        return delimiter.join(sorted(self.option_strings))

    def get_short_option_strings(self):
        '''Returns the short option strings associated with the object.

        Returns:
            list: A list of short option strings ("-o").
        '''

        return list(filter(is_short_option_string, self.option_strings))

    def get_long_option_strings(self):
        '''Returns the long option strings associated with the object.

        Returns:
            list: A list of long option strings ("--option").
        '''

        return list(filter(is_long_option_string, self.option_strings))

    def get_old_option_strings(self):
        '''Returns the old-style option strings associated with the object.

        Returns:
            list: A list of old-style option strings ("-option").
        '''

        return list(filter(is_old_option_string, self.option_strings))

    def get_conflicting_options(self):
        '''Returns a list of conflicting options within the same mutually
        exclusive groups.

        Returns:
            list: A list of Option objects representing conflicting options.
        '''

        if not self.groups:
            return []
        r = []
        for group in self.groups:
            for option in self.parent.options:
                if option.groups is not None and group in option.groups:
                    if option not in r:
                        r.append(option)
        r.remove(self)
        return r

    def get_conflicting_option_strings(self):
        '''Returns a list of option strings conflicting with the current option
        within the same mutually exclusive groups.

        Returns:
            list: A list of option strings representing conflicting options.
        '''

        r = []
        for option in self.get_conflicting_options():
            r.extend(option.get_option_strings())
        return r

    def has_required_arg(self):
        '''Return True if the option takes a required argument.'''

        return self.complete is not None and self.optional_arg is False

    def has_optional_arg(self):
        '''Return True if the option takes an optional argument.'''

        return self.complete is not None and self.optional_arg is True

    def __eq__(self, other):
        return (
            isinstance(other, Option)                   and
            self.option_strings == other.option_strings and
            self.metavar        == other.metavar        and
            self.help           == other.help           and
            self.optional_arg   == other.optional_arg   and
            self.repeatable     == other.repeatable     and
            self.final          == other.final          and
            self.hidden         == other.hidden         and
            self.complete       == other.complete       and
            self.nosort         == other.nosort         and
            self.groups         == other.groups         and
            self.when           == other.when           and
            self.capture        == other.capture
        )

    def __repr__(self):
        return '{option_strings: %r, metavar: %r, help: %r}' % (
            self.option_strings, self.metavar, self.help)


class SubCommandsOption(Positional):
    '''Class holding subcommands of a commandline.'''

    def __init__(self, parent):
        self.subcommands = []

        super().__init__(
            parent,
            parent.get_highest_positional_num() + 1,
            metavar='command')

    def add_commandline_object(self, commandline):
        '''Add an existing commandline object as a subcommand.'''

        if self.get_subcommand_by_name(commandline.prog):
            raise CrazyError(f'Duplicate subcommand. {commandline.prog} already defined.')

        commandline.parent = self.parent
        self.subcommands.append(commandline)

    def add_commandline(self, name, help=''):
        '''Create a new commandline object and add it as a subcommand.'''

        if self.get_subcommand_by_name(name):
            raise CrazyError(f'Duplicate subcommand. {name} already defined.')

        commandline = CommandLine(name, help=help, parent=self.parent)
        self.subcommands.append(commandline)
        return commandline

    def get_choices(self, with_aliases=True):
        '''Return a mapping of command and its description.'''

        r = OrderedDict()
        for subcommand in self.subcommands:
            r[subcommand.prog] = subcommand.help
            if with_aliases:
                for alias in subcommand.aliases:
                    r[alias] = subcommand.help
        return r

    def get_subcommand_by_name(self, name):
        '''Return a subcommand by name or None if not found.'''

        for subcommand in self.subcommands:
            if subcommand.prog == name:
                return subcommand
        return None

    def __eq__(self, other):
        return (
            isinstance(other, SubCommandsOption)  and
            self.subcommands == other.subcommands and
            self.help        == other.help        and
            self.metavar     == other.metavar     and
            self.complete    == other.complete
        )

    def __repr__(self):
        return '{help: %r, subcommands %r}' % (self.help, self.subcommands)


class MutuallyExclusiveGroup:
    '''Helper class for adding mutually exclusive options.'''

    def __init__(self, parent, group):
        assert isinstance(parent, CommandLine)
        assert isinstance(group, str)

        self.parent = parent
        self.group = group

    def add(self, option_strings, **parameters):
        '''Creates and adds a new option.

        For a list of valid parameters, see `class Option`.
        '''

        if 'groups' in parameters:
            raise CrazyError('Paramter `groups` not allowed')

        if 'group' in parameters:
            raise CrazyError('Paramter `group` not allowed')

        return self.parent.add_option(
            option_strings,
            groups=[self.group],
            **parameters)

    def add_option(self, option):
        '''Adds an option object.'''

        option.parent = self.parent
        option.groups = [self.group]
