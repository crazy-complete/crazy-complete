crazy-complete
==============

Every program should have autocompletion in the shell to enhance user experience and productivity. crazy-complete helps solve this task by generating robust and reliable autocompletion scripts.

**Key Features**:
- **Generates Robust Scripts**: Ensures that the autocompletion scripts are reliable and efficient.
- **Multi-Shell Support**: Works seamlessly with **Bash**, **Fish**, and **Zsh**, providing flexibility across different environments.
- **Minimal Dependencies**: The only external dependency is PyYAML.
- **Configurable and Extendable**: The generated autocompletion scripts are highly configurable and can be easily extended to suit your specific needs.
- **Standalone Scripts**: The generated scripts are standalone and do not depend on modified environments, unlike some alternatives like argcomplete.
- **Easy to Use**: Simple and intuitive to set up, allowing you to quickly add autocompletion functionality to your programs.

With crazy-complete, adding autocompletion to your programs has never been easier. Try it out and see the difference it makes in your command-line applications!

Table of Contents
=================

- [Benefits of Using crazy-complete](#benefits-of-using-crazy-complete)
- [Disadvantages of crazy-complete](#disadvantages-of-crazy-complete)
- [Installation](#installation)
- [Synposis](#synopsis)
- [Usage examples](#usage-examples)
- [Definition file examples](#definition-file-examples)
- [Documentation](#documentation)
- [Comparision with other auto-complete generators](#comparision-with-other-auto-complete-generators)
- [Questions or problems](#questions-or-problems)

Benefits of Using crazy-complete
================================

- **Focus on what matters:**
  crazy-complete generates the basic structure of your autocompletion scripts,
  so you can focus entirely on defining options and their completions instead of dealing with repetitive setup code.

- **Cross-shell consistency:**
  Write your completion logic once and get reliable completions for **Bash**, **Zsh**, and **Fish**, with identical behavior across all shells.

- **Powerful argument completion:**
  crazy-complete provides a rich set of [built-in](docs/documentation.md#built-in-commands) helpers for argument completion and makes it simple to define your own [custom argument handlers](docs/documentation.md#user-defined-commands).

- **Arbitrary levels of subcommands:**
  No matter how deeply nested your CLI structure is, crazy-complete can handle it.
  You can define completions for commands, subcommands, and even sub-subcommands without extra effort.

- **Full control over options:**
  - **Repeatable / non-repeatable options**: control whether options can be used once or multiple times.
  - **Mutually exclusive options**: ensure that incompatible options cannot appear together.
  - **Conditional options**: only suggest options when certain conditions are met.
  - **Final options**: options that prevent any further options from being completed.
  - **Hidden options**: completable options that are not shown in the suggestion list.
  - **Capturing options**: collect options and their values to enable advanced, context-sensitive completions.

Disadvantages of crazy-complete
===============================

While crazy-complete offers many advantages, there are some trade-offs to be aware of:

- **Code size and verbosity:**
  Its biggest strength - **secure, fully controlled completions** - can also be its biggest weakness.
  - For **Bash**, this means the generated scripts contain a significant amount of boilerplate code for parsing options and positional arguments.
  - For **Fish**, large command-line definitions (more than 1000 options) may result in slower completions, although performance is usually acceptable for most use cases.
  - **Mitigation:** There are ways to reduce script size and improve performance. See [Tips And Tricks](docs/documentation.md#tips-and-tricks) for more details.
- **Not as optimized as hand-written scripts:**
   The generated scripts prioritize correctness and reliability over minimal size or maximum performance. Hand-written scripts may be more compact and slightly faster in some cases.

Installation
============

|Operating System       | Download                       | Command                                        |
|-----------------------|--------------------------------|-------------------------------------------------
|Arch Linux             | [0.3.8](https://github.com/crazy-complete/crazy-complete/releases/download/0.3.8/arch-linux-python-crazy-complete-0.3.8-1-any.pkg.tar.zst)       | `sudo pacman -U ./arch-linux-python-crazy-complete-0.3.8-1-any.pkg.tar.zst`         |
|Debian Trixie          | [0.3.8](https://github.com/crazy-complete/crazy-complete/releases/download/0.3.8/debian-trixie-python-crazy-complete_0.3.8_all.deb)   | `sudo apt install ./debian-trixie-python-crazy-complete_0.3.8_all.deb`   |
|Debian Bookworm        | [0.3.8](https://github.com/crazy-complete/crazy-complete/releases/download/0.3.8/debian-bookworm-python-crazy-complete_0.3.8_all.deb) | `sudo apt install ./debian-bookworm-python-crazy-complete_0.3.8_all.deb` |
|Ubuntu Noble           | [0.3.8](https://github.com/crazy-complete/crazy-complete/releases/download/0.3.8/ubuntu-noble-python-crazy-complete_0.3.8_all.deb)    | `sudo apt install ./ubuntu-noble-python-crazy-complete_0.3.8_all.deb`    |
|Ubuntu Jammy           | [0.3.8](https://github.com/crazy-complete/crazy-complete/releases/download/0.3.8/ubuntu-jammy-python-crazy-complete_0.3.8_all.deb)    | `sudo apt install ./ubuntu-jammy-python-crazy-complete_0.3.8_all.deb`    |
|Linux Mint 22          | [0.3.8](https://github.com/crazy-complete/crazy-complete/releases/download/0.3.8/linux-mint-22-python-crazy-complete_0.3.8_all.deb)   | `sudo apt install ./linux-mint-22-python-crazy-complete_0.3.8_all.deb`   |
|Linux Mint 21          | [0.3.8](https://github.com/crazy-complete/crazy-complete/releases/download/0.3.8/linux-mint-21-python-crazy-complete_0.3.8_all.deb)   | `sudo apt install ./linux-mint-21-python-crazy-complete_0.3.8_all.deb`   |
|Fedora 44              | [0.3.8](https://github.com/crazy-complete/crazy-complete/releases/download/0.3.8/fedora-44-python-crazy-complete-0.3.8-1.noarch.rpm)       | `sudo dnf install ./fedora-44-python-crazy-complete-0.3.8-1.noarch.rpm`       |
|Fedora 43              | [0.3.8](https://github.com/crazy-complete/crazy-complete/releases/download/0.3.8/fedora-43-python-crazy-complete-0.3.8-1.noarch.rpm)       | `sudo dnf install ./fedora-43-python-crazy-complete-0.3.8-1.noarch.rpm`       |
|OpenSuse (Tumbleweed)  | [0.3.8](https://github.com/crazy-complete/crazy-complete/releases/download/0.3.8/opensuse-python-crazy-complete-0.3.8-1.noarch.rpm)        | `sudo zypper install ./opensuse-python-crazy-complete-0.3.8-1.noarch.rpm`     |

- For other Linux distributions:
  ```
  git clone https://github.com/crazy-complete/crazy-complete
  cd crazy-complete
  python3 -m pip install .
  ```

Synopsis
========

> `crazy-complete [OPTIONS] {bash,fish,zsh,yaml,json} <DEFINITION_FILE>`

See [docs/documentation.md#options](docs/documentation.md#options) for a list of options.

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

Generate shell auto completions for Bash:

```
crazy-complete --input-type=yaml --include-file my_program.bash bash my_program.yaml
```

Definition file examples
========================

See [examples](https://github.com/crazy-complete/crazy-complete/tree/main/examples) for examples.

See [completions](https://github.com/crazy-complete/completions) for real world applications of crazy-complete.

You can even have a look at the [tests](https://github.com/crazy-complete/crazy-complete/tree/main/test).

Documentation
=============

See [docs/documentation.md](docs/documentation.md).

Comparision with other auto-complete generators
===============================================

See [docs/comparision.md](docs/comparision.md) for a comparision with other tools.

Questions or problems
=====================

Don't hesitate to open an issue on [GitHub](https://github.com/crazy-complete/crazy-complete/issues).

