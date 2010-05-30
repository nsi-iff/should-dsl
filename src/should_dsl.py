import sys

class Should(object):

    def __init__(self, negate=False, have=False):
        self._negate = negate
        self._have = have
        self._matchers_by_name = dict()
        self.__set_default_matcher()
        self._identifiers_named_equal_matchers = dict()

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
        self._create_function_matchers()
        return self

    def __or__(self, rvalue):
        self._destroy_function_matchers()
        if not isinstance(rvalue, _Matcher):
            self._rvalue = rvalue
            return self._check_expectation()
        else:
            self._rvalue = rvalue.arg
            return self._make_a_copy(rvalue.function,
                rvalue.error_message, copy_values=True)._check_expectation()

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

    def _make_a_copy(self, func, error_message, copy_values=False):
        clone = Should(self._negate)
        clone._matchers_by_name = self._matchers_by_name
        clone._func = func
        clone._error_message = error_message
        if copy_values:
          if hasattr(self, '_lvalue'):
              clone._lvalue = self._lvalue
          if hasattr(self, '_rvalue'):
              clone._rvalue = self._rvalue
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

    def _create_function_matchers(self):
        f_globals = sys._getframe(2).f_globals
        self._save_clashed_identifiers(f_globals)
        self._put_matchers_on_namespace(f_globals)

    def _save_clashed_identifiers(self, f_globals):
        predicate_matcher_names = ['be_' + attr_name for attr_name in dir(self._lvalue) if not attr_name.startswith('_')]
        for matcher_name in self._matchers_by_name.keys() + predicate_matcher_names:
            if f_globals.has_key(matcher_name):
                self._identifiers_named_equal_matchers[matcher_name] = f_globals[matcher_name]

    def _put_matchers_on_namespace(self, f_globals):
        self._put_regular_matchers_on_namespace(f_globals)
        self._put_predicate_matchers_on_namespace(f_globals)

    def _put_regular_matchers_on_namespace(self, f_globals):
        for matcher_name, matcher_function in self._matchers_by_name.iteritems():
            matcher_function = self._matchers_by_name[matcher_name]
            func, error_message = matcher_function()
            f_globals[matcher_name] = _Matcher(func, error_message)

    def _put_predicate_matchers_on_namespace(self, f_globals):
        attr_names = [attr_name for attr_name in dir(self._lvalue) if not attr_name.startswith('_')]
        for attr_name in attr_names:
            matcher = _Matcher(lambda x, y: getattr(x, y), "%s is %s%s", attr_name)
            f_globals['be_' + attr_name] = matcher

    def _destroy_function_matchers(self):
        f_globals = sys._getframe(2).f_globals
        self._remove_matchers_from_namespace(f_globals)
        self._put_original_identifiers_back(f_globals)

    def _remove_matchers_from_namespace(self, f_globals):
        self._remove_regular_matchers_from_namespace(f_globals)
        self._remove_predicate_matchers_from_namespace(f_globals)

    def _remove_regular_matchers_from_namespace(self, f_globals):
        for matcher_name in self._matchers_by_name.keys():
            del f_globals[matcher_name]

    def _remove_predicate_matchers_from_namespace(self, f_globals):
        attr_names = [attr_name for attr_name in dir(self._lvalue) if not attr_name.startswith('_')]
        for attr_name in attr_names:
            del f_globals['be_' + attr_name]

    def _put_original_identifiers_back(self, f_globals):
        for attr_name, attr_ref in self._identifiers_named_equal_matchers.iteritems():
            f_globals[attr_name] = attr_ref
        self._identifiers_named_equal_matchers.clear()

    # deprecated behaviour
    def __getattr__(self, method_name):
        if method_name not in self._matchers_by_name:
            raise AttributeError("%s object has no matcher '%s'" % (
                self.__class__.__name__, method_name))
        matcher_function = self._matchers_by_name[method_name]
        func, error_message = matcher_function()
        return self._make_a_copy(func, error_message)


class _Matcher(object):
    def __init__(self, function, error_message, arg=None):
        self.function = function
        self.error_message = error_message
        self.arg = arg

    def __call__(self, arg):
        self.arg = arg
        return self


class ShouldNotSatisfied(AssertionError):
    '''Extends AssertionError for unittest compatibility'''


should = Should(negate=False)
should_not = Should(negate=True)

# should objects for backwards compatibility
should_be = should
should_not_be = should_not
should_have = Should(negate=False, have=True)
should_not_have = Should(negate=True, have=True)

def matcher(matcher_function):
    '''Create customer should_be matchers. We recommend you use it as a decorator'''
    for should_object in (should, should_not, should_have, should_not_have):
        should_object.add_matcher(matcher_function)
    return matcher_function

import matchers

