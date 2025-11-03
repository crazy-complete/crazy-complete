'''YAML Parser with column and line information.'''

import yaml
from yaml.events import (StreamStartEvent,
                         DocumentStartEvent, DocumentEndEvent,
                         MappingStartEvent, MappingEndEvent,
                         SequenceStartEvent, SequenceEndEvent,
                         ScalarEvent, AliasEvent)

from .value_with_trace import ValueWithTrace
from .errors import CrazySchemaValidationError


_error = CrazySchemaValidationError


class ExtendedYAMLParser:
    '''Parse YAML with the ability to trace the origin of parsed values.'''

    def __init__(self):
        self.src = None
        self.data = []
        self.current_stack = []
        self.current_key = None

    def parse(self, stream):
        """
        Parses the given YAML stream in a SAX-like way and reconstructs the structure.

        Raises:
            - yaml.parser.ParserError
            - errors.CrazySchemaValidationError
        """
        self.src = stream
        self.data = []
        self.current_stack = []
        self.current_key = None

        loader = yaml.Loader(stream)
        try:
            while True:
                event = loader.get_event()
                if event is None:
                    break
                self.handle_event(event)
        finally:
            loader.dispose()

        return self.data

    def handle_event(self, event):
        """
        Handle each YAML parsing event and construct the corresponding data structure.
        """
        if isinstance(event, StreamStartEvent):
            pass
        elif isinstance(event, DocumentStartEvent):
            pass
        elif isinstance(event, DocumentEndEvent):
            if self.current_stack:
                self.data.append(self.current_stack.pop())
        elif isinstance(event, MappingStartEvent):
            new_map = ValueWithTrace.from_yaml_event({}, self.src, event)
            self.add_to_current_structure(self.current_key, new_map)
            self.current_stack.append(new_map)
            self.current_key = None
        elif isinstance(event, SequenceStartEvent):
            new_seq = ValueWithTrace.from_yaml_event([], self.src, event)
            self.add_to_current_structure(self.current_key, new_seq)
            self.current_stack.append(new_seq)
            self.current_key = None
        elif isinstance(event, ScalarEvent):
            value = self.convert_scalar(event.value, event.implicit)
            value = ValueWithTrace.from_yaml_event(value, self.src, event)

            if self.current_stack and isinstance(self.current_stack[-1].value, list):
                self.add_to_current_structure(None, value)
            else:
                if self.current_key is None:
                    self.current_key = value
                else:
                    self.add_to_current_structure(self.current_key, value)
                    self.current_key = None
        elif isinstance(event, (MappingEndEvent, SequenceEndEvent)):
            self.current_stack.pop()
        elif isinstance(event, AliasEvent):
            value = ValueWithTrace.from_yaml_event(None, self.src, event)
            raise _error('Anchors not supported', value)

    def add_to_current_structure(self, key, value):
        """
        Add a value to the current structure (either dict or list).
        """
        if not self.current_stack:
            # Root-level element
            self.current_stack.append(value)
            return

        current = self.current_stack[-1]
        if isinstance(current.value, dict):
            if key is None:
                raise _error("Missing key for mapping in YAML", value)
            current.value[key] = value
        elif isinstance(current.value, list):
            current.value.append(value)
        else:
            raise _error("Invalid structure in YAML", value)

    def convert_scalar(self, value, implicit):
        """
        Converts a scalar based on its type hints (implicit tuple).
        """
        if implicit[0]:
            lower = value.lower()

            if lower in ("null", "~", ""):
                return None

            if lower in ("true", "on", "yes"):
                return True

            if lower in ("false", "off", "no"):
                return False

            try:
                return int(value)
            except ValueError:
                pass

            try:
                return float(value)
            except ValueError:
                pass

        return value
