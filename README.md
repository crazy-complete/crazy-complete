crazy-complete
==============

Every program should have autocompletion in the shell to enhance user experience and productivity. crazy-complete helps solve this task by generating robust and reliable autocompletion scripts.

**Key Features**:
- **Generates Robust Scripts**: Ensures that the autocompletion scripts are reliable and efficient.
- **Multi-Shell Support**: Works seamlessly with Bash, Fish, and Zsh, providing flexibility across different environments.
- **Minimal Dependencies**: The only external dependency is PyYAML.
- **Configurable and Extendable**: The generated autocompletion scripts are highly configurable and can be easily extended to suit your specific needs.
- **Standalone Scripts**: The generated scripts are standalone and do not depend on modified environments, unlike some alternatives like argcomplete.
- **Easy to Use**: Simple and intuitive to set up, allowing you to quickly add autocompletion functionality to your programs.

With crazy-complete, adding autocompletion to your programs has never been easier. Try it out and see the difference it makes in your command-line applications!

Installation
============

- Using Arch Linux:

  Use the \*.pkg.tar.zst file that has been released in this repository.

  Or use:
  ```
  git clone https://github.com/crazy-complete/crazy-complete
  cd crazy-complete
  makepkg -c && sudo pacman -U python-crazy-complete*.pkg.*
  ```

- Using Debian:

  Use the \*.deb file that has been released in this repository.

- Using Fedora / OpenSuse:

  Use the \*.rpm file that has been released in this repository.

- For other Linux distributions:
  ```
  git clone https://github.com/crazy-complete/crazy-complete
  cd crazy-complete
  python3 -m pip install .
  ```

Synopsis
========

> `crazy-complete [OPTIONS] {bash,fish,zsh,yaml,json} <DEFINITION_FILE>`

Options
=======

**--input-type={yaml,json,python,help,auto}**

> Specify input file type. With 'auto' the file extension will be used
> to determine the input type.

**--abbreviate-commands={True,False}**

> Sets whether commands can be abbreviated.

**--abbreviate-options={True,False}**

> Sets whether options can be abbreviated.
> Note: abbreviated options are not supported by FISH and ZSH.

**--repeatable-options={True,False}**

> Sets whether options are suggested multiple times during completion.

**--inherit-options={True,False}**

> Sets whether parent options are visible to subcommands.

**--vim-modeline={True,False}**

> Sets whether a vim modeline comment shall be appended to the generated code.

**--include-file=FILE**

> Include contents of FILE in output.

**-o|--output=FILE**

> Write output to destination file [default: stdout].

**-i|--install-system-wide**

> Write output to the system-wide completions dir of shell.

**-u|--uninstall-system-wide**

> Uninstall the system-wide completion file for program.

Completions for crazy-complete
==============================

To install system-wide completion files for crazy-complete, execute the following:

```
sudo crazy-complete --input-type=python -i bash "$(which crazy-complete)"
sudo crazy-complete --input-type=python -i fish "$(which crazy-complete)"
sudo crazy-complete --input-type=python -i zsh  "$(which crazy-complete)"
```

If you want to uninstall the completion files, pass `-u` to crazy-complete:

```
sudo crazy-complete --input-type=python -u bash "$(which crazy-complete)"
sudo crazy-complete --input-type=python -u fish "$(which crazy-complete)"
sudo crazy-complete --input-type=python -u zsh  "$(which crazy-complete)"
```

Usage examples
==============

Converting a Python script to YAML:

```
crazy-complete --input-type=python yaml my_program.py
```

Generate a YAML file from help text:

```
grep --help > help_file
crazy-complete --input-type=help yaml help_file
- or -
grep --help | crazy-complete --input-type=help yaml /dev/stdin
```

Generate shell auto completions for BASH:

```
crazy-complete --input-type=yaml --include my_program.bash bash my_program.yaml
```

Definition file examples
========================

See [examples](https://github.com/crazy-complete/crazy-complete/tree/main/examples) for examples.

See [completions](https://github.com/crazy-complete/crazy-complete/tree/main/completions) for real world applications of crazy-complete.

You can even have a look at the [tests](https://github.com/crazy-complete/crazy-complete/tree/main/test).

Documentation
=============

See [documentation.md](https://github.com/crazy-complete/crazy-complete/blob/main/documentation.md) and [commands.md](https://github.com/crazy-complete/crazy-complete/blob/main/commands.md).

Comparision with other auto-complete generators
===============================================

See [comparision](https://github.com/crazy-complete/crazy-complete/blob/main/comparision.md) for a comparision with other tools.

Questions or problems
=====================

Don't hesitate to open an issue on [GitHub](https://github.com/crazy-complete/crazy-complete/issues).
