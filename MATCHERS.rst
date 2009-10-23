Available Matchers
==================

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
- should_be
- should_have
- thrown_by


Examples of use
===============
There are some usages of Should-DSL below (it is assumed you have imported the matchers from should_dsl package)::

    >>> [1, 2, 3] |should_have.all_of| [2, 3]
    
    >>> [1, 2, 3] |should_have.any_of| [1, 2]

    >>> 'hello world' |should_be.ended_with| 'world'

    >>> 1 |should_be.equal_to| 1

    >>> 1 |should_be.greater_than_or_equal_to| 0.9

    >>> 1 |should_be.greater_than| 0.9

    >>> [1, 2, 3] |should_have.in_any_order| [3, 1]

    >>> 1 |should_be.into| [1,2,3]

    >>> object() |should_be.kind_of| object

    >>> 0.9 |should_be.less_than_or_equal_to| 1

    >>> 0.9 |should_be.less_than| 1

    >>> 'Hello World' |should_be.like| r'Hello W.+'

    >>> 1 |should_be| 1
    
    >>> [1,2,3] |should_have| 1
    
    >>> ZeroDivisionError |should_be.thrown_by| divide_one_by_zero

