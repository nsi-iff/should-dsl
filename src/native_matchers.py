"""
This module implements support for deprecated features.
"""

class NativeMatcher(object):
    def message_for_failed_should(self):
        return self._should_message % (self._value, self.arg)

    def message_for_failed_should_not(self):
        return self._should_not_message % (self._value, self.arg)


class NativeHaveMatcher(NativeMatcher):
    def __init__(self):
        self._should_message = "%r does not have %r"
        self._should_not_message = "%r have %r"

    def match(self, value):
        self._value = value
        return self.arg in self._value


class NativeBeMatcher(NativeMatcher):
    def __init__(self):
        self._should_message = "%r is not %r"
        self._should_not_message = "%r is %r"

    def match(self, value):
        self._value = value
        return self._value is self.arg

