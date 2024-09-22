Commands
========

**Note**

> All code examples start with:

```
import argparse

from crazy_complete import argparse_mod
```

**none()**

> Do not add any completion code.
> Note: This is the default.

```
argp = argparse.ArgumentParser('foo')
argp.add_argument('--none').complete('none')
# This line is the same as above:
argp.add_argument('--none2')
```

**file(opts={})**

> Complete a file.
> If opts['directory'] is given, list files in opts['directory'].

```
argp = argparse.ArgumentParser('foo')
argp.add_argument('--file').complete('file')
argp.add_argument('--file-tmp').complete('file', {'directory': '/tmp'})

 ~ > foo --file=<TAB>
 dir1/  dir2/  file1  file2
```

**directory(opts={})**

> Complete a directory.
> If opts['directory'] is given, list directories in opts['directory'].

```
argp = argparse.ArgumentParser('foo')
argp.add_argument('--directory').complete('directory')
argp.add_argument('--directory-tmp').complete('directory', {'directory': '/tmp'})

 ~ > foo --directory=<TAB>
 dir1/  dir2/
```

**choices(items)**

> Complete a list of items or a dictionary in the form `{item: description}`.

```
argp = argparse.ArgumentParser('foo')
argp.add_argument('--choices1').complete('choices', ['Item 1', 'Item 2'])
argp.add_argument('--choices2').complete('choices', {'Item 1': 'Description 1', 'Item 2': 'Description 2'})
# These lines produce the same
argp.add_argument('--choices1', choices=['Item 1', 'Item 2'])
argp.add_argument('--choices2', choices={'Item 1': 'Description 1', 'Item 2': 'Description 2'})

 ~ > foo --choices2=<TAB>
Item 1  (Description 1)  Item 2  (Description 2)
```

**exec(commandline)**

> Execute commandline and parse the output.
> The output must be in form of:
```
<item_1>\t<description_1>\n
<item_2>\t<description_2>\n
[...]
```
> An item and its description are delimited by a tabulator.
> These pairs are delimited by a newline.

```
argp = argparse.ArgumentParser('foo')
argp.add_argument('--exec').complete('exec', 'printf "%s\\t%s\\n" "Item 1" "Description 1" "Item 2" "Description 2"')

 ~ > foo --exec=<TAB>
Item 1  (Description 1)  Item 2  (Description 2)
```

**range(start, stop, step=1)**

> Complete a range of integers.

```
argp = argparse.ArgumentParser('foo')
argp.add_argument('--range').complete('range', 1, 9, 2)

 ~ > foo --range=<TAB>
1  3  5  7  9
```

**signal()**

> Complete signal names (INT, KILL, TERM, etc.).

```
argp = argparse.ArgumentParser('foo')
argp.add_argument('--signal').complete('signal')

 ~ > foo --signal=<TAB>
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

**process()**

> List process names.

```
argp = argparse.ArgumentParser('foo')
argp.add_argument('--process').complete('process')

 ~ > foo --process=s<TAB>
scsi_eh_0         scsi_eh_1       scsi_eh_2      scsi_eh_3  scsi_eh_4
scsi_eh_5         sh              sudo           syndaemon  systemd
systemd-journald  systemd-logind  systemd-udevd
```

**pid()**

> List PIDs.

```
argp = argparse.ArgumentParser('foo')
argp.add_argument('--pid').complete('pid')

 ~ > foo --pid=<TAB>
1       13      166     19      254     31      45
1006    133315  166441  19042   26      32      46
10150   1392    166442  195962  27      33      4609
```

**command()**

> Complete a command.

```
argp = argparse.ArgumentParser('foo')
argp.add_argument('--command').complete('command')

 ~ > foo --command=bas<TAB>
base32    base64    basename  basenc    bash      bashbug
```

**user()**

> Complete a username.

```
argp = argparse.ArgumentParser('foo')
argp.add_argument('--user').complete('user')

 ~ > foo --user=<TAB>
avahi                   bin                     braph
colord                  daemon                  dbus
dhcpcd                  ftp                     git
[...]
```

**group()**

> Complete a group.

```
argp = argparse.ArgumentParser('foo')
argp.add_argument('--group').complete('group')

 ~ > foo --group=<TAB>
adm                     audio                   avahi
bin                     braph                   colord
daemon                  dbus                    dhcpcd
disk                    floppy                  ftp
games                   git                     groups
[...]
```

**service()**

> Complete a SystemD service.

```
argp = argparse.ArgumentParser('foo')
argp.add_argument('--service').complete('service')

 ~ > foo --service=<TAB>
TODO
[...]
```

**variable()**

> Complete a shell variable name.

```
argp = argparse.ArgumentParser('foo')
argp.add_argument('--variable').complete('variable')

 ~ > foo --variable=HO<TAB>
HOME      HOSTNAME  HOSTTYPE
```
