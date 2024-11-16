'''This module contains the configuration class'''

def _assert_is_bool(obj, func, param):
    if not isinstance(obj, bool):
        raise AssertionError(f"Config.{func}: {param}: expected bool, got `{obj}`")

class Config:
    '''
    A class representing configuration settings for command line completion.
    '''

    def __init__(self):
        self.abbreviate_commands = False
        self.abbreviate_options = False
        self.repeatable_options = False
        self.inherit_options = False
        self.vim_modeline = True
        self.include_files = []
        self.zsh_compdef = True
        self.fish_fast = False
        self.fish_inline_conditions = False

    def set_abbreviate_commands(self, enable):
        '''
        Sets whether commands can be abbreviated.

        Args:
            enable (bool):
                If True, commands can be abbreviated; if False, they cannot.

        Notes:
            This feature defaults to `False`.

            Implementation status for shells:
                Bash:
                    - set_abbreviate_commands(True): works
                    - set_abbreviate_commands(False): works
                Fish:
                    - set_abbreviate_commands(True): works
                    - set_abbreviate_commands(False): works
                Zsh:
                    - set_abbreviate_commands(True): works
                    - set_abbreviate_commands(False): works

        See also:
            cli.CommandLine(..., abbreviate_commands=BOOL, ...)
        '''
        _assert_is_bool(enable, "set_abbreviate_commands", "enable")

        self.abbreviate_commands = enable

    def set_abbreviate_options(self, enable):
        '''
        Sets whether options can be abbreviated.

        Args:
            enable (bool):
                If True, options can be abbreviated; if False, they cannot.

        Notes:
            This feature defaults to `False`.

            Implementation status for shells:
                Bash:
                    - set_abbreviate_options(True): works
                    - set_abbreviate_options(False): works
                Fish:
                    - set_abbreviate_options(True): not implemented
                    - set_abbreviate_options(False): works
                Zsh:
                    - set_abbreviate_options(True): not implemented
                    - set_abbreviate_options(False): works

        See also:
            cli.CommandLine(..., abbreviate_options=BOOL, ...)
        '''
        _assert_is_bool(enable, "set_abbreviate_options", "enable")

        self.abbreviate_options = enable

    def set_repeatable_options(self, enable):
        '''
        Sets whether options are suggested multiple times during completion.

        Args:
            enable (bool):
                If True, options can appear multiple times during completion;
                if False, options are suggested only once.

        Notes:
            This feature defaults to `False`.

            Implementation status for shells:
                Bash:
                    - set_repeatable_options(True): works
                    - set_repeatable_options(False): works
                Fish:
                    - set_repeatable_options(True): works
                    - set_repeatable_options(False): works
                Zsh:
                    - set_repeatable_options(True): works
                    - set_repeatable_options(False): works

        See also:
            cli.CommandLine.add_option(..., repeatable=BOOL, ...)
        '''
        _assert_is_bool(enable, "set_repeatable_options", "enable")

        self.repeatable_options = enable

    def set_inherit_options(self, enable):
        '''
        Sets whether parent options are visible to subcommands.

        Args:
            enable (bool):
                If True, parent options are visible to subcommands.
                If False, they are not.

        Notes:
            This feature defaults to `False`.

            Implementation status for shells:
                Bash:
                    - set_inherit_options(True): works
                    - set_inherit_options(False): works
                Fish:
                    - set_inherit_options(True): works
                    - set_inherit_options(False): works
                Zsh:
                    - set_inherit_options(True): works
                    - set_inherit_options(False): works

        See also:
            cli.CommandLine(..., inherit_options=BOOL, ...)
        '''
        _assert_is_bool(enable, "set_inherit_options", "enable")

        self.inherit_options = enable

    def set_vim_modeline(self, enable):
        '''
        Sets whether a vim modeline comment shall be appended to the generated code.

        The modeline comment looks like this:

            # vim: ft=zsh

        Args:
            enable (bool):
                If True, add a vim modline comment;
                if False, don't add a modline comment.

        Notes:
            This feature defaults to `True`.
        '''
        _assert_is_bool(enable, "set_vim_modeline", "enable")

        self.vim_modeline = enable

    def set_zsh_compdef(self, enable):
        '''
        Sets whether a `#compdef` comment is written at the top of the generated
        zsh script.

        The `#compdef` directive is used by Zsh to automatically associate the
        generated completion file with a command, enabling autoload functionality.

        If you plan to load the Zsh completion file manually by sourcing it,
        omitting this line may be necessary.

        Args:
            enable (bool):
                If true, add a `#compdef` line on top of the file;
                If false, don't add a `#compdef` line.

        Notes:
            This feature defaults to `True`
        '''
        _assert_is_bool(enable, "set_zsh_compdef", "enable")

        self.zsh_compdef = enable

    def set_fish_fast(self, enable):
        _assert_is_bool(enable, "set_fish_fast", "enable")

        self.fish_fast = enable

    def set_fish_inline_conditions(self, enable):
        _assert_is_bool(enable, "set_fish_inline_conditions", "enable")

        self.fish_inline_conditions = enable

    def include_file(self, file):
        '''
        Add a file which should be included to the generated code.
        '''
        assert isinstance(file, str), \
            f"Config.include_file: file: expected str, got `{file}`"

        self.include_files.append(file)

    def include_many_files(self, files):
        '''
        Add files which should be included to the generated code.
        '''
        self.include_files.extend(files)

    def get_included_files_content(self):
        content = []
        for file in self.include_files:
            with open(file, 'r', encoding='utf-8') as fh:
                content.append(fh.read().strip())
        return content
