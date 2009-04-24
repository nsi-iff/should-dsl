'''
    This is a simple experiment with internal DSLs
    using Python Language.
    The goal is to write some kind of BDD.


    Here is the point to try make everything
    as transparent as possible
    >>> _ = DSLObject


    >>> _(1).should_be.equal_to(1)
    True
    >>> _(2).should_be.equal_to(3)
    Traceback (most recent call last):
        ...
    ShouldNotSatisfied: 2 is not equal to 3
    >>> _(1).should_not_be.equal_to(2)
    True
    >>> name = 'dsl'
    >>> _(name).should_be.equal_to('dsl')
    True

    >>> _(None).should_be.none
    True
    >>> _('Specification').should_not_be.none
    True

    >>> _(1).should_be.into([1,2,3])
    True
    >>> _(5).should_not_be.into([1,2,3])
    True

    >>> _([1,2,3]).should_have(1)
    True
    >>> _([1,2]).should_have(3)
    Traceback (most recent call last):
        ...
    ShouldNotSatisfied: [1, 2] does not have 3
    >>> _([1,2]).should_not_have(3)
    True

    >>> _('spec' is not 'SPEC').should_be.true
    True
    >>> _('spec' is not 'SPEC').should_not_be.true
    Traceback (most recent call last):
        ...
    ShouldNotSatisfied: True is not True
    >>> _('spec' is not 'SPEC').should_not_be.false
    True


    >>> def divide_one_by_zero():
    ...    return 1 / 0
    >>> def divide_x_by_y(x, y):
    ...     return x / y
    >>> _(ZeroDivisionError).should_be.thrown_by(divide_one_by_zero)
    True
    >>> _(ZeroDivisionError).should_not_be.thrown_by(divide_one_by_zero)
    Traceback (most recent call last):
        ...
    ShouldNotSatisfied: ...ZeroDivisionError... is not thrown by
    <function divide_one_by_zero at ...>

    >>> _(ZeroDivisionError).should_be.thrown_by(divide_x_by_y, 5, 0)
    True

'''

class DSLCommon(object):
    def __init__(self, value, negate=False):
        self._value = value
        self._negate = negate

    def _negate_or_not(self, value):
        if self._negate:
            return not value
        return value


class DSLObject(object):
    def __init__(self, value):
        self._value = value

    @property
    def should_be(self):
        return Should(self._value, negate=False)
    
    @property
    def should_not_be(self):
        return Should(self._value, negate=True)

    def should_have(self, value):
        return Should(self._value, negate=False).have(value)

    def should_not_have(self, value):
        return Should(self._value, negate=True).have(value)


class ShouldNotSatisfied(Exception):
    '''it's raised when some should is not satisfied'''


class Should(DSLCommon):
    @property
    def success(self):
        return True

    def fail(self, message):
        raise ShouldNotSatisfied(message)
        return False

    @property
    def none(self):
        if self._negate_or_not(self._value == None):
            return self.success
        return self.fail("%s is None" % self._value)

    @property
    def true(self):
        if self._negate_or_not(self._value):
            return self.success
        return self.fail("%s is not True" % self._value)

    @property
    def false(self):
        if self._negate_or_not(self._value) == False:
            return self.success
        return self.fail("%s is False" % self._value)

    def equal_to(self, value):
        if self._negate_or_not(value == self._value):
            return self.success
        return self.fail("%s is not equal to %s" % (self._value, value))

    def into(self, container):
        if self._negate_or_not(self._value in container):
            return self.success
        return self.fail("%s is not in %s!" % (self._value, container))

    def have(self, value):
        if self._negate_or_not(value in self._value):
            return self.success
        return self.fail("%s does not have %s" % (self._value, value))

    def thrown_by(self, callable_object, *args, **kw):
        try:
            callable_object(*args, **kw)
            if self._negate == False:
                return self.fail("%s is not thrown by %s" % (str(self._value),
                                                             callable_object))
        except self._value:
            if self._negate == True:
                return self.fail("%s is not thrown by %s" % (str(self._value),
                                                             callable_object))
        return True
 

if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS)
