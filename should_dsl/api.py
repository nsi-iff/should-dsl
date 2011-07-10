import sys
from types import FunctionType


class ShouldDSLApi(object):

    def __init__(self):
        self.matchers = {}

    def add_matcher(self, matcher):
        if isinstance(matcher, FunctionType):
            function, message = matcher()
            class GeneratedMatcher(object):
                name = matcher.__name__
                def __init__(self):
                    self._function, self._message = function, message
                def __call__(self, arg):
                    self.arg = arg
                    return self
                def match(self, value):
                    self._value = value
                    return self._function(self._value, self.arg)
                def message_for_failed_should(self):
                    return self._message % (self._value, "not ", self.arg)
                def message_for_failed_should_not(self):
                    return self._message % (self._value, "", self.arg)
            matcher = GeneratedMatcher
            name = GeneratedMatcher.name
        else:
            name = matcher.name
        self._ensure_matcher_init_doesnt_have_arguments(matcher)
        self.matchers[matcher.name] = matcher

    def _ensure_matcher_init_doesnt_have_arguments(self, matcher_object):
         try:
             matcher_object()
         except TypeError:
             e = sys.exc_info()[1]
             if str(e).startswith('__init__() takes exactly'):
                 raise TypeError('matcher class constructor cannot have arguments')
             else:
                 raise

    def find_matcher(self, matcher_name):
        return self.matchers[matcher_name]

    def add_aliases(self, **kw):
        for matcher_name, alias in kw.items():
            self.matchers[alias] = self.find_matcher(matcher_name)
