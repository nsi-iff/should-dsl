import sys
import native_matchers

class Should(object):

    def __init__(self, negate=False, be=False, have=False):
        self._negate = negate
        self._have = have
        self._matchers_by_name = dict()
        if have or be:
            self._set_default_matcher()
        self._identifiers_named_equal_matchers = dict()

    def _evaluate(self, value):
        if self._negate:
            return not value
        return value

    def __ror__(self, lvalue):
        self._lvalue = lvalue
        self._create_function_matchers()
        return self

    def __or__(self, rvalue):
        self._destroy_function_matchers()
        if not hasattr(self, '_old_style_call'):
            self._rvalue = rvalue
            if not hasattr(rvalue, 'match'):
                self._convert_deprecated_style(rvalue)
        else:
            self._convert_deprecated_style(rvalue)
        return self._check_expectation()

    def _check_expectation(self):
        if not self._evaluate(self._rvalue.match(self._lvalue)):
            raise ShouldNotSatisfied(self._negate and self._rvalue.message_for_failed_should_not() or self._rvalue.message_for_failed_should())
        return True

    def add_matcher(self, matcher_object):
        if hasattr(matcher_object, 'func_name'):
            func, message = matcher_object()
            class GeneratedMatcher(object):
                name = matcher_object.func_name
                def __init__(self):
                    self._func, self._message = func, message
                def __call__(self, arg):
                    self.arg = arg
                    return self
                def match(self, value):
                    self._value = value
                    return self._func(self._value, self.arg)
                def message_for_failed_should(self):
                    return self._message % (self._value, "not ", self.arg)
                def message_for_failed_should_not(self):
                    return self._message % (self._value, "", self.arg)
            matcher_object = GeneratedMatcher
            name = GeneratedMatcher.name
        else:
            name = matcher_object.name
        self._validate_matcher(matcher_object)
        self._matchers_by_name[name] = matcher_object

    def _validate_matcher(self, matcher_object):
        try:
            matcher_object()
        except TypeError, e:
            if str(e).startswith('__init__() takes exactly'):
                raise TypeError('matcher class constructor cannot have arguments')
            else:
                raise

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
            f_globals[matcher_name] = matcher_function()

    def _put_predicate_matchers_on_namespace(self, f_globals):
        attr_names = [attr_name for attr_name in dir(self._lvalue) if not attr_name.startswith('_')]
        for attr_name in attr_names:
            matcher = _PredicateMatcher(attr_name)
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
        return self._prepare_to_receive_rvalue(method_name)

    def _prepare_to_receive_rvalue(self, method_name):
        should = Should(negate=self._negate, have=self._have, be=not self._have)
        should._matchers_by_name = self._matchers_by_name
        should._old_style_call = True
        should._matcher = self._matchers_by_name[method_name]
        return should

    def _set_default_matcher(self):
        '''The default behavior for a should object, called on constructor'''
        if self._have:
            self._turn_into_should_have()
        else:
            self._turn_into_should_be()

    def _turn_into_should_have(self):
        self._matcher = native_matchers.NativeHaveMatcher

    def _turn_into_should_be(self):
        self._matcher = native_matchers.NativeBeMatcher

    def _convert_deprecated_style(self, rvalue):
        self._rvalue = self._matcher()
        self._rvalue.arg = rvalue


class _PredicateMatcher(object):

    def __init__(self, attr_name):
        self._attr_name = attr_name

    def __call__(self, *params):
        self._params = params
        return self

    def match(self, value):
        self._value = value
        attr_value = getattr(self._value, self._attr_name)
        if self._is_method(attr_value):
            if self._has_param():
                attr_value = attr_value(*self._params)
            else:
                attr_value = attr_value()
        return attr_value

    def message_for_failed_should(self):
        return "expected %s to %s True, got False" % (
            self._display_attr(self._attr_name),
            self._display_verb(self._attr_name))

    def message_for_failed_should_not(self):
        return "expected %s to %s False, got True" % (
            self._display_attr(self._attr_name),
            self._display_verb(self._attr_name))

    def _is_method(self, objekt):
        return hasattr(objekt, 'im_func')

    def _display_attr(self, attr_name):
        if self._is_method(getattr(self._value, attr_name)):
            if self._has_param():
                repr_params = [repr(param) for param in self._params]
                param = ", ".join(repr_params)
            else:
                param = ""
            return "%s(%s)" % (attr_name, param)
        else:
            return attr_name

    def _display_verb(self, attr_name):
        return self._is_method(getattr(self._value, attr_name)) \
            and "return" or "be"

    def _has_param(self):
        return hasattr(self, '_params')

class ShouldNotSatisfied(AssertionError):
    '''Extends AssertionError for unittest compatibility'''


should = Should(negate=False)
should_not = Should(negate=True)

# should objects for backwards compatibility
should_be = Should(be=True)
should_not_be = Should(negate=True, be=True)
should_have = Should(negate=False, have=True)
should_not_have = Should(negate=True, have=True)

def matcher(matcher_object):
    '''Create customer should_be matchers. We recommend you use it as a decorator'''
    should_objects = (should, should_not, should_be, should_not_be, should_have,
                      should_not_have)
    for should_object in should_objects:
        should_object.add_matcher(matcher_object)
    return matcher_object

import matchers

