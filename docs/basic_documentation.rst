Crazy-Complete Documentation
============================

.. contents::
   :local:
   :depth: 2

This documentation provides an overview of how to define shell completions for commands using **crazy-complete**.

Command Definition
------------------

To define a completion for a command, use the following structure:

.. code-block:: yaml

   prog: "<PROGRAM NAME>"
   help: "<PROGRAM DESCRIPTION>"
   options:
     <OPTION ...>
   positionals:
     <POSITIONAL ...>

:prog:
   The name of the program for which you want to create completion.
:help:
   *(optional)* A short description of the program.
:options:
   *(optional)* A list of options the program accepts.
:positionals:
   *(optional)* A list of positional arguments the program uses.

Example:

.. code-block:: yaml

   prog: "git"
   help: "Distributed version control system"

Option Definition
-----------------

Options are defined as follows:

.. code-block:: yaml

   options:
     - option_strings: ["<OPTION STRING>", ...]
       metavar: "<METAVAR>"
       help: "<OPTION DESCRIPTION>"
       optional_arg: <BOOL>
       complete: <COMPLETE ACTION>
       repeatable: <BOOL>
       final: <BOOL>
       hidden: <BOOL>
       groups: ["<GROUP>", ...]
       when: "<CONDITION>"

:option_strings:
   A list of option strings (e.g., ``["-h", "--help"]``).
:metavar:
   *(optional)* The placeholder used for the argument (e.g., ``FILE``).
:help:
   *(optional)* A description of the option.
:optional_arg:
   *(optional)* Indicates if the option's argument is optional (default: ``false``).
:complete:
   *(optional)* Defines the completion method.  
   If not set, the option does not take an argument.  
   Use ``["none"]`` if the option accepts an argument but no specific completion method applies.
:repeatable:
   *(optional)* Whether an option can be used multiple times (default: ``false``).
:final:
   *(optional)* If true, no further options are suggested after this one.  
   Commonly used for ``--help`` or ``--version`` (default: ``false``).
:hidden:
   *(optional)* Excludes this option from completion suggestions, but it remains valid when typed manually.
:groups:
   *(optional)* Assigns this option to one or more groups.  
   Multiple options from the same group cannot be suggested at once, useful for mutually exclusive flags.
:when:
   *(optional)* Enables this option only if the condition evaluates to true.

Example:

.. code-block:: yaml

   options:
     - option_strings: ["--directory", "-C"]
       metavar: "PATH"
       help: "Run as if git was started in PATH"
       complete: ["directory"]

Positional Arguments
--------------------

Positional arguments are defined as follows:

.. code-block:: yaml

   positionals:
     - number: <NUMBER>
       metavar: "<METAVAR>"
       help: "<POSITIONAL DESCRIPTION>"
       repeatable: <BOOL>
       complete: <COMPLETE ACTION>
       when: "<CONDITION>"

:number:
   The order of the positional argument (e.g., ``1`` for the first argument).
:metavar:
   *(optional)* Placeholder for the positional argument in the help text.
:help:
   *(optional)* A description of the positional argument.
:repeatable:
   *(optional)* Whether this argument can be repeated (default: ``false``).
:complete:
   *(optional)* Completion method to generate possible values (default: ``["none"]``).
:when:
   *(optional)* Enables this positional only if the condition evaluates to true.

Example:

.. code-block:: yaml

   positionals:
     - number: 1
       metavar: "FILE"
       help: "File to process"
       complete: ["file"]

Subcommands
-----------

Subcommands are defined by appending them to the program name:

.. code-block:: yaml

   prog: "<PROGRAM NAME> <SUBCOMMAND> ..."
   aliases: ["<ALIAS>", ...]
   help: "<SUBCOMMAND DESCRIPTION>"

:prog:
   The name of the program, followed by the subcommand(s).
:aliases:
   *(optional)* A list of alternative names for the subcommand.  
   Aliases must not include the program name.
:help:
   *(optional)* A description of the subcommand.

Example:

.. code-block:: yaml

   prog: "kubectl get"
   help: "Display one or many resources"
   options:
     - option_strings: ["--output"]
       complete: ["choices", ["json", "yaml", "wide"]]

Best Practices
--------------

* Use ``["none"]`` only when a value is required but no completion applies.
* Use ``repeatable: true`` for options like ``--tag`` or ``--define``.
* Set ``final: true`` for options like ``--help`` or ``--version`` so no further suggestions appear afterward.
* Use groups for mutually exclusive flags to improve user experience.

