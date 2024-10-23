Crazy-Complete Documentation
============================

This documentation provides an overview of how to define shell completion for commands using crazy-complete.

**Defining a Command**

To define a completion for a command, use the following structure:

```
prog: "<PROGRAM NAME>"
help: "<PROGRAM DESCRIPTION>"
options:
  <OPTION ...>
positionals:
  <POSITIONAL ...>
```

- *prog*: The name of the program for which you want to create completion
- *help* (optional): A short description of the program
- *options* (optional): A list of options the program accepts
- *positionals* (optional): A list of positional arguments the program uses


**Defining an Option**

To define an option, use this format:

```
[...]
options:
  - option_strings: ["<OPTION STRING>", ...]
    metavar: "<METAVAR>"
    help: "<OPTION DESCRIPTION>"
    takes_args: <BOOL>
    complete: <COMPLETE ACTION>
    multiple_option: <BOOL>
    group: <GROUP>
    when: "<CONDITION>"
[...]
```

- *option\_strings*: A list of option strings (e.g., ["-h", "--help"])
- *metavar* (optional): The placeholder used for the argument (e.g., "FILE")
- *help* (optional): A description of the option
- *takes\_args* (optional): Indicates if the option takes arguments (true or false, default: true)
- *complete* (optional): The method used to generate possible completions for this option
- *multiple\_option* (optional): Indicates whether an option can be suggested multiple times (true or false, default: false)
- *group* (optional): Add this option into the specified group. Multiple flags from the same group cannot be completed at once. Useful for mutually exclusive flags.
- *when* (optional): Only enable this option if CONDITION evaluates to true

**Defining a Positional Argument**

Positional arguments are defined as follows:

```
[...]
positionals:
  - number: <NUMBER>
    metavar: "<METAVAR>"
    help: "<POSITIONAL DESCRIPTION>"
    repeatable: <BOOL>
    complete: <COMPLETE ACTION>
    when: "<CONDITION>"
[...]
```

- *number*: The order of the positional argument (e.g., 1 for the first argument)
- *metavar* (optional): A placeholder for the positional argument in the help text
- *help* (optional): A description of the positional argument
- *repeatable* (optional): Indicates if this positional argument can be repeated (true or false, default: false)
- *complete* (optional): The method used to generate possible completions for this positional argument
- *when* (optional): Only enable this positional if CONDITION evaluates to true

**Defining Subcommands**

To define subcommands, append the subcommand name directly to the program name:

```
prog: "<PROGRAM NAME> <SUBCOMMAND> ..."
aliases: ["<ALIAS>", ...]
help: "<SUBCOMMAND DESCRIPTION>"
[...]
```

- *prog*: The name of the program, followed by the subcommand(s)
- *aliases* (optional): A list of alternative names for the subcommand. Aliases must not include the program name
- *help* (optional): A description of the subcommand
