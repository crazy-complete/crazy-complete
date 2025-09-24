Completion Commands
===================

.. contents::
   :local:
   :depth: 1

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Command
     - Description
   * - :ref:`none`
     - No completion, but specifies that an argument is required
   * - :ref:`integer`
     - Complete an integer
   * - :ref:`float`
     - Complete a floating point number
   * - :ref:`combine`
     - Combine multiple completion commands
   * - :ref:`file`
     - Complete a file
   * - :ref:`directory`
     - Complete a directory
   * - :ref:`choices`
     - Complete from a set of values
   * - :ref:`value_list`
     - Complete a list
   * - :ref:`exec`
     - Complete by the output of a command or function
   * - :ref:`exec_fast`
     - Complete by the output of a command or function (fast and unsafe)
   * - :ref:`exec_internal`
     - Complete by a function that uses the shell's internal completion mechanisms
   * - :ref:`range`
     - Complete a range of integers
   * - :ref:`signal`
     - Complete a signal
   * - :ref:`hostname`
     - Complete a hostname
   * - :ref:`process`
     - Complete a process
   * - :ref:`pid`
     - Complete a PID
   * - :ref:`command`
     - Complete a command
   * - :ref:`user`
     - Complete a user
   * - :ref:`group`
     - Complete a group
   * - :ref:`service`
     - Complete a SystemD service
   * - :ref:`variable`
     - Complete a shell variable
   * - :ref:`environment`
     - Complete an environment variable

.. _none:

none
----

Disables autocompletion for this option but still marks it as requiring an argument.

Without specifying ``complete``, the option would not take an argument.

.. code-block:: yaml

   prog: "example"
   options:
     - option_strings: ["--none"]
       complete: ["none"]

.. _integer:

integer
-------

Complete an integer.

**NOTE:** This completion currently serves as documentation and does not provide actual functionality.

If you want to complete a range of integers, see :ref:`range`.

.. code-block:: yaml

   prog: "example"
   options:
     - option_strings: ["--integer"]
       complete: ["integer"]

.. _float:

float
-----

Complete a floating point number.

**NOTE:** This completion currently serves as documentation and does not provide actual functionality.

.. code-block:: yaml

   prog: "example"
   options:
     - option_strings: ["--float"]
       complete: ["float"]

.. _combine:

combine
-------

Combine two or more completion commands.

.. code-block:: yaml

   prog: "example"
   options:
     - option_strings: ["--combine"]
       complete: ["combine", [["user"], ["pid"]]]

.. _file:

file
----

Complete a file.

You can restrict completion to a specific directory by adding ``{"directory": ...}``.

.. code-block:: yaml

   prog: "example"
   options:
     - option_strings: ["--file"]
       complete: ["file"]
     - option_strings: ["--file-tmp"]
       complete: ["file", {"directory": "/tmp"}]

Example:

.. code-block:: console

   $ example --file=<TAB>
   dir1/  dir2/  file1  file2

.. _directory:

directory
---------

Complete a directory.

You can restrict completion to a specific directory by adding ``{"directory": ...}``.

.. code-block:: yaml

   prog: "example"
   options:
     - option_strings: ["--directory"]
       complete: ["directory"]
     - option_strings: ["--directory-tmp"]
       complete: ["directory", {"directory": "/tmp"}]

Example:

.. code-block:: console

   $ example --directory=<TAB>
   dir1/  dir2/

.. _choices:

choices
-------

Complete a list of items.

Items can be a list or a dictionary.

If a dictionary is supplied, the keys are used as items and the values are used
as description.

.. code-block:: yaml

   prog: "example"
   options:
     - option_strings: ["--choices-1"]
       complete: ["choices", ["Item 1", "Item 2"]]
     - option_strings: ["--choices-2"]
       complete: ["choices", {"Item 1": "Description 1", "Item 2": "Description 2"}]

Example:

.. code-block:: console

   $ example --choices-2=<TAB>
   Item 1  (Description 1)  Item 2  (Description 2)

.. _value_list:

value_list
----------

Complete one or more items from a list of items. Similar to ``mount -o``.

Arguments with assignable values (``mount -o uid=1000``) aren't supported.

Arguments are supplied by adding ``{"values": ...}``.

A separator can be supplied by adding ``{"separator": ...}`` (the default is `","`).

.. code-block:: yaml

   prog: "example"
   options:
     - option_strings: ["--value-list-1"]
       complete: ["value_list", {"values": ["exec", "noexec"]}]
     - option_strings: ["--value-list-2"]
       complete: ["value_list", {"values": {"one": "Description 1", "two": "Description 2"}}]

Example:

.. code-block:: console

   $ example --value-list-1=<TAB>
   exec    noexec
   $ example --value-list-1=exec,<TAB>
   exec    noexec
   $ example --value-list-2=<TAB>
   one  -- Description 1
   two  -- Description 2

.. _exec:

exec
----

Execute a command and parse the output.

The output must be in form of::

   <item_1>\t<description_1>\n
   <item_2>\t<description_2>\n
   [...]

