Synopsis
========

``crazy-complete [OPTIONS] {bash,fish,zsh,yaml,json} <DEFINITION_FILE>``

Options
=======

.. option:: --input-type={yaml,json,python,help,auto}

   Specify input file type. With ``auto`` the file extension will be used
   to determine the input type.

.. option:: --abbreviate-commands={True,False}

   Sets whether commands can be abbreviated.

.. option:: --abbreviate-options={True,False}

   Sets whether options can be abbreviated.
   **Note:** Abbreviated options are not supported by Fish and Zsh.

.. option:: --repeatable-options={True,False}

   Sets whether options are suggested multiple times during completion.

.. option:: --inherit-options={True,False}

   Sets whether parent options are visible to subcommands.

.. option:: --vim-modeline={True,False}

   Sets whether a vim modeline comment shall be appended to the generated code.

.. option:: --include-file=FILE

   Include contents of FILE in output.

.. option:: -o, --output=FILE

   Write output to destination file. [default: stdout]

.. option:: -i, --install-system-wide

   Write output to the system-wide completions directory of the shell.

.. option:: -u, --uninstall-system-wide

   Uninstall the system-wide completion file for the program.
