'''
This file just give examples of should_dsl use
with unittest module.
You can write regular unittests but avoid using "asserts",
you can use the should_dsl!

    >>> output = StringIO()
    >>> runner = unittest.TextTestRunner(stream=output)
    >>> loader = unittest.TestLoader()
    >>> suite = loader.loadTestsFromTestCase(UsingShouldExample)
    >>> runner.run(suite)
    <unittest._TextTestResult run=8 errors=0 failures=4>

'''

import unittest
from cStringIO import StringIO
from should_dsl import (should_be, should_not_be,
                        should_have, should_not_have)


class UsingShouldExample(unittest.TestCase):
#    def test_showing_should_be_fail(self):
#        'hello world!' |should_be| 'Hello World!'

#    def test_showing_should_be_work(self):
#        1+1 |should_be| 2

#    def test_showing_should_not_be_fail(self):
#        'bdd' |should_not_be| 'bdd'
#        # equal_to doesn't compare ids, but content
#        'hi' |should_not_be.equal_to| 'HI'.lower()

    def test_showing_should_not_be_work(self):
        'hello world!' |should_not_be| 'Hello World!'
        # the objects have different ids below
#        'hi' |should_not_be| 'HI'.lower()


    def test_showing_should_have_fail(self):
        [1, 2, 3] |should_have| 5

    def test_showing_should_have_work(self):
        'hello world!' |should_have| 'world'

    def test_showing_should_not_have_fail(self):
        {'one': 1, 'two': 2} |should_not_have| 'two'

    def test_showing_should_not_have_work(self):
        ["that's", 'all', 'folks'] |should_not_have| "that"

