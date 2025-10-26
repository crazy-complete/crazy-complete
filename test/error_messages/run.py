#!/usr/bin/env python3

'''This script is for checking error messages of cracy-complete.'''

import os
import sys
import yaml

SCRIPT_FILE = os.path.basename(__file__)
SCRIPT_DIR  = os.path.dirname(__file__)
YAML_TESTS_EXPECTED_INFILE  = 'yaml_expected'
YAML_TESTS_EXPECTED_OUTFILE = 'yaml_expected.new'
DICTIONARY_TESTS_EXPECTED_INFILE  = 'dictionary_expected'
DICTIONARY_TESTS_EXPECTED_OUTFILE = 'dictionary_expected.new'

os.environ['LANGUAGE'] = 'en'

# We want to import the development version of cracy-complete,
# not the installed version.
CRAZY_COMPLETE_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..'))
sys.path.insert(0, CRAZY_COMPLETE_DIR)

import crazy_complete # noqa: E402

os.chdir(os.path.dirname(os.path.abspath(__file__)))

class TesterBase:
    def __init__(self, expected_file, new_expected_file):
        self.results = []
        self.expected_file = expected_file
        self.new_expected_file = new_expected_file

    def run(self):
        for file in sorted(os.listdir('.')):
            if os.path.isdir(file):
                self.run_subdirectory(file)

        result_content = '\n'.join(self.results)

        with open(self.new_expected_file, 'w', encoding='UTF-8') as fh:
            fh.write(result_content)

        try:
            with open(self.expected_file, 'r', encoding='UTF-8') as fh:
                expected_content = fh.read()
        except Exception as e:
            print(f'Cannot open `{self.expected_file}`: {e}')
            sys.exit(1)

        if expected_content != result_content:
            print(f'{self.expected_file} differs from {self.new_expected_file}.')
            print('Use diff on those files for details')
            sys.exit(1)

    def run_subdirectory(self, directory):
        self.results.append(f'======= Directory "{directory}" =======')

        for file in sorted(os.listdir(directory)):
            full_path = os.path.join(directory, file)
            basename = file.replace('.yaml', '')
            self.run_test(full_path, basename)


class YamlValidatorTester(TesterBase):
    def run_test(self, file, basename):
        print(f'Testing {file}', end=' ... ')

        have_error = 'No error'

        with open(file, 'r', encoding='UTF-8') as fh:
            content = fh.read()

        try:
            parser = crazy_complete.extended_yaml_parser.ExtendedYAMLParser()
            definitions = parser.parse(content)
            crazy_complete.scheme_validator.validate(definitions)
        except crazy_complete.errors.CrazyError as e:
            have_error = str(e)

        self.results.append('%-40s | %s' % (basename, have_error))

        print()


class DictionaryValidatorTester(TesterBase):
    def run_test(self, file, basename):
        print(f'Testing {file}', end=' ... ')

        have_error = 'No error'

        with open(file, 'r', encoding='UTF-8') as fh:
            definition = list(yaml.safe_load_all(fh))

        try:
            cmdline = crazy_complete.dictionary_source.dictionaries_to_commandline(definition)
            crazy_complete.bash.generate_completion(cmdline, None)
        except crazy_complete.errors.CrazyError as e:
            have_error = str(e)

        self.results.append('%-40s | %s' % (basename, have_error))

        print()

testers = [
    YamlValidatorTester(YAML_TESTS_EXPECTED_INFILE, YAML_TESTS_EXPECTED_OUTFILE),
    DictionaryValidatorTester(DICTIONARY_TESTS_EXPECTED_INFILE, DICTIONARY_TESTS_EXPECTED_OUTFILE)
]

for tester in testers:
    tester.run()
