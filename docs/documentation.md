Crazy-Complete Documentation
============================

This documentation provides an overview of how to define shell completion for commands using crazy-complete.

- [Generating a Defintion File from Help](#generating-a-definition-file-from-help)
- [Defining a Command](#defining-a-command)
- [Defining an Option](#defining-an-option)
- [Defining a Positional Argument](#defining-a-positional-argument)
- [Completion Commands](#completion-commands)
  - [Built-in Commands](#built-in-commands)
  - [User-Defined Commands](#user-defined-commands)
- [When Conditionals](#when-conditionals)
- [Capturing Options](#capturing-options)
- [Tips and Tricks](#tips-and-tricks)

## Generating a Definition File from Help

It is possible to generate a definition file from a commands help output:

```
grep --help > help_file
crazy-complete --input-type=help yaml help_file

# or

grep --help | crazy-complete --input-type=help yaml /dev/stdin
```

## Defining a Command

To define a completion for a command, use the following structure:

```yaml
prog: "<PROGRAM NAME>"
aliases: ["<ALIAS>", ...]
help: "<PROGRAM DESCRIPTION>"
options:
  <OPTION ...>
positionals:
  <POSITIONAL ...>
```

- *prog*: The name of the program for which you want to create completion
- *aliases* (optional): Specify alternative program names for which this completion should also apply
- *help* (optional): A short description of the program
- *options* (optional): A list of [options](#defining-an-option) the program accepts
- *positionals* (optional): A list of [positional arguments](#defining-a-positional-argument) the program uses

## Defining an Option

To define an option, use this format:

```yaml
[...]
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
    capture: "<VARIABLE>"
[...]
```

- *option\_strings*: A list of option strings (e.g., ["-h", "--help"])
- *metavar* (optional): The placeholder used for the argument (e.g., "FILE")
- *help* (optional): A description of the option
- *optional\_arg* (optional): Indicates if the option's argument is optional (default: false)
- *complete* (optional): Defines the method used to provide possible completions for this option. If not set, the option does not take an argument. Use `["none"]` if the option accepts an argument but no specific completion method applies. See [Completion Commands](#completion-commands)
- *repeatable* (optional): Indicates whether an option can be suggested multiple times (true or false, default: false)
- *final* (optional): The final parameter indicates that no further options are shown after this one if it is passed on command line. Mostly used for --help and --version (default: false)
- *hidden* (optional): Specifies whether an option should be excluded from the auto-completion suggestions, though it remains usable when typed manually. (default: false)
- *groups* (optional): Add this option into the specified groups. Multiple flags from the same group cannot be completed at once. Useful for mutually exclusive flags
- *when* (optional): Only enable this option if [CONDITION](#when-conditionals) evaluates to true
- *capture* (optional): Specify the [variable](#capturing-options) where values of this option should be captured

## Defining a Positional Argument

Positional arguments are defined as follows:

```yaml
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
- *complete* (optional): The method used to generate possible completions for this positional argument. Default `["none"]`. See [Completion Commands](#completion-commands).
- *when* (optional): Only enable this positional if [CONDITION](#when-conditionals) evaluates to true

## Defining Subcommands

To define subcommands, append the subcommand name directly to the program name:

```yaml
prog: "<PROGRAM NAME> <SUBCOMMAND> ..."
aliases: ["<ALIAS>", ...]
help: "<SUBCOMMAND DESCRIPTION>"
[...]
```

- *prog*: The name of the program, followed by the subcommand(s)
- *aliases* (optional): A list of alternative names for the subcommand. Aliases must not include the program name
- *help* (optional): A description of the subcommand

## Completion Commands

### Built-in Commands

| Command                          | Description                                                                 |
|----------------------------------|-----------------------------------------------------------------------------|
| [none](#none)                    | No completion, but specifies that an argument is required                   |
| [integer](#integer)              | Complete an integer                                                         |
| [float](#float)                  | Complete a floating point number                                            |
| [combine](#combine)              | Combine multiple completion commands                                        |
| [file](#file)                    | Complete a file                                                             |
| [directory](#directory)          | Complete a directory                                                        |
| [choices](#choices)              | Complete from a set of values                                               |
| [value\_list](#value_list)       | Complete a list                                                             |
| [range](#range)                  | Complete a range of integers                                                |
| [signal](#signal)                | Complete a signal                                                           |
| [hostname](#hostname)            | Complete a hostname                                                         |
| [process](#process)              | Complete a process                                                          |
| [pid](#pid)                      | Complete a PID                                                              |
| [command](#command)              | Complete a command                                                          |
| [user](#user)                    | Complete a user                                                             |
| [group](#group)                  | Complete a group                                                            |
| [service](#service)              | Complete a SystemD service                                                  |
| [variable](#variable)            | Complete a shell variable                                                   |
| [environment](#environment)      | Complete a environment variable                                             |
| [history](#history)              | Complete based on a shell's history                                         |


### Bonus Commands

| Command                          | Description                                                                 |
|----------------------------------|-----------------------------------------------------------------------------|
| net\_interface                   | Complete a network interface                                                |
| mountpoint                       | Complete a mountpoint                                                       |
| login\_shell                     | Complete a login shell                                                      |
| charset                          | Complete a charset                                                          |
| locale                           | Complete a locale                                                           |
| timezone                         | Complete a timezone                                                         |
| alsa\_card                       | Complete an ALSA card                                                       |
| alsa\_device                     | Complete an ALSA device                                                     |

### User-defined Commands

> User-defined commands may require including additional code with `--include-file=FILE`

| Command                          | Description                                                                 |
|----------------------------------|-----------------------------------------------------------------------------|
| [exec](#exec)                    | Complete by the output of a command or function                             |
| [exec\_fast](#exec_fast)         | Complete by the output of a command or function (fast and unsafe)           |
| [exec\_internal](#exec_internal) | Complete by a function that uses the shell's internal completion mechanisms |

### none

> Disables autocompletion for this option but still marks it as requiring an argument.
>
> Without specifying `complete`, the option would not take an argument.

```yaml
prog: "example"
options:
  - option_strings: ["--none"]
    complete: ["none"]
```

### integer

> Complete an integer.
>
> **NOTE**: This completion currently serves as documentation and does not provide actual functionality.
>
> If you want to complete a range of integers, see **range**.

```yaml
prog: "example"
options:
  - option_strings: ["--integer"]
    complete: ["integer"]
```

### float

> Complete a floating point number.
>
> **NOTE**: This completion currently serves as documentation and does not provide actual functionality.

```yaml
prog: "example"
options:
  - option_strings: ["--float"]
    complete: ["float"]
```

### combine

> Combine two or more completion commands.

```yaml
prog: "example"
options:
  - option_strings: ["--combine"]
    complete: ["combine", [["user"], ["pid"]]]
```

### file

> Complete a file.
>
> You can restrict completion to a specific directory by adding `{"directory": ...}`.

```yaml
prog: "example"
options:
  - option_strings: ["--file"]
    complete: ["file"]
  - option_strings: ["--file-tmp"]
    complete: ["file", {"directory": "/tmp"}]
```

```
 ~ > example --file=<TAB>
 dir1/  dir2/  file1  file2
```

### directory

> Complete a directory.
>
> You can restrict completion to a specific directory by adding `{"directory": ...}`.

```yaml
prog: "example"
options:
  - option_strings: ["--directory"]
    complete: ["directory"]
  - option_strings: ["--directory-tmp"]
    complete: ["directory", {"directory": "/tmp"}]
```

```
 ~ > example --directory=<TAB>
 dir1/  dir2/
```

### choices

> Complete a list of items.
>
> Items can be a list or a dictionary.
>
> If a dictionary is supplied, the keys are used as items and the values are used
> as description.

```yaml
prog: "example"
options:
  - option_strings: ["--choices-1"]
    complete: ["choices", ["Item 1", "Item 2"]]
  - option_strings: ["--choices-2"]
    complete: ["choices", {"Item 1": "Description 1", "Item 2": "Description 2"}]
```

```
 ~ > example --choices-2=<TAB>
Item 1  (Description 1)  Item 2  (Description 2)
```

### value\_list

> Complete one or more items from a list of items. Similar to `mount -o`.
>
> Arguments with assignable values (`mount -o uid=1000`) aren't supported.
>
> Arguments are supplied by adding `{"values": ...}`.
>
> A separator can be supplied by adding `{"separator": ...}` (the default is `","`).

```yaml
prog: "example"
options:
  - option_strings: ["--value-list-1"]
    complete: ["value_list", {"values": ["exec", "noexec"]}]
  - option_strings: ["--value-list-2"]
    complete: ["value_list", {"values": {"one": "Description 1", "two": "Description 2"}}]
```

```
 ~ > example --value-list-1=<TAB>
exec    noexec
 ~ > example --value-list-1=exec,<TAB>
exec    noexec
 ~ > example --value-list-2=<TAB>
one  -- Description 1
two  -- Description 2
```

### exec

> Execute a command and parse the output.
>
> The output must be in form of:
```
<item_1>\t<description_1>\n
<item_2>\t<description_2>\n
[...]
```
> An item and its description are delimited by a tabulator.
>
> These pairs are delimited by a newline.

```yaml
prog: "example"
options:
  - option_strings: ["--exec"]
    complete: ["exec", "printf '%s\\t%s\\n' 'Item 1' 'Description 1' 'Item 2' 'Description 2'"]
```

```
 ~ > example --exec=<TAB>
Item 1  (Description 1)  Item 2  (Description 2)
```

### exec\_fast

> Faster version of exec for handling large amounts of data.
>
> This implementation requires that the items of the parsed output do not include
> special shell characters or whitespace.

```yaml
prog: "example"
options:
  - option_strings: ["--exec-fast"]
    complete: ["exec_fast", "printf '%s\\t%s\\n' 1 one 2 two"]
```

### exec\_internal

> Execute a function that internally modifies the completion state.
>
> This is useful if a more advanced completion is needed.

```yaml
prog: "example"
options:
  - option_strings: ["--exec-internal"]
    complete: ["exec_internal", "my_completion_func"]
```

> For Bash, it might look like:
```
my_completion_func() {
    COMPREPLY=( $(compgen -W "foo bar baz") )
}
```
> For Zsh, it might look like:
```
my_completion_func() {
    local items=( foo bar baz )
    _describe '' items
}
```
> For Fish, it might look like:
```
function my_completion_func
    printf '%s\n' foo bar baz
end
```

### range

> Complete a range of integers.

```yaml
prog: "example"
options:
  - option_strings: ["--range-1"]
    complete: ["range", 1, 9]
  - option_strings: ["--range-2"]
    complete: ["range", 1, 9, 2]
```

```
 ~ > example --range-1=<TAB>
1  2  3  4  5  6  7  8  9
 ~ > example --range-2=<TAB>
1  3  5  7  9
```

### signal

> Complete signal names (INT, KILL, TERM, etc.).

```yaml
prog: "example"
options:
  - option_strings: ["--signal"]
    complete: ["signal"]
```

```
 ~ > example --signal=<TAB>
ABRT    -- Process abort signal
ALRM    -- Alarm clock
BUS     -- Access to an undefined portion of a memory object
CHLD    -- Child process terminated, stopped, or continued
CONT    -- Continue executing, if stopped
FPE     -- Erroneous arithmetic operation
HUP     -- Hangup
ILL     -- Illegal instruction
INT     -- Terminal interrupt signal
[...]
```

### hostname

> Complete a hostname.

```yaml
prog: "example"
options:
  - option_strings: ["--hostname"]
    complete: ["hostname"]
```

```
 ~ > example --hostname=<TAB>
localhost
```

### process

> Complete a process name.

```yaml
prog: "example"
options:
  - option_strings: ["--process"]
    complete: ["process"]
```

```
 ~ > example --process=s<TAB>
scsi_eh_0         scsi_eh_1       scsi_eh_2      scsi_eh_3  scsi_eh_4
scsi_eh_5         sh              sudo           syndaemon  systemd
systemd-journald  systemd-logind  systemd-udevd
```

### pid

> Complete a PID.

```yaml
prog: "example"
options:
  - option_strings: ["--pid"]
    complete: ["pid"]
```

```
 ~ > example --pid=<TAB>
1       13      166     19      254     31      45
1006    133315  166441  19042   26      32      46
10150   1392    166442  195962  27      33      4609
```

### command

> Complete a command.

```yaml
prog: "example"
options:
  - option_strings: ["--command"]
    complete: ["command"]
```

```
 ~ > example --command=bas<TAB>
base32    base64    basename  basenc    bash      bashbug
```

### user

> Complete a username.

```yaml
prog: "example"
options:
  - option_strings: ["--user"]
    complete: ["user"]
```

```
 ~ > example --user=<TAB>
avahi                   bin                     braph
colord                  daemon                  dbus
dhcpcd                  ftp                     git
[...]
```

### group

> Complete a group.

```yaml
prog: "example"
options:
  - option_strings: ["--group"]
    complete: ["group"]
```

```
 ~ > example --group=<TAB>
adm                     audio                   avahi
bin                     braph                   colord
daemon                  dbus                    dhcpcd
disk                    floppy                  ftp
games                   git                     groups
[...]
```

### service

> Complete a SystemD service.

```yaml
prog: "example"
options:
  - option_strings: ["--service"]
    complete: ["service"]
```

```
 ~ > example --service=<TAB>
TODO
[...]
```

### variable

> Complete a shell variable name.
>
> To complete an environment variable, use **environment**.

```yaml
prog: "example"
options:
  - option_strings: ["--variable"]
    complete: ["variable"]
```

```
 ~ > example --variable=HO<TAB>
HOME      HOSTNAME  HOSTTYPE
```

### environment

> Complete a shell environment variable name.

```yaml
prog: "example"
options:
  - option_strings: ["--environment"]
    complete: ["environment"]
```

```
 ~ > example --environment=X<TAB>
XDG_RUNTIME_DIR  XDG_SEAT  XDG_SESSION_CLASS  XDG_SESSION_ID
XDG_SESSION_TYPE XDG_VTNR
```

### history

> Complete based on a shell's history.

> The argument is an extended regular expression passed to `grep -E`.

```yaml
prog: "example"
options:
  - option_strings: ["--history"]
    complete: ["history", '[a-zA-Z0-9]+@[a-zA-Z0-9]+']
```

```
 ~ > example --history=
foo@bar mymail@myprovider
```

## When Conditionals

Options and Positional Arguments can include a `when` attribute that defines
a *single* condition under which the option (or positional argument) should be
activated.

### has\_option

> Checks if one or more specified options have been provided on the command line.

> **NOTE**: The options used inside the condition have also to be defined as options!

**Examples:**

```yaml
# This activates --conditional if --foo, --bar or --baz are present on the command line

[...]
options:
  - option_strings: ["--conditional"]
    when: "has_option --foo --bar --baz"

  - option_strings: ["--foo", "--bar", "--baz"]
[...]
```

### option\_is

> Checks if one ore more specified options have been set to a specific value.

> **NOTE**: The options used inside the condition have also to be defined as options!

**Example:**

```yaml
# This activates --conditional if --foo, --bar or --baz are set to value1, value2 or value3

[...]
options:
  - option_strings: ["--conditional"]
    when: "option_is --foo --bar --baz -- value1 value2 value3"

  - option_strings: ["--foo", "--bar", "--baz"]
    complete: ["none"]
[...]
```

## Capturing Options

Options can include a `capture` field to store their values for later use.

The value of `capture` is the **name of a variable** that will receive all values passed to that option.

- The captured variable is always an **array**, containing one element for each occurence of the option on the command line.
- This makes it easy to implement **context-sensitive completions** that depend on previously supplied option values

> **NOTE:** There is currently **no automatic check for name clashes** between your capture variables and the parser's internal variables.
> To minimize the risk of conflicts, it is recommended to prefix variable names with `CAPTURE_` or `CAPTURED_`.

> **NOTE:** Captured variables are currently only available in **Bash** and **Zsh**.

**Example:**

```yaml
prog: my_db_tool
options:
  - option_strings: ["--database", "-d"]
    complete: ["choices", ["mysql", "postgres", "sqlite"]]
    capture: "CAPTURED_DB"

  - option_strings: ["--table", "-t"]
    complete: ["exec", "_my_db_tool_complete_table"]
```

For **Bash** and **Zsh**:

```bash
_my_db_tool_complete_table() {
  case "${CAPTURED_DB[-1]}" in
    mysql)    printf '%s\n' users orders products;;
    postgres) printf '%s\n' customers invoices transactions;;
    sqlite)   printf '%s\n' local_cache config sessions;;
  esac
}
```

## Tips and Tricks

It is always recommended to define your command line **as precisely as possible**.
This helps crazy-complete generate reliable completions. Key practices include:
- **Final options**: Use `final: true` for options like `--help` and `--version` that should
  prevent further options from being completed
- **Hidden options**: Use `hidden: true` for options that should be completable but not shown
  in the suggestion list
- **Mutually exclusive options**: Use `groups: [...]` to define sets of options that cannot appear
    together

### Trying out zsh autocompletion scripts

By default, crazy-complete generates scripts that should be installed under `/usr/share/zsh/site-functions`
and loaded from there. If you want to try the generated scripts directly, use `--zsh-compdef=False`.

### Optimizing Script Output

Especially for **Fish** scripts, performance can decrease if many options are defined.
Features like final options and non-repeatable options require extra conditional code to execute, which can make completions slower.

To improve performance these features can be completely disabled using:

```
crazy-complete fish --disable=final,repeatable DEFINITION_FILE
```

This turns off final and repeatable option handling, reducing script size and improving completion speed
