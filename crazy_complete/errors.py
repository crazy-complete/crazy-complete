'''This module contains Exception classes for crazy-complete.'''

class CrazyError(Exception):
    '''
    Exception class for handling predictable or expected errors.

    This exception is raised in situations where the error condition is
    anticipated and should be handled gracefully by the program. It is
    meant to signal issues that are not caused by bugs in the code but
    by user input.
    '''

class CrazyTypeError(CrazyError):
    '''
    Exception raised for invalid parameter types.

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
        return 'Parameter `%s` has an invalid type. Expected types: %s. Received: %r (%s)' % (
            self.name, self.expected, self.value, type(self.value).__name__)

class InternalError(Exception):
    '''
    Exception raised for internal errors within the program.

    This exception indicates that an unexpected condition has occurred that
    typically results from a bug or flaw in the code logic. It represents
    errors that are not caused by user actions or external factors, but
    rather by mistakes or inconsistencies in the program's internal state.
    '''
