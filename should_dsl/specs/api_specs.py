import unittest
from should_dsl.api import ShouldDSLApi
from should_dsl.specs import Mock


class ShouldDSLApiSpec(unittest.TestCase):

    def setUp(self):
        self.api = ShouldDSLApi()

    def test_matchers_should_start_empty(self):
        self.assertEquals({}, self.api.matchers)

    def test_should_be_possible_to_add_matchers(self):
        my_fake_matcher = Mock()
        my_fake_matcher.name = 'fake_matcher'
        self.api.add_matcher(my_fake_matcher)
        self.assertEquals({'fake_matcher': my_fake_matcher}, self.api.matchers)

    def test_should_be_possible_to_find_matcher_by_name(self):
        my_fake_matcher = Mock()
        my_fake_matcher.name = 'fake_matcher'
        self.api.add_matcher(my_fake_matcher)
        self.assertEquals(my_fake_matcher, self.api.find_matcher('fake_matcher'))
