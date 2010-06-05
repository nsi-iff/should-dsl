Should-DSL: Improved readability for should-style expectations
==============================================================

The goal of *Should-DSL* is to write should expectations in Python as clear and readable as possible, using **"almost"** natural language (limited - sometimes - by the Python language constraints).

For using this DSL, you need to import the should and should_not objects from should_dsl module, or import all from should_dsl.

For example::

    1 |should| equal_to(1)             # will be True
    'should' |should| include('oul')   # will also be True
    3 |should| be_into([0, 1, 2])      # will raise a ShouldNotSatisfied exception


The *equal_to* matcher verifies object equality. If you want to ensure identity, you must use *be* as matcher::

    2 |should| be(2)


A nice example of exceptions would be::

    def raise_zerodivisionerror():
        return 1/0
    raise_zerodivisionerror |should| throw(ZeroDivisionError)


*should* has a negative version::

    2 |should_not| be_into([1, 3, 5])     # will be true
    'should' |should_not| include('oul')  # will raise a ShouldNotSatisfied exception


Extending the DSL with custom matchers is easy::

    from should_dsl import matcher

    @matcher
    def be_the_square_root_of():
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


**be**

Checks object identity (*is*).::

    >>> 1 |should| be(1)
    True

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


**be_greater_than**
**be_greater_than_or_equal_to**
**be_less_than**
**be_less_than_or_equal_to**

Simply checks the given comparisons.::

    >>> 1 |should_not| be_greater_than(1)
    True
    >>> 2 |should| be_greater_than_or_equal_to(2)
    True
    >>> 0.1 |should| be_less_than(0.11)
    True
    >>> 3000 |should| be_less_than_or_equal_to(3001)
    True


**be_into**
**contain**
**include**

Verifies if an object is contained (*be_into*) or contains (*contain*) another. The *contain* and *include* matchers do exactly the same job.::

    >>> 1 |should| be_into(range(2))
    True
    >>> ['a'] |should_not| be_into(['a'])
    True
    >>> ['a'] |should| be_into([['a']])
    True
    >>> ['x', 'y', 'z'] |should| contain('z')
    True
    >>> ['x', 'y', 'z'] |should| include('z')
    True


**be_kind_of**

Verifies if an object is of a given type.::

    >>> 1 |should| be_kind_of(int)
    True

    >>> class Foo: pass
    >>> Foo() |should| be_kind_of(Foo)
    True
    >>> class Bar(Foo): pass
    >>> Bar() |should| be_kind_of(Foo)
    True


**be_like**

Checks matching against a regular expression.::

    >>> 'Hello World' |should| be_like(r'Hello W.+')
    True
    >>> '123 is a number' |should_not| be_like(r'^[12]+ is a number')
    True


**be_thrown_by**
**throw**

Checks if a given piece of code raises an arbitrary exception.::

    >>> ZeroDivisionError |should| be_thrown_by(lambda: 1/0)
    True
    >>> (lambda: 1/0.000001) |should_not| throw(ZeroDivisionError)
    True

*throw* matcher also supports message checking.::

    >>> def foo(): raise TypeError("Hey, it's cool!")
    >>> foo |should| throw(TypeError, message="Hey, it's cool!")
    True
    >>> foo |should| throw(TypeError, message="This won't work...")
    Traceback (most recent call last):
    ...
    ShouldNotSatisfied: expected to throw TypeError with the message "This won't work...", got TypeError with "Hey, it's cool!"


**close_to**

Checks if a number is close to another, given a delta.::

    >>> 1 |should| close_to(0.9, delta=0.1)
    True
    >>> 0.8 |should| close_to(0.9, delta=0.1)
    True
    >>> 1 |should_not| close_to(0.89, delta=0.1)
    True
    >>> 4.9 |should| close_to(4, delta=0.9)
    True


**end_with**

Verifies if a string ends with a given suffix.::

    >>> "brazil champion of 2010 FIFA world cup" |should| end_with('world cup')
    True
    >>> "hello world" |should_not| end_with('worlds')
    True


**equal_to**

Checks object equality (not identity).>::

    >>> 1 |should| equal_to(1)
    True

    >>> class Foo: pass
    >>> Foo() |should_not| equal_to(Foo())
    True

    >>> class Foo(object):
    ...     def __eq__(self, other):
    ...         return True
    >>> Foo() |should| equal_to(Foo())
    True


**equal_to_ignoring_case**

Checks equality of strings ignoring case.::

    >>> 'abc' |should| equal_to_ignoring_case('AbC')
    True

    >>> 'XYZAb' |should| equal_to_ignoring_case('xyzaB')
    True


**have**

Checks the element count of a given collection. It can work with iterables, requiring a qualifier expression for readability purposes that is only a syntax sugar.::

    >>> ['b', 'c', 'd'] |should| have(3).elements
    True

    >>> [1, [1, 2, 3], 'a', lambda: 1, 2**3] |should| have(5).heterogeneous_things
    True

    >>> ['asesino', 'japanische kampfhoerspiele', 'facada'] |should| have(3).grindcore_bands
    True

    >>> "left" |should| have(4).characters
    True

*have* also works with non-iterable objects, in which the qualifier is a name of attribute or method that contains the collection to be count.::

    >>> class Foo:
    ...     def __init__(self):
    ...         self.inner_things = ['a', 'b', 'c']
    ...     def pieces(self):
    ...         return range(10)
    >>> Foo() |should| have(3).inner_things
    True
    >>> Foo() |should| have(10).pieces
    True


**have_at_least**

Same to *have*, but checking if the element count is greater than or equal to the given value. Works for collections with syntax sugar, object attributes or methods.::

    >>> range(20) |should| have_at_least(19).items
    True
    >>> range(20) |should| have_at_least(20).items
    True
    >>> range(20) |should_not| have_at_least(21).items
    True


**have_at_most**

Same to *have*, but checking if the element count is less than or equal to the given value. Works for collections with syntax sugar, object attributes or methods.::

    >>> range(20) |should_not| have_at_most(19).items
    True
    >>> range(20) |should| have_at_most(20).items
    True
    >>> range(20) |should| have_at_most(21).items
    True


**include_all_of**
**include_in_any_order**

Check if a iterable includes all elements of another. Both matchers do the same job.::

   >>> [4, 5, 6, 7] |should| include_all_of([5, 6])
   True
   >>> [4, 5, 6, 7] |should| include_in_any_order([5, 6])
   True
   >>> ['b', 'c'] |should| include_all_of(['b', 'c'])
   True
   >>> ['b', 'c'] |should| include_in_any_order(['b', 'c'])
   True
   >>> ['b', 'c'] |should_not| include_all_of(['b', 'c', 'a'])
   True
   >>> ['b', 'c'] |should_not| include_in_any_order(['b', 'c', 'a'])
   True


**include_any_of**

Checks if an iterable includes any element of another.::

    >>> [1, 2, 3] |should| include_any_of([3, 4, 5])
    True
    >>> (1,) |should| include_any_of([4, 6, 3, 1, 9, 7])
    True


**respond_to**

Checks if an object has a given attribute or method.::

    >>> 1.1 |should| respond_to('real')
    True

    >>> class Foo:
    ...     def __init__(self):
    ...         self.foobar = 10
    ...     def bar(self): pass
    >>> Foo() |should| respond_to('foobar')
    True
    >>> Foo() |should| respond_to('bar')
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

