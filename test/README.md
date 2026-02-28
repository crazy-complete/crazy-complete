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

- **./install-completions.sh**

  - Installs or uninstalls system-wide completion files for `tests/crazy-complete-test`

  - Used for interactive testing

  - **Usage**: `./install-completions.sh {install|uninstall}`

    - To install the completion files, run `./install-completions.sh install`

    - To uninstall the completion files, run `./install-completion.sh uninstall`

Test subdirectories
-------------------

- **./tests/run.py**

  - Contains the primary tests focused on checking the functionality of
    generated completion scripts.

  - **Execution methods**

    - `--driver=tmux`:
      This is the default driver.
      It uses `tmux` to emulate terminals.

    - `--driver=pyte`:
      This requires the python modules `pyte` and `pexpect` to be installed.
      This driver has been disabled, because the Fish shell started using
      the `kitty` protocol which is not supported by `pyte`.

  - **Usage**: `./tests/run.py [-t=<NUM>] [-w=<SECONDS>] [-d={pyte,tmux}] [-f]`

    - `-d|--driver`:
      As stated above, this option is used to specify the execution method.

    - `-t|--threads`:
      Sets how many threads per shell shall be used while testing.
      The default is `1` to ensure there are no problems even on slow systems.
      However, a value of `5` is recommended on normal systems.

    - `-w|--wait`:
      Sets how many seconds to wait for completion output per test.
      The default is `5` to ensure there are no problems even on slow systems.
      However, a value of `1` is recommended on normal systems.

    - `-f|--fast`:
      Makes the tests run even faster at the cost of corectness for some tests.
      For tests where the input matches the expected output, these tests will always pass.

  - The script writes a file named `./tests/tests.new.yaml`.
    If the tests fail, this file can be diffed against `./tests/tests.yaml`.

- **./conversion/run.sh**

   - Simple tests that validate JSON and YAML conversion.

   - Also includes simple tests for parsing the help output.

   - **Usage**: `./test/conversion/run.sh`

- **./error_messages/run.py**

   - Includes tests specifically designed to validate error handling.

   - Verifies that the tool provides meaningful error messages when misued,
     ensuring user feedback is clear and helpful.

   - **Usage**: `./error_messages/run.py`
