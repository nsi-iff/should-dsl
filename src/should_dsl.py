'''
    This is a simple experiment with internal DSLs
    using Python Language.
    The goal is to write some kind of BDD.


    Here is the point to try make everything
    as transparent as possible
    >>> _ = DSLObject

    Take a look at the doctests (doctests folder)
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
        negate = ''
        if self._negate == False:
            negate = 'not '
        return self.fail("%s is %sNone" % (self._value, negate))

    @property
    def true(self):
        if self._negate_or_not(self._value):
            return self.success
        negate = ''
        if self._negate == False:
            negate = 'not '
        return self.fail("%s is %sTrue" % (self._value, negate))

    @property
    def false(self):
        if self._negate_or_not(self._value) == False:
            return self.success
        negate = ''
        if self._negate == False:
            negate = 'not '
        return self.fail("%s is %sFalse" % (self._value, negate))

    def equal_to(self, value):
        if self._negate_or_not(value == self._value):
            return self.success
        negate = ''
        if self._negate == False:
            negate = 'not '
        return self.fail("%s is %sequal to %s" % (self._value, negate, value))

    def into(self, container):
        if self._negate_or_not(self._value in container):
            return self.success
        negate = ''
        if self._negate == False:
            negate = 'not '
        return self.fail("%s is %sinto %s" % (self._value, negate, container))

    def have(self, value):
        if self._negate_or_not(value in self._value):
            return self.success
        negate = ''
        if self._negate == False:
            negate = 'not '
        return self.fail("%s does %shave %s" % (self._value, negate, value))

    def thrown_by(self, callable_object, *args, **kw):
        try:
            callable_object(*args, **kw)
            if self._negate == False:
                return self.fail("%s is not thrown by %s" % (str(self._value),
                                                             callable_object))
        except self._value:
            if self._negate == True:
                return self.fail("%s is thrown by %s" % (str(self._value),
                                                             callable_object))
        return True
 

if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS)
