'''Functions that are used in the generation process.'''

from .errors import CrazyError
from . import completion_validator
from . import cli
from . import config as _config
from . import when

class GenerationContext:
    def __init__(self, config, helpers):
        self.config = config
        self.helpers = helpers

    def getOptionGenerationContext(self, commandline, option):
        return OptionGenerationContext(
            self.config,
            self.helpers,
            commandline,
            option
        )

class OptionGenerationContext(GenerationContext):
    def __init__(self, config, helpers, commandline, option):
        super().__init__(config, helpers)
        self.commandline = commandline
        self.option = option

def _apply_config(commandline, config):
    '''Applies configuration settings to a command line object.

    If a setting in the CommandLine or Option object is set to ExtendedBool.INHERIT,
    it will be overridden by the corresponding setting from the config object.

    Args:
        commandline (CommandLine): The command line object to apply the configuration to.
        config (Config): The configuration object containing the settings to apply.

    Returns:
        None
    '''
    assert isinstance(commandline, cli.CommandLine), \
        "commandline_apply_config: commandline: expected CommandLine, got %r" % commandline

    assert isinstance(config, _config.Config), \
        "commandline_apply_config: config: expected Config, got %r" % config

    if commandline.abbreviate_commands == cli.ExtendedBool.INHERIT:
        commandline.abbreviate_commands = config.abbreviate_commands

    if commandline.abbreviate_options == cli.ExtendedBool.INHERIT:
        commandline.abbreviate_options = config.abbreviate_options

    if commandline.inherit_options == cli.ExtendedBool.INHERIT:
        commandline.inherit_options = config.inherit_options

    for option in commandline.options:
        if option.repeatable == cli.ExtendedBool.INHERIT:
            option.repeatable = config.repeatable_options

def _add_parsed_when(commandline):
    for option in commandline.options:
        if option.when:
            try:
                option.when_parsed = when.parse_when(option.when)
            except CrazyError as e:
                raise CrazyError('%s: %s: %s: %s' % (
                    commandline.get_command_path(),
                    option.get_option_strings_key('|'),
                    option.when,
                    e)) from e
        else:
            option.when_parsed = None

def enhance_commandline(commandline, config):
    '''Enhance commandline.

    - Make a copy of commandline
    - Apply configuration to it
    - Add `when_parsed` attribute
    '''

    commandline = commandline.copy()
    commandline.visit_commandlines(lambda c: _apply_config(c, config))
    commandline.visit_commandlines(lambda c: _add_parsed_when(c))
    completion_validator.validate_commandlines(commandline)
    return commandline

def visit_commandlines(completion_class, ctxt, commandline):
    '''Visit commandlines with a completer class.'''

    result = []

    def _call_generator(commandline):
        result.append(completion_class(ctxt, commandline))

    commandline.visit_commandlines(_call_generator)

    return result
