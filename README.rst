Should-DSL: Improved readability for should-style expectations
==============================================================

The goal of *Should-DSL* is to write should expectations in Python as clear and readable as possible, using **"almost"** natural language (limited - sometimes - by the Python language constraints).

For using this DSL, you need to import the should and should_not objects from should_dsl module, or import all from should_dsl.

For example::

    1 |should| equal_to(1)             # will be True
    'should' |should| include('oul')   # will also be True
    3 |should| be_into([0, 1, 2])      # will raise a ShouldNotSatisfied exception


The *equal* matcher verifies object equality. If you want to ensure identity, you must use *be* as matcher::

    2 |should| be(2)


A nice example of exceptions would be::

    def raise_zerodivisionerror():
        return 1/0
    ZeroDivisionError |should| be_thrown_by(raise_zerodivisionerror)


*should* has a negative version::

    2 |should_not| be_into([1, 3, 5])     # will be true
    'should' |should_not| include('oul')  # will raise a ShouldNotSatisfied exception


Extending the DSL with custom matchers is easy::

    from should_dsl import matcher

    @matcher
    def the_square_root_of():
        import math
        return (lambda x, y: x == math.sqrt(y), "%s is %sthe square root of %s")

    3 |should| be_the_square_root_of(9)    # will be true
    4 |should| be_the_square_root_of(9)    # will raise a ShouldNotSatisfiedException


Should-DSL with unittest
------------------------

*should-dsl* is unittest-compatible, so, on a unittest test case, failures on should expectations will result on unittest failures, not errors::

    >>> from should_dsl import *
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
- be
- ended_with
- equal
- equal_to_ignoring_case
- greater_than_or_equal_to
- greater_than
- in_any_order
- into
- kind_of
- less_than_or_equal_to
- less_than
- like
- throw
- thrown_by

Examples::

    >>> a = "some message"
    >>> b = "some message"
    >>> id(a) == id(b) # the strings are equal but the ids are different
    False
    >>> a |should| be(b)
    Traceback (most recent call last):
    ...
    ShouldNotSatisfied: some message is not some message

    >>> c = "another message"
    >>> d = c
    >>> id(c) == id(d)
    True
    >>> c |should| be(d)
    True

    >>> [1,2,3] |should| include(1)
    True


Predicate matchers
------------------

Should-DSL supports predicate matchers::

    >>> class Foo(object):
    ...     def __init__(self, valid=True):
    ...         self.valid = valid
    >>> Foo() |should| be_valid
    True

Predicate matchers also work with methods::

    >>> class House(object):
    ...     def __init__(self, kind):
    ...         self._kind = kind
    ...     def made_of(self, kind):
    ...         return self._kind.upper() == kind.upper()
    >>> house = House('Wood')
    >>> house |should| be_made_of('wood')
    True
    >>> house |should| be_made_of('stone')
    Traceback (most recent call last):
    ...
    ShouldNotSatisfied: expected made_of('stone') to return true, got false


Deprecated usage
----------------

All *should-dsl* matchers also support a deprecated form, so::

    3 |should_not| equal_to(3)

can be written as::

    3 |should_not.equal_to| 3

Besides, should_dsl module offers should_be, should_have (and their negative counterparts) to be used with no matchers, as::

    [1, 2] |should_have| 1
    x |should_be| 1

This syntax for writing expectations was changed because the requirement to have a single "right value" is a limitation to future improvements.

We don't plan to remove the deprecated syntax in the near future, but we discourage its use from now.

