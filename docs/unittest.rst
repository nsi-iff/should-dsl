Should-DSL with unittest
========================

*should-dsl* is unittest-compatible, so, in any unittest test case, failures on should expectations will result on unittest failures, not errors::

    >>> from should_dsl import *
    >>> import os
    >>> import unittest

    >>> class UsingShouldExample(unittest.TestCase):
    ...     def test_showing_should_not_be_works(self):
    ...         'hello world!' |should_not| be('Hello World!')
    ...
    ...     def test_showing_should_include_fails(self):
    ...         [1, 2, 3] |should| include(5)
    ...
    ...     def test_showing_should_include_works(self):
    ...         'hello world!' |should| include('world')
    ...
    ...     def test_showing_should_not_include_fails(self):
    ...         {'one': 1, 'two': 2} |should_not| include('two')
    ...
    ...     def test_showing_should_not_include_works(self):
    ...         ["that's", 'all', 'folks'] |should_not| include('that')

    >>> devnull = open(os.devnull, 'w')
    >>> runner = unittest.TextTestRunner(stream=devnull)
    >>> suite = unittest.TestLoader().loadTestsFromTestCase(UsingShouldExample)
    >>> runner.run(suite)
    <unittest...TextTestResult run=5 errors=0 failures=2>
    >>> devnull.close()
