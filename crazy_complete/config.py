#!/usr/bin/python3

def _is_bool(obj):
    return isinstance(obj, bool)

class Config:
    '''
    A class representing configuration settings for command line completion.
    '''

    def __init__(self):
        self.abbreviate_commands = False
        self.abbreviate_options = False
        self.multiple_options = False
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
            enable (bool): If True, commands can be abbreviated; if False, they cannot.

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
            commandline.CommandLine(..., abbreviate_commands=BOOL, ...)
        '''
        assert _is_bool(enable), "Config.set_abbreviate_commands: enable: expected bool, got %r" % enable

        self.abbreviate_commands = enable

    def set_abbreviate_options(self, enable):
        '''
        Sets whether options can be abbreviated.

        Args:
            enable (bool): If True, options can be abbreviated; if False, they cannot.

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
            commandline.CommandLine(..., abbreviate_options=BOOL, ...)
        '''
        assert _is_bool(enable), "Config.set_abbreviate_options: enable: expected bool, got %r" % enable

        self.abbreviate_options = enable

    def set_multiple_options(self, enable):
        '''
        Sets whether options are suggested multiple times during completion.

        Args:
            enable (bool): If True, options can appear multiple times during completion;
                           if False, options are suggested only once.

        Notes:
            This feature defaults to `False`.

            Implementation status for shells:
                Bash:
                    - set_multiple_options(True): works
                    - set_multiple_options(False): works
                Fish:
                    - set_multiple_options(True): works
                    - set_multiple_options(False): works
                Zsh:
                    - set_multiple_options(True): works
                    - set_multiple_options(False): works

        See also:
            CommandLine.add(..., multiple_option=BOOL, ...)
        '''
        assert _is_bool(enable), "Config.set_multiple_options: enable: expected bool, got %r" % enable

        self.multiple_options = enable

    def set_inherit_options(self, enable):
        '''
        Sets whether parent options are visible to subcommands.

        Args:
            enable (bool): If True, parent options are visible to subcommands.
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
            commandline.CommandLine(..., inherit_options=BOOL, ...)
        '''
        assert _is_bool(enable), "Config.set_inherit_options: enable: expected bool, got %r" % enable

        self.inherit_options = enable

    def set_vim_modeline(self, enable):
        '''
        Sets whether a vim modeline comment shall be appended to the generated code.

        The modeline comment looks like this:

            # vim: ft=zsh

        Args:
            enable (bool): If True, add a vim modline comment; if False, don't add a modline comment.

        Notes:
            This feature defaults to `True`.
        '''
        assert _is_bool(enable), "Config.set_vim_modeline: enable: expected bool, got %r" % enable

        self.vim_modeline = enable

    def set_zsh_compdef(self, enable):
        assert _is_bool(enable), "Config.set_zsh_compdef: enable: expected bool, got %r" % enable

        self.zsh_compdef = enable

    def include_file(self, file):
        # TODO: docstring
        self.include_files.append(file)

    def include_many_files(self, files):
        # TODO: docstring
        self.include_files.extend(files)

    def set_fish_fast(self, enable):
        self.fish_fast = enable

    def set_fish_inline_conditions(self, enable):
        self.fish_inline_conditions = enable

