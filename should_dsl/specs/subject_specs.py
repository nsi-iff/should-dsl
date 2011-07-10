import unittest
from should_dsl.api import ShouldDSLApi
from should_dsl.subject import Subject
from should_dsl.specs import Mock
from should_dsl.dsl import ShouldNotSatisfied



class SubjectShouldSpec(unittest.TestCase):

    def setUp(self):
        self.api = ShouldDSLApi()
        self.subject = Subject('foo', self.api)

    def test_should_have_method_should(self):
        self.assertTrue(hasattr(self.subject, 'should'))
        self.assertTrue(hasattr(self.subject.should, '__call__'))

    def test_should_method_should_call_find_matcher_on_api(self):
        matcher_mock = Mock()
        matcher_mock.match = Mock(return_value=True)
        self.api.find_matcher = Mock(return_value=matcher_mock)
        
        self.subject.should(equal_to='foo')
        self.assertTrue(self.api.find_matcher.called)
        self.assertTrue(self.api.find_matcher.called_with(('equal_to',), {}))

    def test_should_method_should_call_match_method_on_matcher_found(self):
        matcher_mock = Mock()
        matcher_mock.match = Mock(return_value=True)
        self.api.find_matcher = Mock(return_value=matcher_mock)
        
        self.assertEqual(None, self.subject.should(equal_to='foo'))
        self.assertTrue(matcher_mock.match.called)
        self.assertTrue(matcher_mock.match.called_with(('foo',), {}))

    def test_should_raise_shouldnotsatisfied_if_does_not_match(self):
        matcher_mock = Mock()
        matcher_mock.match = Mock(return_value=False)
        self.api.find_matcher = Mock(return_value=matcher_mock)
        
        self.assertRaises(ShouldNotSatisfied, self.subject.should, **{'equal_to': 'foo'})


class SubjectShouldNotSpec(unittest.TestCase):

    def setUp(self):
        self.api = ShouldDSLApi()
        self.subject = Subject('foo', self.api)

    def test_should_have_method_should_not(self):
        self.assertTrue(hasattr(self.subject, 'should_not'))
        self.assertTrue(hasattr(self.subject.should_not, '__call__'))

    def test_should_not_method_should_call_find_matcher_on_api(self):
        matcher_mock = Mock()
        matcher_mock.match = Mock(return_value=False)
        self.api.find_matcher = Mock(return_value=matcher_mock)
        
        self.subject.should_not(equal_to='foo')
        self.assertTrue(self.api.find_matcher.called)
        self.assertTrue(self.api.find_matcher.called_with(('equal_to',), {}))

    def test_should_not_method_should_call_match_method_on_matcher_found(self):
        matcher_mock = Mock()
        matcher_mock.match = Mock(return_value=False)
        self.api.find_matcher = Mock(return_value=matcher_mock)
        
        self.assertEqual(None, self.subject.should_not(equal_to='foo'))
        self.assertTrue(matcher_mock.match.called)
        self.assertTrue(matcher_mock.match.called_with(('foo',), {}))

    def test_should_raise_shouldnotsatisfied_if_does_match(self):
        matcher_mock = Mock()
        matcher_mock.match = Mock(return_value=True)
        self.api.find_matcher = Mock(return_value=matcher_mock)
        
        self.assertRaises(ShouldNotSatisfied, self.subject.should_not, **{'equal_to': 'foo'})

