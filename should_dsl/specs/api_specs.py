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

    def test_should_generate_matcher_if_argument_is_a_function(self):
        def fake_matcher():
            return (lambda x, y: x == y, "msg")

        self.api.add_matcher(fake_matcher)
        matcher_created = self.api.find_matcher('fake_matcher')

        self.assertTrue(hasattr(matcher_created, '__call__'))
        self.assertTrue(hasattr(matcher_created, 'match'))
        self.assertTrue(hasattr(matcher_created, 'message_for_failed_should'))
        self.assertTrue(hasattr(matcher_created, 'message_for_failed_should_not'))
        self.assertTrue(hasattr(matcher_created, 'name'))
        self.assertEquals('fake_matcher', matcher_created.name)

    def test_should_be_possible_to_add_aliases_to_matchers(self):
        my_fake_matcher = Mock()
        my_fake_matcher.name = 'fake_matcher'
        self.api.add_matcher(my_fake_matcher)
        self.api.add_aliases(fake_matcher='foo')
        self.assertEquals(my_fake_matcher, self.api.find_matcher('foo'))

    def test_should_raise_typeerror_if_matcher_constructor_expecs_more_than_one_arg(self):
        def fake_matcher():
            return (lambda x, y: x == y, "msg")
        self.api.add_matcher(fake_matcher)
        matcher_created = self.api.find_matcher('fake_matcher')
        matcher_created.__init__ = lambda self, x, y: 'foo'

        self.assertRaises(TypeError, self.api.add_matcher, matcher_created)

