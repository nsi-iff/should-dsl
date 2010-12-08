=============================================================
Should-DSL: Improve readability for should-style expectations
=============================================================

The goal of *Should-DSL* is to write should expectations in Python as clear and readable as possible, using **"almost"** natural language (limited - sometimes - by the Python language constraints).

In order to use this DSL, you need to import ``should`` and ``should_not`` objects from ``should_dsl`` module.

For example::

    >>> from should_dsl import should

    >>> 1 |should| equal_to(1)
    >>> 'should' |should| include('oul')
    >>> 3 |should| be_into([0, 1, 2])
    Traceback (most recent call last):
    ...
    ShouldNotSatisfied: 3 is not into [0, 1, 2]


The ``equal_to`` matcher verifies object equality. If you want to ensure identity, you must use ``be`` as matcher::

    >>> 2 |should| be(2)


A nice example of exceptions would be::

    >>> def raise_zerodivisionerror():
    ...     return 1/0
    >>> raise_zerodivisionerror |should| throw(ZeroDivisionError)


``should`` has a negative version: ``should_not``::

    >>> from should_dsl import should_not

    >>> 2 |should_not| be_into([1, 3, 5])
    >>> 'should' |should_not| include('oul')
    Traceback (most recent call last):
    ...
    ShouldNotSatisfied: 'should' does include 'oul'

