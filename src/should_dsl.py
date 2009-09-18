class Should(object):

    def __init__(self, negate=False, have=False):
        self._negate = negate
        self._have = have
        self._matchers_by_name = dict()
        self.__set_default_matcher()

    def _evaluate(self, value):
        if self._negate:
            return not value
        return value

    def _negate_str(self):
        if not self._negate:
            return 'not '
        return ''

    def __ror__(self, lvalue):
        self._lvalue = lvalue
        return self

    def __or__(self, rvalue):
        self._rvalue = rvalue
        return self._check_expectation()

    def __set_default_matcher(self):
        '''The default behavior for a should object, called on constructor'''
        if self._have:
            self._turn_into_should_have()
        else:
            self._turn_into_should_be()

    def _turn_into_should_have(self):
        self._func = lambda container, item: item in container
        self._error_message = '%s does %shave %s'

    def _turn_into_should_be(self):
        self._func = lambda x, y: x is y
        self._error_message = '%s is %s%s'

    def _make_a_copy(self, func, error_message):
        clone = Should(self._negate)
        clone._matchers_by_name = self._matchers_by_name
        clone._func = func
        clone._error_message = error_message
        return clone

    def _check_expectation(self):
        evaluation = self._evaluate(self._func(self._lvalue, self._rvalue))
        if not evaluation:
            raise ShouldNotSatisfied(self._error_message % (self._lvalue,
                                                            self._negate_str(),
                                                            self._rvalue))
        return True

    def add_matcher(self, matcher_function):
        '''Adds a new matcher.
        The function must return a tuple (or any other __getitem__ compatible object)
        containing two elements:
        [0] = a function taking one or two parameters, that will do the desired comparison
        [1] = the error message. this message must contain three %s placeholders. By example,
        "%s is %snicer than %s" can result in "Python is nicer than Ruby" or
        "Python is not nicer than Ruby" depending whether |should_be.function_name| or
        |should_not_be.function_name| be applied.
        '''
        self._matchers_by_name[matcher_function.__name__] = matcher_function

    def __getattr__(self, method_name):
        '''if it can't find method_name in the instance
           it will look in _matchers_by_name'''
        if method_name not in self._matchers_by_name:
            raise AttributeError("%s object has no matcher '%s'" % (
                self.__class__.__name__, method_name))
        matcher_function = self._matchers_by_name[method_name]
        func, error_message = matcher_function()
        return self._make_a_copy(func, error_message)


class ShouldNotSatisfied(AssertionError):
    '''Extends AssertionError for unittest compatibility'''

should_be = Should(negate=False)
should_not_be = Should(negate=True)
should_have = Should(negate=False, have=True)
should_not_have = Should(negate=True, have=True)

def matcher(matcher_function):
    '''Create customer should_be matchers. We recommend you use it as a decorator'''
    for should_object in (should_be, should_not_be, should_have, should_not_have):
        should_object.add_matcher(matcher_function)
    return matcher_function

import matchers