An item and its description are delimited by a tabulator.

These pairs are delimited by a newline.

.. code-block:: yaml

   prog: "example"
   options:
     - option_strings: ["--exec"]
       complete: ["exec", "printf '%s\\t%s\\n' 'Item 1' 'Description 1' 'Item 2' 'Description 2'"]

Example:

.. code-block:: console

   $ example --exec=<TAB>
   Item 1  (Description 1)  Item 2  (Description 2)

.. _exec_fast:

exec_fast
---------

Faster version of exec for handling large amounts of data.

This implementation requires that the items of the parsed output do not include
special shell characters or whitespace.

.. code-block:: yaml

   prog: "example"
   options:
     - option_strings: ["--exec-fast"]
       complete: ["exec_fast", "printf '%s\\t%s\\n' 1 one 2 two"]

.. _exec_internal:

exec_internal
-------------

Execute a function that internally modifies the completion state.

This is useful if a more advanced completion is needed.

.. code-block:: yaml

   prog: "example"
   options:
     - option_strings: ["--exec-internal"]
       complete: ["exec_internal", "my_completion_func"]

Examples:

Bash::

   my_completion_func() {
       COMPREPLY=( $(compgen -W "foo bar baz") )
   }

Zsh::

   my_completion_func() {
       local items=( foo bar baz )
       _describe '' items
   }

Fish::

   function my_completion_func
       printf '%s\n' foo bar baz
   end

.. _range:

range
-----

Complete a range of integers.

.. code-block:: yaml

   prog: "example"
   options:
     - option_strings: ["--range-1"]
       complete: ["range", 1, 9]
     - option_strings: ["--range-2"]
       complete: ["range", 1, 9, 2]

Example:

.. code-block:: console

   $ example --range-1=<TAB>
   1  2  3  4  5  6  7  8  9
   $ example --range-2=<TAB>
   1  3  5  7  9

.. _signal:

signal
------

Complete signal names (INT, KILL, TERM, etc.).

.. code-block:: yaml

   prog: "example"
   options:
     - option_strings: ["--signal"]
       complete: ["signal"]

Example:

.. code-block:: console

   $ example --signal=<TAB>
   ABRT    -- Process abort signal
   ALRM    -- Alarm clock
   BUS     -- Access to an undefined portion of a memory object
   [...]

.. _hostname:

hostname
--------

Complete a hostname.

.. code-block:: yaml

   prog: "example"
   options:
     - option_strings: ["--hostname"]
       complete: ["hostname"]

Example:

.. code-block:: console

   $ example --hostname=<TAB>
   localhost

.. _process:

process
-------

Complete a process name.

.. code-block:: yaml

   prog: "example"
   options:
     - option_strings: ["--process"]
       complete: ["process"]

Example:

.. code-block:: console

   $ example --process=s<TAB>
   scsi_eh_0   scsi_eh_1  sudo  systemd  [...]

.. _pid:

pid
---

Complete a PID.

.. code-block:: yaml

   prog: "example"
   options:
     - option_strings: ["--pid"]
       complete: ["pid"]

Example:

.. code-block:: console

   $ example --pid=<TAB>
   1  13  166  19  [...]

.. _command:

command
-------

Complete a command.

.. code-block:: yaml

   prog: "example"
   options:
     - option_strings: ["--command"]
       complete: ["command"]

Example:

.. code-block:: console

   $ example --command=bas<TAB>
   base32  base64  basename  basenc  bash  bashbug

.. _user:

user
----

Complete a username.

.. code-block:: yaml

   prog: "example"
   options:
     - option_strings: ["--user"]
       complete: ["user"]

Example:

.. code-block:: console

   $ example --user=<TAB>
   avahi  bin  braph  [...]

.. _group:

group
-----

Complete a group.

.. code-block:: yaml

   prog: "example"
   options:
     - option_strings: ["--group"]
       complete: ["group"]

Example:

.. code-block:: console

   $ example --group=<TAB>
   adm  audio  avahi  [...]

.. _service:

service
-------

Complete a SystemD service.

.. code-block:: yaml

   prog: "example"
   options:
     - option_strings: ["--service"]
       complete: ["service"]

Example:

.. code-block:: console

   $ example --service=<TAB>
   TODO

.. _variable:

variable
--------

Complete a shell variable name.

To complete an environment variable, use :ref:`environment`.

.. code-block:: yaml

   prog: "example"
   options:
     - option_strings: ["--variable"]
       complete: ["variable"]

Example:

.. code-block:: console

   $ example --variable=HO<TAB>
   HOME  HOSTNAME  HOSTTYPE

.. _environment:

environment
-----------

Complete a shell environment variable name.

.. code-block:: yaml

   prog: "example"
   options:
     - option_strings: ["--environment"]
       complete: ["environment"]

Example:

.. code-block:: console

   $ example --environment=X<TAB>
   XDG_RUNTIME_DIR  XDG_SESSION_TYPE  [...]
