'''Classes for generating file output.'''

from . import modeline
from . import generation_notice


class Output:
    '''Class for generating output.'''

    def __init__(self, config, helpers):
        self.config = config
        self.helpers = helpers
        self.output = []

    def add(self, string):
        '''Add to output.'''
        self.output.append(string)

    def extend(self, strings):
        '''Add many to output.'''
        self.output.extend(strings)

    def add_as_block(self):
        '''Return a helper context manager for adding a multi-line block.'''

        class _Block:
            def __init__(self, parent):
                self.parent = parent
                self.lines = []

            def add(self, line):
                '''Add a single line to the current block.'''
                self.lines.append(line)

            def extend(self, lines):
                '''Add multiple lines to current block.'''
                self.lines.extend(lines)

            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc_val, exc_tb):
                block_text = "\n".join(self.lines)
                self.parent.output.append(block_text)

        return _Block(self)

    def add_generation_notice(self):
        '''Add the generation notice.'''
        self.add(generation_notice.GENERATION_NOTICE)

    def add_comments(self):
        '''Add additioanl comments.'''
        if self.config.comments:
            self.add(self.config.get_comments_as_string())

    def add_included_files(self):
        '''Add included files.'''
        self.output.extend(self.config.get_included_files_content())

    def add_helper_functions_code(self):
        '''Add helper functions.'''
        for code in self.helpers.get_used_functions_code():
            self.add(code)

    def add_vim_modeline(self, shell):
        '''Add the vim modeline.'''
        if self.config.vim_modeline:
            self.add(modeline.get_vim_modeline(shell))

    def get(self):
        '''Return the output.'''
        return '\n\n'.join(self.output)
