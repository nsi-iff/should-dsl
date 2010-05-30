class NativeMatcher(object):
    def __init__(self, value):
        self._value = value

    def message_for_failed_should(self):
        return self._should_message % (self._value, self.arg)

    def message_for_failed_should_not(self):
        return self._should_not_message % (self._value, self.arg)


class NativeHaveMatcher(NativeMatcher):
    def __init__(self, value):
        NativeMatcher.__init__(self, value)
        self._should_message = "%s does not have %s"
        self._should_not_message = "%s have %s"

    def match(self):
        return self.arg in self._value


class NativeBeMatcher(NativeMatcher):
    def __init__(self, value):
        NativeMatcher.__init__(self, value)
        self._should_message = "%s is not %s"
        self._should_not_message = "%s is %s"

    def match(self):
        return self._value is self.arg

