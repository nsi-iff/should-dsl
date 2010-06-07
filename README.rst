Should-DSL: Improved readability for should-style expectations
==============================================================

The goal of *Should-DSL* is to write should expectations in Python as clear and readable as possible, using **"almost"** natural language (limited - sometimes - by the Python language constraints).

For using this DSL, you need to import the should and should_not objects from should_dsl module, or import all from should_dsl.

For example::

    >>> from should_dsl import should

    >>> 1 |should| equal_to(1)
    True
    >>> 'should' |should| include('oul')
    True
    >>> 3 |should| be_into([0, 1, 2])
    Traceback (most recent call last):
    ...
    ShouldNotSatisfied: 3 is not into [0, 1, 2]


The *equal_to* matcher verifies object equality. If you want to ensure identity, you must use *be* as matcher::

    >>> 2 |should| be(2)
    True


A nice example of exceptions would be::

    >>> def raise_zerodivisionerror():
    ...     return 1/0
    >>> raise_zerodivisionerror |should| throw(ZeroDivisionError)
    True


*should* has a negative version::

    >>> from should_dsl import should_not

    >>> 2 |should_not| be_into([1, 3, 5])
    True
    >>> 'should' |should_not| include('oul')
    Traceback (most recent call last):
    ...
    ShouldNotSatisfied: should does include oul



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


**change**

Checks for changes on the result of a given function, method or lambda.

::

    >>> class Box(object):
    ...     def __init__(self):
    ...         self.items = []
    ...     def add_items(self, *items):
    ...         for item in items:
    ...             self.items.append(item)
    ...     def item_count(self):
    ...         return len(self.items)
    ...     def clear(self):
    ...         self.items = []
    >>> box = Box()
    >>> box.add_items(5, 4, 3)
    >>> box.clear |should| change(box.item_count)
    True
    >>> box.clear |should_not| change(box.item_count)
    True

If the function or method has parameters, it must be called within a lambda or using a tuple. The following ways are both equivalent::

    >>> (lambda: box.add_items(1, 2, 3)) |should| change(box.item_count)
    True
    >>> (box.add_items, 1, 2, 3) |should| change(box.item_count)
    True

*change* also works given an arbitrary change count::

    >>> box.clear()
    >>> box.add_items(1, 2, 3)
    >>> box.clear |should| change(box.item_count).by(-3)
    True
    >>> box.add_items(1, 2, 3)
    >>> box.clear |should| change(box.item_count).by(-2)
    Traceback (most recent call last):
    ...
    ShouldNotSatisfied: result should have changed by -2, but was changed by -3

*change* has support for maximum and minumum with *by_at_most* and *by_at_least*::

    >>> (box.add_items, 1, 2, 3) |should| change(box.item_count).by_at_most(3)
    True
    >>> (box.add_items, 1, 2, 3) |should| change(box.item_count).by_at_most(2)
    Traceback (most recent call last):
    ...
    ShouldNotSatisfied: result should have changed by at most 2, but was changed by 3

    >>> (box.add_items, 1, 2, 3) |should| change(box.item_count).by_at_least(3)
    True
    >>> (box.add_items, 1, 2, 3) |should| change(box.item_count).by_at_least(4)
    Traceback (most recent call last):
    ...
    ShouldNotSatisfied: result should have changed by at least 4, but was changed by 3


And, finally, *change* supports specifying the initial and final values or only the final one::

    >>> box.clear()
    >>> (box.add_items, 1, 2, 3) |should| change(box.item_count)._from(0).to(3)
    True
    >>> box.clear |should| change(box.item_count).to(0)
    True
    >>> box.clear |should| change(box.item_count).to(0)
    Traceback (most recent call last):
    ...
    ShouldNotSatisfied: result should have been changed to 0, but is now 0



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


Custom matchers
---------------

