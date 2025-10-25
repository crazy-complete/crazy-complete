### Meta commands

| Command                             | Description                                               |
| ----------------------------------- | --------------------------------------------------------- |
| [combine](#combine)                 | Combine multiple completers                               |
| [key\_value\_list](#key_value_list) | Complete a comma-separated list of key=value pairs        |
| [list](#list)                       | Complete a comma-separated list using a completer         |
| [none](#none)                       | No completion, but specifies that an argument is required |

### Built-in commands

| Command                                    | Description                                    |
| ------------------------------------------ | ---------------------------------------------- |
| [choices](#choices)                        | Complete from a set of words                   |
| [command](#command)                        | Complete a command                             |
| [command\_arg](#command_arg)               | Complete arguments of a command                |
| [commandline\_string](#commandline_string) | Complete a command line as a string            |
| [date](#date)                              | Complete a date string                         |
| [date\_format](#date_format)               | Complete a date format string                  |
| [directory](#directory)                    | Complete a directory                           |
| [directory\_list](#directory_list)         | Complete a comma-separated list of directories |
| [environment](#environment)                | Complete a shell environment variable name     |
| [file](#file)                              | Complete a file                                |
| [file\_list](#file_list)                   | Complete a comma-separated list of files       |
| [filesystem\_type](#filesystem_type)       | Complete a filesystem type                     |
| [float](#float)                            | Complete floating point number                 |
| [gid](#gid)                                | Complete a group id                            |
| [group](#group)                            | Complete a group                               |
| [history](#history)                        | Complete based on a shell's history            |
| [hostname](#hostname)                      | Complete a hostname                            |
| [integer](#integer)                        | Complete an integer                            |
| [mime\_file](#mime_file)                   | Complete a file based on it's MIME-type        |
| [pid](#pid)                                | Complete a PID                                 |
| [process](#process)                        | Complete a process name                        |
| [range](#range)                            | Complete a range of integers                   |
| [service](#service)                        | Complete a SystemD service                     |
| [signal](#signal)                          | Complete signal names                          |
| [uid](#uid)                                | Complete a user id                             |
| [user](#user)                              | Complete a username                            |
| [value\_list](#value_list)                 | Complete a list of values                      |
| [variable](#variable)                      | Complete a shell variable name                 |

### User-defined commands

| Command                          | Description                                                                 |
| -------------------------------- | --------------------------------------------------------------------------- |
| [exec](#exec)                    | Complete by the output of a command or function                             |
| [exec\_fast](#exec_fast)         | Complete by the output of a command or function (fast and unsafe)           |
| [exec\_internal](#exec_internal) | Complete by a function that uses the shell's internal completion mechanisms |

### Bonus commands

| Command                          | Description                  |
| -------------------------------- | ---------------------------- |
| [alsa\_card](#alsa_card)         | Complete an ALSA card        |
| [alsa\_device](#alsa_device)     | Complete an ALSA device      |
| [charset](#charset)              | Complete a charset           |
| [locale](#locale)                | Complete a locale            |
| [login\_shell](#login_shell)     | Complete a login shell       |
| [mountpoint](#mountpoint)        | Complete a mountpoint        |
| [net\_interface](#net_interface) | Complete a network interface |
| [timezone](#timezone)            | Complete a timezone          |

### alsa\_card

> Complete an ALSA card

```yaml
prog: "example"
options:
  - option_strings: ["--alsa-card"]
    complete: ["alsa_card"]
```

```
~ > example --alsa-card=<TAB>
0  1
```

**SEE ALSO**

- [alsa\_device](#alsa_device): For completing an ALSA device

### alsa\_device

> Complete an ALSA device

```yaml
prog: "example"
options:
  - option_strings: ["--alsa-device"]
    complete: ["alsa_device"]
```

```
~ > example --alsa-device=<TAB>
hw:0  hw:1
```

**SEE ALSO**

- [alsa\_card](#alsa_card): For completing an ALSA card

### charset

> Complete a charset

```yaml
prog: "example"
options:
  - option_strings: ["--charset"]
    complete: ["charset"]
```

```
~ > example --charset=A<TAB>
ANSI_X3.110-1983  ANSI_X3.4-1968    ARMSCII-8         ASMO_449
```

### locale

> Complete a locale

```yaml
prog: "example"
options:
  - option_strings: ["--locale"]
    complete: ["locale"]
```

```
~ > example --locale=<TAB>
C  C.UTF-8  de_DE  de_DE@euro  de_DE.iso88591  de_DE.iso885915@euro
de_DE.UTF-8  deutsch  en_US  en_US.iso88591  en_US.UTF-8  german  POSIX
```

### login\_shell

> Complete a login shell

```yaml
prog: "example"
options:
  - option_strings: ["--login-shell"]
    complete: ["login_shell"]
```

```
~ > example --login-shell=<TAB>
/bin/bash   /bin/sh         /usr/bin/fish       /usr/bin/sh
[...]
```

### mountpoint

> Complete a mountpoint

```yaml
prog: "example"
options:
  - option_strings: ["--mountpoint"]
    complete: ["mountpoint"]
```

```
~ > example --mountpoint=<TAB>
/  /boot  /home  /proc  /run  /sys  /tmp
[...]
```

### net\_interface

> Complete a network interface

```yaml
prog: "example"
options:
  - option_strings: ["--net-interface"]
    complete: ["net_interface"]
```

```
~ > example --net-interface=<TAB>
eno1  enp1s0  lo  wlo1  wlp2s0
[...]
```

### timezone

> Complete a timezone

```yaml
prog: "example"
options:
  - option_strings: ["--timezone"]
    complete: ["timezone"]
```

```
~ > example --timezone=Europe/B<TAB>
Belfast     Belgrade    Berlin      Bratislava
Brussels    Bucharest   Budapest    Busingen
```

### choices

> Complete from a set of words

Items can be a list or a dictionary.
 
If a dictionary is supplied, the keys are used as items and the values are used
as description.


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

### command

> Complete a command

This completer provides completion suggestions for executable commands available in the system's `$PATH`.
 
`$PATH` can be modified using these options:
 
`{"path": "<directory>:..."}`: Overrides the default `$PATH` entirely.
 
`{"path_append": "<directory>:..."}`: Appends to the default `$PATH`.
 
`{"path_prepend": "<directory>:..."}`: Prepends to the default `$PATH`.


**NOTES**

- `path_append` and `path_prepend` can be used together, but both are mutually exclusive with `path`.

```yaml
prog: "example"
options:
  - option_strings: ["--command"]
    complete: ["command"]
  - option_strings: ["--command-sbin"]
    complete: ["command", {"path_append": "/sbin:/usr/sbin"}]
```

```
~ > example --command=bas<TAB>
base32    base64    basename  basenc    bash      bashbug
```

**SEE ALSO**

- [command\_arg](#command_arg): For completing arguments of a command

- [commandline\_string](#commandline_string): For completing a command line as a string

### command\_arg

> Complete arguments of a command

**NOTES**

- This completer can only be used in combination with a previously defined `command` completer.

- This completer requires `repeatable: true`.

```yaml
prog: "example"
positionals:
  - number: 1
    complete: ["command"]

  - number: 2
    complete: ["command_arg"]
    repeatable: true
```

```
~ > example sudo bas<TAB>
base32    base64    basename  basenc    bash      bashbug
```

**SEE ALSO**

- [command](#command): For completing a command

- [commandline\_string](#commandline_string): For completing a command line as a string

### commandline\_string

> Complete a command line as a string

```yaml
prog: "example"
options:
  - option_strings: ["--commandline"]
    complete: ["commandline_string"]
```

```
~ > example --commandline='sudo ba<TAB>
base32    base64    basename  basenc    bash      bashbug
```

### date

> Complete a date string

The argument is the date format as described in `strftime(3)`.


**NOTES**

- This completer is currently only implemented in **Zsh**.

```yaml
prog: "example"
options:
  - option_strings: ["--date"]
    complete: ["date", '%Y-%m-%d']
```

```
~ > example --date=<TAB>

         November                        
Mo  Tu  We  Th  Fr  Sa  Su     
     1   2   3   4   5   6    
 7   8   9  10  11  12  13
14  15  16  17  18  19  20
21  22  23  24  25  26  27
28  29  30
```

**SEE ALSO**

- [date\_format](#date_format): For completing a date format string

### date\_format

> Complete a date format string

**NOTES**

- This completer is currently only implemented in **Fish** and **Zsh**.

```yaml
prog: "example"
options:
  - option_strings: ["--date-format"]
    complete: ["date_format"]
```

```
~ > example --date-format '%<TAB>
a     -- abbreviated day name
A     -- full day name
B     -- full month name
c     -- preferred locale date and time
C     -- 2-digit century
d     -- day of month (01-31)
D     -- American format month/day/year (%m/%d/%y)
e     -- day of month ( 1-31)
[...]
```

**SEE ALSO**

- [date](#date): For completing a date

### directory

> Complete a directory

You can restrict completion to a specific directory by adding `{"directory": ...}`.


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

**SEE ALSO**

- [directory\_list](#directory_list): For completing a list of directories

### directory\_list

> Complete a comma-separated list of directories

This is an alias for `['list', ['directory']]`.

You can restrict completion to a specific directory by adding `{"directory": ...}`. Directory has to be an absolute path.
 
The separator can be changed by adding `{"separator": ...}`
 
By default, duplicate values are not offered for completion. This can be changed by adding `{"duplicates": true}`.


```yaml
prog: "example"
options:
  - option_strings: ["--directory-list"]
    complete: ["directory_list"]
```

```
~ > example --directory-list=directory1,directory2,<TAB>
directory3  directory4
```

### environment

> Complete a shell environment variable name

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

### file

> Complete a file

You can restrict completion to a specific directory by adding `{"directory": ...}`. Directory has to be an absolute path.
 
You can restrict completion to specific extensions by adding `{"extensions": [...]}`.
 
You can make matching extensions *fuzzy* by adding `{"fuzzy": true}`.
Fuzzy means that the files do not have to end with the exact extension. For example `foo.txt.1`.
 
**NOTE:** Restricting completion to specific file extensions only makes sense if the program being completed actually expects files of those types.
On Unix-like systems, file extensions generally have no inherent meaning -- they are purely conventional and not required for determining file types.


```yaml
prog: "example"
options:
  - option_strings: ["--file"]
    complete: ["file"]
  - option_strings: ["--file-tmp"]
    complete: ["file", {"directory": "/tmp"}]
  - option_strings: ["--file-ext"]
    complete: ["file", {"extensions": ["c", "cpp"]}]
```

```
~ > example --file=<TAB>
dir1/  dir2/  file1  file2
~ > example --file-ext=<TAB>
dir1/  dir2/  file.c  file.cpp
```

**SEE ALSO**

- [file\_list](#file_list): For completing a list of files

- [mime\_file](#mime_file): For completing a file based on it's MIME-type

### file\_list

> Complete a comma-separated list of files

This is an alias for `['list', ['file']]`.

You can restrict completion to a specific directory by adding `{"directory": ...}`.
 
You can restrict completion to specific extensions by adding `{"extensions": [...]}`.
 
You can make matching extensions *fuzzy* by adding `{"fuzzy": true}`.
Fuzzy means that the files do not have to end with the exact extension. For example `foo.txt.1`.
 
By default, duplicate values are not offered for completion. This can be changed by adding `{"duplicates": true}`.

The separator can be changed by adding `{"separator": ...}`


```yaml
prog: "example"
options:
  - option_strings: ["--file-list"]
    complete: ["file_list"]
```

```
~ > example --file-list=file1,file2,<TAB>
file3  file4
```

### filesystem\_type

> Complete a filesystem type

```yaml
prog: "example"
options:
  - option_strings: ["--filesystem-type"]
    complete: ["filesystem_type"]
```

```
~ > example --filesystem-type=<TAB>
adfs     autofs   bdev      bfs     binder     binfmt_misc  bpf
cgroup   cgroup2  configfs  cramfs  debugfs    devpts       devtmpfs
```

### float

> Complete floating point number

**NOTES**

- This completer currently serves as documentation and does not provide actual functionality.

```yaml
prog: "example"
options:
  - option_strings: ["--float"]
    complete: ["float"]
```

```
~ > example --float=<TAB>
<NO OUTPUT>
```

### gid

> Complete a group id

```yaml
prog: "example"
options:
  - option_strings: ["--gid"]
    complete: ["gid"]
```

```
~ > example --gid=<TAB>
0      -- root
1000   -- braph
102    -- polkitd
108    -- vboxusers
11     -- ftp
12     -- mail
133    -- rtkit
19     -- log
[...]
```

**SEE ALSO**

- [group](#group): For completing a group name

### group

> Complete a group

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

**SEE ALSO**

- [gid](#gid): For completing a group id

### history

> Complete based on a shell's history

The argument is an extended regular expression passed to `grep -E`.


```yaml
prog: "example"
options:
  - option_strings: ["--history"]
    complete: ["history", '[a-zA-Z0-9]+@[a-zA-Z0-9]+']
```

```
~ > example --history=<TAB>
foo@bar mymail@myprovider
```

### hostname

> Complete a hostname

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

### integer

> Complete an integer

**NOTES**

- This completer currently serves as documentation and does not provide actual functionality.

```yaml
prog: "example"
options:
  - option_strings: ["--integer"]
    complete: ["integer"]
```

```
~ > example --integer=<TAB>
<NO OUTPUT>
```

**SEE ALSO**

- [range](#range): For completing a range of integers

### mime\_file

> Complete a file based on it's MIME-type

This completer takes an extended regex passed to `grep -E` to filter the results.


```yaml
prog: "example"
options:
  - option_strings: ["--image"]
    complete: ["mime_file", 'image/']
```

```
~ > example --image=<TAB>
dir1/  dir2/  img.png  img.jpg
```

### pid

> Complete a PID

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

**SEE ALSO**

- [process](#process): For completing a process name

### process

> Complete a process name

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

**SEE ALSO**

- [pid](#pid): For completing a PID

### range

> Complete a range of integers

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

### service

> Complete a SystemD service

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

### signal

> Complete signal names

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

### uid

> Complete a user id

```yaml
prog: "example"
options:
  - option_strings: ["--uid"]
    complete: ["uid"]
```

```
~ > example --uid=<TAB>
0      -- root
1000   -- braph
102    -- polkitd
133    -- rtkit
14     -- ftp
1      -- bin
2      -- daemon
33     -- http
65534  -- nobody
[...]
```

**SEE ALSO**

- [user](#user): For completing a user name

### user

> Complete a username

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

**SEE ALSO**

- [uid](#uid): For completing a user id

### value\_list

> Complete a list of values

Complete one or more items from a list of items. Similar to `mount -o`.
 
Arguments with assignable values (`mount -o uid=1000`) aren't supported.
 
Arguments are supplied by adding `{"values": ...}`.
 
A separator can be supplied by adding `{"separator": ...}` (the default is `","`).
 
By default, duplicate values are not offered for completion. This can be changed by adding `{"duplicates": true}`.


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
noexec
~ > example --value-list-2=<TAB>
one  -- Description 1
two  -- Description 2
```

**SEE ALSO**

- [key\_value\_list](#key_value_list): For completing a comma-separated list of key=value pairs

### variable

> Complete a shell variable name

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

**SEE ALSO**

- [environment](#environment): For completing an environment variable

### combine

> Combine multiple completers

With `combine` multiple completers can be combined into one.

It takes a list of completers as its argument.


```yaml
prog: "example"
options:
  - option_strings: ["--combine"]
    complete: ["combine", [["user"], ["pid"]]]
```

```
~ > example --user-list=avahi,daemon,<TAB>
1439404  3488332  3571716           3607235                 4134206
alpm     avahi    bin               braph                   daemon
root     rtkit    systemd-coredump  systemd-journal-remote  systemd-network
[...]
```

### key\_value\_list

> Complete a comma-separated list of key=value pairs

The first argument is the separator used for delimiting the key-value pairs.

The second argument is the separator used for delimiting the value from the key.

The third argument is either a dictionary or a list.

The dictionary has to be in the form of:

  `{<key>: <completer>, ...}`

The list has to be in the form of:

  `[ [<key>, <description>, <completer>], ... ]`

If a key does not take an argument, use `null` as completer.

If a key does take an argument but cannot be completed, use `['none']` as completer.


```yaml
prog: "example"
options:
  - option_strings: ["--key-value-list"]
    complete: ["key_value_list", ",", "=", {
      'flag':   null,
      'nocomp': ['none'],
      'user':   ['user'],
      'check':  ['choices', {
        'relaxed': "convert to lowercase before lookup",
        'strict': "no conversion"
      }]
    }]

  - option_strings: ["--key-value-list-with-desc"]
    complete: ["key_value_list", ",", "=", [
      ['flag',   'An option flag', null],
      ['nodesc', null, null],
      ['nocomp', 'An option with arg but without completer', ['none']],
      ['user',   'Takes a username',  ['user']],
      ['check',  'Specify file name conversions', ['choices', {
        'relaxed': "convert to lowercase before lookup",
        'strict': "no conversion"
      }]]
    ]]
```

```
~ > example --key-value-list flag,user=<TAB>
bin                     braph
colord                  dbus
dhcpcd                  git
```

### list

> Complete a comma-separated list using a completer

Complete a comma-separated list of any completer.

The separator can be changed by adding `{"separator": ...}`.

By default, duplicate values are not offered for completion. This can be changed by adding `{"duplicates": true}`.


```yaml
prog: "example"
options:
  - option_strings: ["--user-list"]
    complete: ["list", ["user"]]
  - option_strings: ["--option-list"]
    complete: ["list", ["choices", ["setuid", "async", "block"]], {"separator": ":"}]
```

```
~ > example --user-list=avahi,daemon,<TAB>
bin                     braph
colord                  dbus
dhcpcd                  git
```

**SEE ALSO**

- [key\_value\_list](#key_value_list): For completing a list of key=value pairs

- [file\_list](#file_list): For completing a list of files

- [directory\_list](#directory_list): For completing a list of directories

### none

> No completion, but specifies that an argument is required

Disables autocompletion for this option but still marks it as requiring an argument.

Without specifying `complete`, the option would not take an argument.


```yaml
prog: "example"
options:
  - option_strings: ["--none"]
    complete: ["none"]
```

```
~ > example --none=<TAB>
<NO OUTPUT>
```

### exec

> Complete by the output of a command or function

The output must be in form of:

```
<item_1>\t<description_1>\n
<item_2>\t<description_2>\n
[...]
```

An item and its description are delimited by a tabulator.
 
These pairs are delimited by a newline.


**NOTES**

- Functions can be put inside a file and included with `--include-file`

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

**SEE ALSO**

- [exec\_fast](#exec_fast): Faster implementation of exec

### exec\_fast

> Complete by the output of a command or function (fast and unsafe)

Faster version of exec for handling large amounts of data.
 
This implementation requires that the items of the parsed output do not include
special shell characters or whitespace.


**NOTES**

- Functions can be put inside a file and included with `--include-file`

```yaml
prog: "example"
options:
  - option_strings: ["--exec-fast"]
    complete: ["exec_fast", "printf '%s\\t%s\\n' 1 one 2 two"]
```

```
~ > example --exec-internal=<TAB>
1  -- one
2  -- one
```

### exec\_internal

> Complete by a function that uses the shell's internal completion mechanisms

Execute a function that internally modifies the completion state.

This is useful if a more advanced completion is needed.

For **Bash**, it might look like:

```sh
my_completion_func() {
    COMPREPLY=( $(compgen -W "read write append" -- "$cur") )
}
```

For **Zsh**, it might look like:

```sh
my_completion_func() {
    local items=(
        read:'Read data from a file'
        write:'Write data from a file'
        append:'Append data to a file'
    )

    _describe 'my items' items
}
```

For **Fish**, it might look like:

```sh
function my_completion_func
    printf '%s\t%s\n' \
        read 'Read data from a file'  \
        write 'Write data from a file' \
        append 'Append data to a file'
end
```


**NOTES**

- Functions can be put inside a file and included with `--include-file`

```yaml
prog: "example"
options:
  - option_strings: ["--exec-internal"]
    complete: ["exec_internal", "my_completion_func"]
```

```
~ > example --exec-internal=<TAB>
append  -- Append data to a file
read    -- Read data from a file
write   -- Write data from a file
```