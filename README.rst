Should-DSL: Improved readability for should-style expectations
==============================================================

The goal of *Should-DSL* is to write should expectations in Python as clear and readable as possible, using **"almost"** natural language (with limitations from Python language).

For using this DSL, you need to import all the module's namespace, as::

    from should_dsl import *


For example::

    1  |should_be.equal_to| 1     # will be true
    'should' |should_have| 'oul'  # will also be true
    3 |should_be.into| (0, 1, 2)  # will raise a ShouldNotSatisfied exception


The *equal_to* matcher verifies object equality. If you want to ensure identity, you must use *should_be* with no matcher::

    2 |should_be| 2


A nice example of exceptions would be::

    def raise_zerodivisionerror():
        return 1/0
    ZeroDivisionError |should_be.thrown_by| raise_zerodivisionerror


Both *should_have* and *should_be* have versions for negation::

    2 |should_not_be.into| [1, 3, 5]    # will be true
    'should' |should_not_have| 'oul'    # will raise a ShouldNotSatisfied exception


Extending the DSL with custom matchers is easy::

    @matcher
    def the_square_root_of():
        import math
        return (lambda x, y: x == math.sqrt(y), "%s is %sthe square root of %s")

    3 |should_be.the_square_root_of| 9    # will be true
    4 |should_be.the_square_root_of| 9    # will raise a ShouldNotSatisfiedException


Should-DSL with unittest
------------------------

*should-dsl* is unittest-compatible, so, on a unittest test case, failures on should expectations will result on unittest failures, not errors::

    >>> from should_dsl import *
    >>> import unittest

    >>> class UsingShouldExample(unittest.TestCase):
    ...     def test_showing_should_not_be_works(self):
    ...         'hello world!' |should_not_be| 'Hello World!'
    ... 
    ...     def test_showing_should_have_fails(self):
    ...         [1, 2, 3] |should_have| 5
    ... 
    ...     def test_showing_should_have_works(self):
    ...         'hello world!' |should_have| 'world'
    ... 
    ...     def test_showing_should_not_have_fails(self):
    ...         {'one': 1, 'two': 2} |should_not_have| 'two'
    ... 
    ...     def test_showing_should_not_have_works(self):
    ...         ["that's", 'all', 'folks'] |should_not_have| 'that'

    >>> from cStringIO import StringIO
    >>> runner = unittest.TextTestRunner(stream=StringIO())
    >>> suite = unittest.TestLoader().loadTestsFromTestCase(UsingShouldExample)
    >>> runner.run(suite)
    <unittest._TextTestResult run=5 errors=0 failures=2>



Should-DSL Matchers
===================

Below there are some explanations about the available matchers in *should_dsl* package.


Available Matchers
------------------


- all_of
- any_of
- ended_with
- equal_to
- greater_than_or_equal_to
- greater_than
- in_any_order
- into
- kind_of
- less_than_or_equal_to
- less_than
- like
- thrown_by

"Native" matchers
-----------------

- should_be (by default it do checking on ids)
- should_have

Examples::

    >>> a = "some message"
    >>> b = "some message"
    >>> id(a) == id(b) # the strings are equal but the ids are different
    False
    >>> a |should_be| b
    Traceback (most recent call last):
    ...
    ShouldNotSatisfied: some message is not some message

    >>> c = "another message"
    >>> d = c
    >>> id(c) == id(d)
    True
    >>> c |should_be| d
    True
    
    >>> [1,2,3] |should_have| 1
    True
    


Examples of use
===============

There are some usages of Should-DSL below::

    >>> [1, 2, 3] |should_have.all_of| [2, 3]
    True
    
    >>> [1, 2, 3] |should_have.any_of| [1, 2]
    True

    >>> 'hello world' |should_be.ended_with| 'world'
    True

    >>> 1 |should_be.equal_to| 1
    True

    >>> 1 |should_be.greater_than_or_equal_to| 0.9
    True

    >>> 1 |should_be.greater_than| 0.9
    True

    >>> [1, 2, 3] |should_have.in_any_order| [3, 1]
    True

    >>> 1 |should_be.into| [1,2,3]
    True

    >>> 1 |should_be.kind_of| int
    True

    >>> 0.9 |should_be.less_than_or_equal_to| 1
    True

    >>> 0.9 |should_be.less_than| 1
    True

    >>> 'Hello World' |should_be.like| r'Hello W.+'
    True

    >>> ZeroDivisionError |should_be.thrown_by| (lambda: 1/0)
    True
