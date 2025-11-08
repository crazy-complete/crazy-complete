'''Value holder class with line and column information'''


class ValueWithTrace:
    '''Represents a value from a configuration file along with its metadata.

    This class is used to associate a value from a YAML or JSON file with its
    source, line number, and column number. It is particularly useful for
    debugging and error reporting, as it provides precise location information
    for the value in the original configuration file.

    Attributes:
        value (Any): The value extracted from the configuration file.
        src (str): The source of the configuration file.
        line (int): The line number of the value in the source.
        column (int): The column number of the value in the source.
    '''

    def __init__(self, value, source, line, column):
        self.value = value
        self.source = source
        self.line = line
        self.column = column

    @staticmethod
    def from_yaml_event(value, source, event):
        '''Constructs a `ValueWithTrace` from a YAML event object.'''

        return ValueWithTrace(
            value,
            source,
            event.start_mark.line + 1,
            event.start_mark.column + 1)

    def get_position_string(self):
        '''Return a string describing the position of the value.'''

        return f'line {self.line}, column {self.column}'

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, other):
        return self.value == other

    def __repr__(self):
        return f'{self.value!r}'


class ValueWithOutTrace:
    '''Class holding a value without metadata. '''

    def __init__(self, value):
        self.value = value

    def get_position_string(self):
        '''Return empty string.'''

        return ''

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, other):
        return self.value == other

    def __repr__(self):
        return f'{self.value!r}'
