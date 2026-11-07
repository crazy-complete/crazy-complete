crazy-complete tests
--------------------

This directory contains all the tests for the **crazy-complete** project.
The tests are organized into specific categories to ensure functionality and proper error handling.

Root test directory
-------------------

- **./run.sh**

  - This script serves as the main entry point for running all tests within
    the `test` directory.

  - **Usage**: To run all tests, simply execute `./run.sh`
    Any additional options are passed to `./tests/run.py`.

Test subdirectories
-------------------

- **./tests/**

  - Contains the primary tests for checking the functionality of
    generated completion scripts.

  - Each test group lives in its own subdirectory with the following layout:

    ```
    tests/
      <group>/
        definition.yaml   # the crazy-complete definition
        tests.yaml        # test cases for this group
        include.bash      # (optional) shell-specific helpers
        include.fish
        include.zsh
    ```

  - Tests are discovered by scanning `./tests/` for subdirectories that
    contain a `tests.yaml` file (`output/` and `tmp/` are skipped).

  - **Execution methods**

    - `--driver=tmux`:
      This is the default driver.
      It uses `tmux` to emulate terminals.

    - `--driver=pyte`:
      This requires the python modules `pyte` and `pexpect` to be installed.
      This driver has been disabled, because the Fish shell started using
      the `kitty` protocol which is not supported by `pyte`.

  - **Usage**: `./tests/run.py [OPTIONS]`

    - `-d|--driver <DRIVER>`:
      As stated above, this option is used to specify the execution method.

    - `-t|--threaded`:
      Flag (no argument).
      When set, the three shells of a single test file run concurrently
      (one thread per shell) instead of sequentially.
      This roughly triples the speed for a single test file.

    - `-p|--parallel <NUM>`:
      Maximum number of test *files* to run in parallel (default `1`).
      Use `-p 0` to run all test files at once (no limit).
      Each parallel worker spawns its own tmux session per shell.

    - `-w|--wait <SECONDS>`:
      Sets how many seconds to wait for completion output per test.
      The default is `5` to ensure there are no problems even on slow systems.
      However, a value of `1` is recommended on normal systems.

    - `-s|--select <DIRECTORY>`:
      Execute only the test group(s) in the specified subdirectory(ies).
      Accepts a path relative to `./tests/` or just the directory basename
      (e.g. `-s float`, `-s key_value_list`).
      Can be repeated to select multiple groups.
      Useful for developing or debugging a specific feature without having
      to run all tests.

    - `-f|--fast`:
      Makes the tests run even faster at the cost of correctness for some tests.
      For tests where the input matches the expected output, these tests
      will always pass.

  - **Output on failure**

    When one or more test groups fail, `run.py` prints:

    1. A diff between `tests.yaml` and `tests.new.yaml` for each failed group.
    2. The total number of failed tests.

    The `tests.new.yaml` files are written for *all* groups (not only the
    failed ones) so they can be diffed manually if needed.

- **./conversion/run.sh**

  - Simple tests that validate JSON and YAML conversion.

  - Also includes simple tests for parsing the help output.

  - **Usage**: `./test/conversion/run.sh`

- **./error_messages/run.py**

  - Includes tests specifically designed to validate error handling.

  - Verifies that the tool provides meaningful error messages when misued,
    ensuring user feedback is clear and helpful.

  - **Usage**: `./error_messages/run.py`

- **./completely/run.sh**

  - Tests for the `completely` input type.
    For every `*.input.yaml` file this script runs crazy-complete
    in `yaml` mode with `--input-type=completely` and compares the result
    against the matching `*.expected.yaml` file.

  - **Usage**: `./completely/run.sh [OPTIONS]`

    - `--update`:
      Instead of checking against the expected files, this writes the current
      crazy-complete output to the matching `*.expected.yaml`.
      Use this to (re)generate the expected files after a change.
