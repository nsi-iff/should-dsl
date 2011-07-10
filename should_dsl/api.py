class ShouldDSLApi(object):

    def __init__(self):
        self.matchers = {}

    def add_matcher(self, matcher_name, matcher):
        self.matchers[matcher_name] = matcher

    def find_matcher(self, matcher_name):
        return self.matchers[matcher_name]