Extending the DSL with custom matchers is very easy. For simple matchers, a decorated function is enough. The function name must be the name of the matcher. The function must have no parameters and it must return a tuple containing two elements. The first one is the function (or lambda), receiving two parameters, to be run for the comparison, and the second is the failure message. The failure message must have three %s placeholders. The first and the third for, respectively, the actual and expected values. Second %s is a placeholder for a 'not ' string for a failed should_not, or an empty string for a failed should. In the example, when should fails, a message can be "4 is not the square root of 9"; in another way, if the fail is in a should_not, the message could be "3 is the square root of 9", if the expectation was *3 \|should_not\| be_the_square_root_of(9)*. The example is below::

    >>> from should_dsl import matcher

    >>> @matcher
    ... def be_the_square_root_of():
    ...     import math
    ...     return (lambda x, y: x == math.sqrt(y), "%s is %sthe square root of %s")

    >>> 3 |should| be_the_square_root_of(9)
    True
    >>> 4 |should| be_the_square_root_of(9)
    Traceback (most recent call last):
    ...
    ShouldNotSatisfied: 4 is not the square root of 9


If your custom matcher has a more complex behaviour, or if both should and should_not messages differ, you can create custom matchers as classes. In fact, classes as matchers are the preferred way to create matchers, being function matchers only a convenience for simple cases.

Below is an example of the square root matcher defined as a class::

    >>> import math
    >>> @matcher
    ... class SquareRoot(object):
    ...
    ...     name = 'be_the_square_root_of'
    ...
    ...     def __call__(self, radicand):
    ...         self._radicand = radicand
    ...         return self
    ...
    ...     def match(self, actual):
    ...         self._actual = actual
    ...         self._expected = math.sqrt(self._radicand)
    ...         return self._actual == self._expected
    ...
    ...     def message_for_failed_should(self):
    ...         return 'expected %s to be the square root of %s, got %s' % (
    ...             self._actual, self._radicand, self._expected)
    ...
    ...     def message_for_failed_should_not(self):
    ...         return 'expected %s not to be the square root of %s' % (
    ...             self._actual, self._radicand)
    ...
    >>> 3 |should| be_the_square_root_of(9)
    True
    >>> 4 |should| be_the_square_root_of(9)
    Traceback (most recent call last):
    ...
    ShouldNotSatisfied: expected 4 to be the square root of 9, got 3.0
    >>> 2 |should_not| be_the_square_root_of(4.1)
    True
    >>> 2 |should_not| be_the_square_root_of(4)
    Traceback (most recent call last):
    ...
    ShouldNotSatisfied: expected 2 not to be the square root of 4


A matcher class must fill the following requirements:

- a class attribute called *name* containing the desired name for the matcher;
- a *match(actual)* method receiving the actual value of the expectation as a parameter (e.g., in
  *2 \|should\| equal_to(3)* the actual is 2 and the expected is 3). This method should return
  the boolean result of the desired comparison;
- two methods, called *message_for_failed_should* and *message_for_failed_should_not* for returning
  the failure messages for, respectively, should and should_not.

The most common way the expected value is inject to the matcher is through making the matcher
callable. Thus, the matcher call can get the expected value and any other necessary or optional
information. By example, the *close_to* matcher's *__call__()* method receives 2 parameters:
the expected value and a delta. Once a matcher is a regular Python object, any Python can be used.
In *close_to*, delta can be used as a named parameter for readability purposes.


Deprecated usage
----------------

All *should-dsl* matchers also support a deprecated form, so::

    >>> 3 |should_not| equal_to(2.99)
    True

can be written as::

    >>> 3 |should_not.equal_to| 2.99
    True

Besides, should_dsl module offers should_be, should_have (and their negative counterparts) to be used with no matchers, as::

    >>> from should_dsl import *

    >>> [1, 2] |should_have| 1
    True
    >>> 1 |should_be| 1
    True

This syntax for writing expectations was changed because the requirement to have a single "right value" is a limitation to future improvements.

We don't plan to remove the deprecated syntax in the near future, but we discourage its use from now.



Should-DSL with unittest
========================

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

