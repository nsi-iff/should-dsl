=============================================================
Should-DSL: Improve readability for should-style expectations
=============================================================

The goal of *Should-DSL* is to write should expectations in Python as clear and readable as possible, using **"almost"** natural language (limited - sometimes - by the Python language constraints).

For using this DSL, you need to import ``should`` and ``should_not`` objects from ``should_dsl`` module, or import everything from ``should_dsl``.

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


The ``equal_to`` matcher verifies object equality. If you want to ensure identity, you must use ``be`` as matcher::

    >>> 2 |should| be(2)
    True


A nice example of exceptions would be::

    >>> def raise_zerodivisionerror():
    ...     return 1/0
    >>> raise_zerodivisionerror |should| throw(ZeroDivisionError)
    True


``should`` has a negative version: ``should_not``::

    >>> from should_dsl import should_not

    >>> 2 |should_not| be_into([1, 3, 5])
    True
    >>> 'should' |should_not| include('oul')
    Traceback (most recent call last):
    ...
    ShouldNotSatisfied: 'should' does include 'oul'



Deprecated usage
================

All Should-DSL releases before 2.0 are now deprecated, but we still support the old style, but it will be removed soon and we discourage you to use the old style. Old style usage like::

    >>> 3 |should_not.equal_to| 2.99
    True

should be written as::

    >>> 3 |should_not| equal_to(2.99)
    True


Besides, ``should_dsl`` module offers ``should_be``, ``should_have`` (and their negative counterparts) to be used with no matchers - all old styles -, as::

    >>> from should_dsl import *

    >>> [1, 2] |should_have| 1
    True
    >>> 1 |should_be| 1
    True

This syntax for writing expectations was changed because the requirement to have a single "right value" had been a limition to right new matchers and add new enhancements to Should-DSL and you should update the code you use the old style, because we plan to remove them soon.
