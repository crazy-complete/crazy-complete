'''This module contains Exception classes for crazy-complete.'''


class CrazyError(Exception):
    '''Exception class for handling predictable or expected errors.

    This exception is raised in situations where the error condition is
    anticipated and should be handled gracefully by the program. It is
    meant to signal issues that are not caused by bugs in the code but
    by user input.
    '''


class CrazyTypeError(CrazyError):
    '''Exception raised for invalid parameter types.

    Args:
        name (str): The name of the parameter with the invalid type.
        expected (str): A description of the expected types for the parameter.
        value (any): The actual value passed that has the wrong type.
    '''

    def __init__(self, name, expected, value):
        self.name = name
        self.expected = expected
        self.value = value
        super().__init__(self.__str__())

    def __str__(self):
        s0 = 'Parameter `%s` has an invalid type.' % self.name
        s1 = 'Expected types: %s. Received: %r (%s)' % (
            self.expected, self.value, type(self.value).__name__)
        return f'{s0} {s1}'


class CrazySchemaValidationError(CrazyError):
    '''Exception raised for errors in the configuration structure.

    This exception is specifically designed to handle errors encountered when
    validating YAML or JSON configuration files against a defined schema.
    It provides detailed error messages, including the line and column numbers
    where the error occurred, to help locate the issue in the configuration
    file.

    Args:
        message (str): The error message.
        value_with_trace (ValueWithTrace): The value that caused the error.
    '''

    def __init__(self, message, value_with_trace):
        self.message = message
        self.value_with_trace = value_with_trace
        super().__init__(self.__str__())

    def __str__(self):
        pos_string = self.value_with_trace.get_position_string()

        if not pos_string:
            return self.message

        return f'{pos_string}: {self.message}'


class InternalError(Exception):
    '''Exception raised for internal errors within the program.

    This exception indicates that an unexpected condition has occurred that
    typically results from a bug or flaw in the code logic. It represents
    errors that are not caused by user actions or external factors, but
    rather by mistakes or inconsistencies in the program's internal state.
    '''
