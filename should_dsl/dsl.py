import sys
import re
from types import FunctionType


_predicate_regexes = set(['is_(.+)', 'is(.+)'])


class Should(object):

    def __init__(self, negate=False):
        self._negate = negate
        self._matchers_by_name = dict()
        self._identifiers_named_equal_matchers = dict()
        self._outer_frame = None

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
        self._rvalue = rvalue
        return self._check_expectation()

    def _check_expectation(self):
        if not self._evaluate(self._rvalue.match(self._lvalue)):
            raise ShouldNotSatisfied(self._negate and \
                self._rvalue.message_for_failed_should_not() or \
                self._rvalue.message_for_failed_should())


    def _destroy_function_matchers(self):
        self._outer_frame = sys._getframe(2).f_globals
        self._remove_matchers_from_namespace()
        self._put_original_identifiers_back()

    def _remove_matchers_from_namespace(self):
        self._remove_regular_matchers_from_namespace()
        self._remove_predicate_matchers_from_namespace()

    def _remove_regular_matchers_from_namespace(self):
        f_globals = self._outer_frame
        for matcher_name in list(self._matchers_by_name.keys()):
            del f_globals[matcher_name]

    def _remove_predicate_matchers_from_namespace(self):
        f_globals = self._outer_frame
        for attr_name in dir(self._lvalue):
            matcher = 'be_%s' % attr_name
            if matcher in f_globals:
                del f_globals[matcher]

    def _put_original_identifiers_back(self):
        f_globals = self._outer_frame
        for attr_name, attr_ref in self._identifiers_named_equal_matchers.items():
            f_globals[attr_name] = attr_ref
        self._identifiers_named_equal_matchers.clear()


    def _create_function_matchers(self):
        self._outer_frame = sys._getframe(2).f_globals
        self._save_clashed_identifiers()
        self._put_matchers_on_namespace()

    def _save_clashed_identifiers(self):
        f_globals = self._outer_frame
        predicate_matcher_names = ['be_' + attr_name for attr_name in dir(self._lvalue) if not attr_name.startswith('_')]
        for matcher_name in list(self._matchers_by_name.keys()) + predicate_matcher_names:
            if matcher_name in f_globals:
                self._identifiers_named_equal_matchers[matcher_name] = f_globals[matcher_name]

    def _put_matchers_on_namespace(self):
        self._put_regular_matchers_on_namespace()
        self._put_predicate_matchers_on_namespace()

    def _put_regular_matchers_on_namespace(self):
        f_globals = self._outer_frame
        for matcher_name, matcher_function in self._matchers_by_name.items():
            matcher_function = self._matchers_by_name[matcher_name]
            matcher = matcher_function()
            self._inject_negate_information(matcher)
            f_globals[matcher_name] = matcher

    def _inject_negate_information(self, matcher):
        try:
            matcher.run_with_negate = self._negate
        except AttributeError:
            pass

    def _put_predicate_matchers_on_namespace(self):
        f_globals = self._outer_frame
        predicate_and_matcher_names = []
        public_names = self._get_all_public_attr_names(self._lvalue)
        for attr_name in public_names:
            for regex in _predicate_regexes:
                r = re.match(regex, attr_name)
                if r:
                    predicate_and_matcher_names.append((r.group(1), attr_name))
        predicate_and_matcher_names += [(attr_name, attr_name) for attr_name in public_names]
        for predicate_name, attr_name in predicate_and_matcher_names:
            f_globals['be_' + predicate_name] = _PredicateMatcher(attr_name)


    def add_matcher(self, matcher_object):
        if (hasattr(matcher_object, 'func_name') or
            isinstance(matcher_object, FunctionType)):
            function, message, not_for_should, not_for_should_not = \
                self._process_custom_matcher_function(matcher_object)
            class GeneratedMatcher(object):
                name = matcher_object.__name__
                def __init__(self):
                    self._function, self._message = function, message
                def __call__(self, arg):
                    self._arg = arg
                    return self
                def match(self, value):
                    self._value = value
                    return self._function(self._value, self._arg)
                def message_for_failed_should(self):
                    return self._build_message(not_for_should)
                def message_for_failed_should_not(self):
                    return self._build_message(not_for_should_not)
                def _build_message(self, not_):
                    try:
                        return self._message % (self._value, not_, self._arg)
                    except TypeError:
                        return self._message % {
                            'expected': self._arg,
                            'not': not_,
                            'actual': self._value}

            matcher_object = GeneratedMatcher
            name = GeneratedMatcher.name
        else:
            name = matcher_object.name
        self._ensure_matcher_init_doesnt_have_arguments(matcher_object)
        self._matchers_by_name[name] = matcher_object

    def _ensure_matcher_init_doesnt_have_arguments(self, matcher_object):
        try:
            matcher_object()
        except TypeError:
            e = sys.exc_info()[1]
            if str(e).startswith('__init__() takes exactly'):
                raise TypeError('matcher class constructor cannot have arguments')
            else:
                raise

    def _get_all_public_attr_names(self, obj):
        return [attr_name for attr_name in dir(obj) if not attr_name.startswith('_')]

    def _process_custom_matcher_function(self, matcher_function):
        values = matcher_function()
        function, message = values[0:2]
        if len(values) <= 2:
            nots = ('not ', '')
        else:
            nots = values[2]._negate and ('', 'not ') or ('not ', '')
        return (function, message) + nots

    def add_aliases(self, **aliases):
        for name, alias in aliases.items():
            matcher = self._matchers_by_name[name]
            self._matchers_by_name[alias] = matcher


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

    def _is_method(self, object_):
        return (hasattr(object_, 'im_func') or hasattr(object_, '__func__'))

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

def matcher(matcher_object):
    '''Adds given matcher to should objects. We recommend you use it as a decorator'''
    should.add_matcher(matcher_object)
    should_not.add_matcher(matcher_object)
    return matcher_object

def add_predicate_regex(regex):
    _predicate_regexes.update([regex])

def matcher_configuration(verifier, message, word_not_for=should_not):
    return (verifier, message, word_not_for)

def aliases(**kwargs):
    should.add_aliases(**kwargs)
    should_not.add_aliases(**kwargs)

