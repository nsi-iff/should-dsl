import unittest
from should_dsl.api import ShouldDSLApi
from should_dsl.subject import Subject
from should_dsl.specs import Mock


class SubjectSpec(unittest.TestCase):

    def setUp(self):
        self.api = ShouldDSLApi()
        self.subject = Subject('foo', self.api)

    def test_should_have_method_should(self):
        self.assertTrue(hasattr(self.subject, 'should'))
        self.assertTrue(hasattr(self.subject.should, '__call__'))

    def test_should_method_should_call_find_matcher_on_api(self):
        matcher_mock = Mock()
        matcher_mock.match = Mock()
        self.api.find_matcher = Mock(return_value=matcher_mock)
        
        self.subject.should(equal_to='foo')
        self.assertTrue(self.api.find_matcher.called)
        self.assertTrue(self.api.find_matcher.called_with(('equal_to',), {}))

    def test_should_method_should_call_match_method_on_matcher_found(self):
        matcher_mock = Mock()
        matcher_mock.match = Mock(return_value='result')
        self.api.find_matcher = Mock(return_value=matcher_mock)
        
        self.assertEqual('result', self.subject.should(equal_to='foo'))
        self.assertTrue(matcher_mock.match.called)
        self.assertTrue(matcher_mock.match.called_with(('foo',), {}))
