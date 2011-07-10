from dsl import ShouldNotSatisfied


class Subject(object):

    def __init__(self, obj, api):
        self._api = api
        self._obj = obj

    def should(self, **kwargs):
        matcher_name = kwargs.keys()[0]
        matcher_args = kwargs[matcher_name]
        matcher = self._api.find_matcher(matcher_name)
        if not matcher.match(matcher_args):
            raise ShouldNotSatisfied(matcher.message_for_failed_should())

    def should_not(self, **kwargs):
        matcher_name = kwargs.keys()[0]
        matcher_args = kwargs[matcher_name]
        matcher = self._api.find_matcher(matcher_name)
        if matcher.match(matcher_args):
            raise ShouldNotSatisfied(matcher.message_for_failed_should_not())


