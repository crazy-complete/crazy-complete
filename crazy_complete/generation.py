''' Functions that are used in the generation process '''

from . import completion_validator
from . import cli
from . import utils
from . import config as _config

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

def enhance_commandline(commandline, program_name, config):
    commandline = commandline.copy()

    if program_name is not None:
        commandline.prog = program_name

    if config is None:
        config = _config.Config()

    cli.commandline_apply_config(commandline, config)
    completion_validator.CompletionValidator().validate_commandlines(commandline)
    return commandline

class CompletionGenerator:
    def __init__(self, completion_class, helpers_class, commandline, config):
        self.include_files_content = []
        for file in config.include_files:
            with open(file, 'r', encoding='utf-8') as fh:
                self.include_files_content.append(fh.read().strip())

        self.completion_class = completion_class
        self.ctxt = GenerationContext(config, helpers_class(commandline.prog))
        self.result = []
        commandline.visit_commandlines(self._call_generator)

    def _call_generator(self, commandline):
        self.result.append(self.completion_class(self.ctxt, commandline))
