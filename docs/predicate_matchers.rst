Predicate matchers
------------------

Predicate matchers are the matchers work with boolean methods and attributes, to give users more freedom to write more readable specifications.

Should-DSL supports predicate matchers on attributes::

    >>> from should_dsl import should
    >>> class Foo(object):
    ...     def __init__(self, is_valid):
    ...         self.valid = is_valid
    >>> Foo(is_valid=True) |should| be_valid


And methods::

    >>> class Person(object):
    ...    def __init__(self, money_in_wallet):
    ...        self._money_in_wallet = money_in_wallet
    ...    def rich(self):
    ...        return self._money_in_wallet > 10000
    ...
    >>> john = Person(money_in_wallet=999999999)
    >>> john |should| be_rich



    >>> class House(object):
    ...     def __init__(self, kind):
    ...         self._kind = kind
    ...     def made_of(self, kind):
    ...         return self._kind.upper() == kind.upper()
    >>> house = House('Wood')
    >>> house |should| be_made_of('wood')
    >>> house |should| be_made_of('stone')
    Traceback (most recent call last):
    ...
    ShouldNotSatisfied: expected made_of('stone') to return True, got False
