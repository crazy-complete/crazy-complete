Completion commands
===================

**none**

> Do not add any completion code.
> This is the default.

```yaml
prog: "example"
options:
  - option_strings: ["--none"]
    complete: ["none"]
```

**file**

> Complete a file.
> A directory can be supplied by adding {"directory": ...}

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

**directory**

> Complete a directory.
> A directory can be supplied by adding {"directory": ...}

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

**choices**

> Complete a list of items. Items can be a list or a dictionary.
> If a dictionary is supplied, the keys are used as items and the values are used
> as description.

```yaml
prog: "example"
options:
  - option_strings: ["--choices1"]
    complete: ["choices", ["Item 1", "Item 2"]]
  - option_strings: ["--choices2"]
    complete: ["choices", {"Item 1": "Description 1", "Item 2": "Description 2"}]
```

```
 ~ > example --choices2=<TAB>
Item 1  (Description 1)  Item 2  (Description 2)
```

**value_list**

> Complete one or more items from a list of items. Similar to `mount -o`.
> Arguments with assignable values (`mount -o uid=1000`) aren't supported.
> Arguments are supplied by adding {"values": ...}
> A separator can be supplied by adding {"separator": ...} (the default is ",")

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

**exec**

> Execute commandline and parse the output.
> The output must be in form of:
```
<item_1>\t<description_1>\n
<item_2>\t<description_2>\n
[...]
```
> An item and its description are delimited by a tabulator.
> These pairs are delimited by a newline.

```yaml
prog: "example"
options:
  - option_strings: ["--exec"]
    complete: ["exec", "printf '%s\\t%s\\n' 'Item 1' 'Description 2' 'Item 2' 'Description 2'"]
```

```
 ~ > example --exec=<TAB>
Item 1  (Description 1)  Item 2  (Description 2)
```

**exec_fast**

> Faster version of exec for handling large amounts of data.
> This implementation requires that the items of the parsed output do not include
> special shell characters or whitespace.

**range**

> Complete a range of integers.

```yaml
prog: "example"
options:
  - option_strings: ["--range-1"]
    complete: ["range", 1, 9]
  - option_strings: ["--range-2"]
    complete: ["range", 1, 9]
```

```
 ~ > example --range-1=<TAB>
1  2  3  4  5  6  7  8  9
 ~ > example --range-2=<TAB>
1  3  5  7  9
```

**signal**

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

**process**

> List process names.

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

**pid**

> List PIDs.

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

**command**

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

**user**

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

**group**

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

**service**

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

**variable**

> Complete a shell variable name.
> To complete a environment variable, use **environment**.

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

**environment**

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
