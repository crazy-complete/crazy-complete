'''This module contains the configuration class.'''


def _assert_is_bool(obj, func, param):
    if not isinstance(obj, bool):
        raise AssertionError(f"Config.{func}: {param}: expected bool, got `{obj}`")


class Config:
    '''Class representing configuration settings for command line completion.'''

    # pylint: disable=too-many-instance-attributes
    # pylint: disable=too-many-public-methods

    def __init__(self):
        self.function_prefix        = '_$PROG'
        self.debug                  = False
        self.abbreviate_commands    = False
        self.abbreviate_options     = False
        self.repeatable_options     = False
        self.inherit_options        = False
        self.option_stacking        = True
        self.vim_modeline           = True
        self.include_files          = []
        self.comments               = []
        self.keep_comments          = False
        self.bash_completions_version = (2,)
        self.zsh_compdef            = True
        self.fish_fast              = False
        self.fish_inline_conditions = False

        self.disabled_hidden        = False
        self.disabled_final         = False
        self.disabled_groups        = False
        self.disabled_repeatable    = False
        self.disabled_when          = False

    def set_function_prefix(self, prefix):
        '''Sets the function prefix used for generated functions.

        Args:
            prefix (str):
                The prefix to be used. May contain the `$PROG` placeholder.

        Notes:
            This defaults to `_$PROG`
        '''

        assert isinstance(prefix, str), \
            f"Config.set_function_prefix: prefix: expected str, got `{prefix}`"

        self.function_prefix = prefix

    def set_debug(self, enable):
        '''Sets debug mode.

        Args:
            enable (bool):
                If True, additional code for debugging is generated.

        Notes:
            This feature defaults to `False`.
        '''

        _assert_is_bool(enable, "set_debug", "enable")

        self.debug = enable

    def set_abbreviate_commands(self, enable):
        '''Sets whether commands can be abbreviated.

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

        See Also:
            cli.CommandLine(..., abbreviate_commands=BOOL, ...)
        '''

        _assert_is_bool(enable, "set_abbreviate_commands", "enable")

        self.abbreviate_commands = enable

    def set_abbreviate_options(self, enable):
        '''Sets whether options can be abbreviated.

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

        See Also:
            cli.CommandLine(..., abbreviate_options=BOOL, ...)
        '''

        _assert_is_bool(enable, "set_abbreviate_options", "enable")

        self.abbreviate_options = enable

    def set_repeatable_options(self, enable):
        '''Sets whether options are suggested multiple times during completion.

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

        See Also:
            cli.CommandLine.add_option(..., repeatable=BOOL, ...)
        '''

        _assert_is_bool(enable, "set_repeatable_options", "enable")

        self.repeatable_options = enable

    def set_inherit_options(self, enable):
        '''Sets whether parent options are visible to subcommands.

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

        See Also:
            cli.CommandLine(..., inherit_options=BOOL, ...)
        '''

        _assert_is_bool(enable, "set_inherit_options", "enable")

        self.inherit_options = enable

    def set_option_stacking(self, enable):
        '''Sets wether short option stacking is allowed.

        Args:
            enable (bool):
                IF True, option stacking is allowed.
                If False, it is not.

        Notes:
            This feature defaults to `True`.

            Implementation status for shells:
                Bash:
                    - set_option_stacking(True): works
                    - set_option_stacking(False): not implemented
                Fish:
                    - set_option_stacking(True): works
                    - set_option_stacking(False): works
                Zsh:
                    - set_option_stacking(True): works
                    - set_option_stacking(False): works

        '''

        _assert_is_bool(enable, "set_option_stacking", "enable")

        self.option_stacking = enable

    def set_vim_modeline(self, enable):
        '''Sets whether a vim modeline comment shall be appended to the generated code.

        The modeline comment looks like this:

            # vim: ft=zsh ts=2 sts=2 sw=2 et

        Args:
            enable (bool):
                If True, add a vim modline comment;
                if False, don't add a modline comment.

        Notes:
            This feature defaults to `True`.
        '''

        _assert_is_bool(enable, "set_vim_modeline", "enable")

        self.vim_modeline = enable

    def set_bash_completions_version(self, version):
        '''Sets the version of bash-completions.

        Args:
            version (tuple):
                A tuple in form like (2,) or (2, 12).

        Notes:
            This defaults to (2,).
        '''

        assert isinstance(version, tuple), \
            "Config.set_bash_completions_version(): version: expected tuple"

        self.bash_completions_version = version

    def set_zsh_compdef(self, enable):
        '''Sets whether a `#compdef` comment is written at the top of the generated
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

    def set_keep_comments(self, enable):
        '''Sets whether comments shall be included in the generated code.

        Args:
            enable (bool):
                If True, comments are included.
                if False, don't include comments.

        Notes:
            This feature defaults to `False`.
        '''

        _assert_is_bool(enable, "set_keep_comments", "enable")

        self.keep_comments = enable

    def set_fish_fast(self, enable):
        '''Use faster conditions at the cost of correctness.'''

        _assert_is_bool(enable, "set_fish_fast", "enable")

        self.fish_fast = enable

    def set_fish_inline_conditions(self, enable):
        '''Don't store conditions in an extra variable.'''

        _assert_is_bool(enable, "set_fish_inline_conditions", "enable")

        self.fish_inline_conditions = enable

    def include_file(self, file):
        '''Add a file which should be included to the generated code.'''

        assert isinstance(file, str), \
            f"Config.include_file: file: expected str, got `{file}`"

        self.include_files.append(file)

    def include_many_files(self, files):
        '''Add files which should be included to the generated code.'''

        assert hasattr(files, '__iter__') and not isinstance(files, str), \
            f"Config.include_many_files: files: expected iterable, got `{files}`"

        self.include_files.extend(files)

    def add_comments(self, comments):
        '''Add comments to the generated output.'''

        assert hasattr(comments, '__iter__') and not isinstance(comments, str), \
            f"Config.include_many_comments: comments: expected iterable, got `{comments}`"

        self.comments.extend(comments)

    def get_included_files_content(self):
        '''Return a list of contents of all included files.'''

        content = []

        for file in self.include_files:
            with open(file, 'r', encoding='utf-8') as fh:
                content.append(fh.read().strip())

        return content

    def get_comments_as_string(self):
        '''Return a string of all comments.'''

        return '\n'.join(f'# {c}' for c in self.comments)

    def disable_hidden(self, disable):
        '''Disable hidden options.

        This disables hidden options completely.
        '''

        _assert_is_bool(disable, "disable_hidden", "disable")

        self.disabled_hidden = disable

    def disable_final(self, disable):
        '''Disable final options.

        This disables final options completely.
        '''

        _assert_is_bool(disable, "disable_final", "disable")

        self.disabled_final = disable

    def disable_groups(self, disable):
        '''Disable option grouping.

        This disables the mutually exclusive feature for options completely.
        '''

        _assert_is_bool(disable, "disable_groups", "disable")

        self.disabled_groups = disable

    def disable_repeatable(self, disable):
        '''Disable repeatable options.

        This disables repeatable options completely.

        Despite its name, this function actually does the opposite:
        Instead of making all options non-repeatable, it makes all options
        repeatable.
        '''

        _assert_is_bool(disable, "disable_repeatable", "disable")

        self.disabled_repeatable = disable

    def disable_when(self, disable):
        '''Disable when feature.

        This disables conditional options and positionals completely.
        '''

        _assert_is_bool(disable, "disable_when", "disable")

        self.disabled_when = disable
