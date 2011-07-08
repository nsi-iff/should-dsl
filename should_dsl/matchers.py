import re
import sys
from decimal import Decimal
from difflib import unified_diff
from should_dsl import matcher
from should_dsl.backwardscompat import string_types


class Be(object):

    name = 'be'

    def __call__(self, expected):
        self._expected = expected
        return self

    def match(self, actual):
        self._actual = actual
        return self._actual is self._expected

    def message_for_failed_should(self):
        return "%r was expected to be %r" % (self._actual, self._expected)

    def message_for_failed_should_not(self):
        return "%r was not expected to be %r" % (self._actual, self._expected)


matcher(Be)


class EqualTo(object):

    name = 'equal_to'

    def __call__(self, expected, diff=False, case_sensitive=True):
        self._expected = expected
        self._make_diff = diff
        self._case_sensitive = case_sensitive
        return self

    def match(self, actual):
        self._actual = actual
        self._diff = ''

        if not self._case_sensitive:
            self._prepare_strings_to_case_insensitive()

        if not self._actual == self._expected:
            if isinstance(self._expected, string_types) and isinstance(self._actual, string_types) and self._make_diff:
                self._prepare_strings_to_diff()
                diff_generator = unified_diff(self._actual, self._expected, fromfile='actual', tofile='expected')
                for line in diff_generator:
                    self._diff += line
            return False
        return True

    def _prepare_strings_to_case_insensitive(self):
            self._expected = self._expected.lower()
            self._actual = self._actual.lower()

    def _prepare_strings_to_diff(self):
            self._actual = self._actual.splitlines(True)
            self._expected = self._expected.splitlines(True)

    def message_for_failed_should(self):
        default_message = "%r is not equal to %r" % (self._actual, self._expected)
        if not self._make_diff:
            return default_message
        return "the strings are different, see the diff below:\n%s" % self._diff

    def message_for_failed_should_not(self):
        return "%r is equal to %r" % (self._actual, self._expected)

matcher(EqualTo)


@matcher
def include():
    return (lambda container, item: item in container, "%r does %sinclude %r")


@matcher
def contain():
    return (lambda container, item: item in container, "%r does %scontain %r")


@matcher
def be_into():
    return (lambda item, container: item in container, '%r is %sinto %r')


@matcher
def be_greater_than():
    return (lambda x, y: x > y, '%r is %sgreater than %r')


@matcher
def be_greater_than_or_equal_to():
    return (lambda x, y: x >= y, '%r is %sgreater than or equal to %r')


@matcher
def be_less_than():
    return (lambda x, y: x < y, '%r is %sless than %r')


@matcher
def be_less_than_or_equal_to():
    return (lambda x, y: x <= y, '%r is %sless than or equal to %r')


def check_exception(expected_exception, callable_and_possible_params):
    if getattr(callable_and_possible_params, '__getitem__', False):
        callable_object = callable_and_possible_params[0]
        params = callable_and_possible_params[1:]
    else:
        callable_object = callable_and_possible_params
        params = []

    try:
        callable_object(*params)
        return False
    except expected_exception:
        return True
    except Exception:
        return False


@matcher
def be_thrown_by():
    return (check_exception, '%r is %sthrown by %r')


class Throw:

    name = 'throw'

    def __call__(self, exception, message=None, message_regex=None):
        self._expected_message = message
        self._expected_message_regex = message_regex
        if isinstance(exception, Exception):
            self._expected_exception = exception.__class__
            if message is None and message_regex is None:
                self._expected_message = str(exception)
        else:
            self._expected_exception = exception
        return self

    def match(self, lvalue):
        self._lvalue = lvalue
        if getattr(lvalue, '__getitem__', False):
            args = lvalue[1:]
            lvalue = lvalue[0]
        else:
            args = []
        try:
            lvalue(*args)
            self._actual_exception = None
            return False
        except self._expected_exception:
            e = sys.exc_info()[1]
            self._actual_exception = self._expected_exception
            self._actual_message = str(e)
            return self._handle_expected_message() and self._handle_expected_regex()
        except Exception:
            e = sys.exc_info()[1]
            self._actual_exception = e.__class__
            return False

    def _using_message(self):
        return self._expected_message is not None

    def _using_regex(self):
        return self._expected_message_regex is not None and not self._using_message()

    def _got_exception(self):
        return hasattr(self, '_actual_exception') and self._actual_exception is not None

    def _handle_expected_message(self):
        if not self._using_message():
            return True
        return self._expected_message == self._actual_message

    def _handle_expected_regex(self):
        if not self._using_regex():
            return True
        return re.match(self._expected_message_regex, self._actual_message) is not None

    def message_for_failed_should(self):
        message = "expected to throw %r" % self._expected_exception.__name__
        if self._using_message():
            message += " with the message %r" % self._expected_message
        elif self._using_regex():
            message += " with a message that matches %r" % self._expected_message_regex
        if self._got_exception():
            message += ', got %r' % self._actual_exception.__name__
            if self._using_message():
                message += ' with %r' % self._actual_message
            elif self._using_regex():
                message += ' with no match for %r' % self._actual_message
        else:
            message += ', got no exception'
        return message

    def message_for_failed_should_not(self):
        message = "expected not to throw %r" % self._expected_exception.__name__
        if self._using_message():
            message += " with the message %r" % self._expected_message
        elif self._using_regex():
            message += " with a message that matches %r" % self._expected_message_regex
        return "%s, but got it" % message

matcher(Throw)


@matcher
def include_in_any_order():
    def contains_in_any_order(container, elements):
        for element in elements:
            if element not in container:
                return False
        return True
    return (contains_in_any_order, "%r does %sinclude in any order %r")


@matcher
def include_all_of():
    return (include_in_any_order()[0], "%r does %sinclude all of %r")


@matcher
def include_any_of():
    def include_any_of_func(container, elements):
        for element in elements:
            if element in container:
                return True
        return False
    return (include_any_of_func, "%r does %sinclude any of %r")


@matcher
def be_kind_of():
    return (lambda obj, kind: isinstance(obj, kind), "%r is %s a kind of %r")


@matcher
def be_instance_of():
    return (lambda obj, kind: isinstance(obj, kind), "%r is %s an instance of %r")


@matcher
def start_with():
    return (lambda x, y: x.startswith(y), "%r does %sstart with %r")


@matcher
def end_with():
    return (lambda x, y: x.endswith(y), "%r does %send with %r")


class BeLike(object):

    name = 'be_like'

    def __call__(self, regex, flags=0):
        self._regex = regex
        self._flags = flags
        return self

    def match(self, lvalue):
        self._lvalue = lvalue
        return re.match(self._regex, self._lvalue, self._flags) is not None

    def message_for_failed_should(self):
        return "%r is not like %r%s" % (self._lvalue, self._regex,
            self._flags and ' with given flags' or '')

    def message_for_failed_should_not(self):
        return "%r is like %r%s" % (self._lvalue, self._regex,
            self._flags and ' with given flags' or '')


matcher(BeLike)


@matcher
def equal_to_ignoring_case():
    try:
        unicode
        lower = lambda x: unicode(x, 'utf-8').lower()
    except NameError:
        # py3k is unicode by default
        lower = lambda x: x.lower()
    return (lambda x, y: lower(x) == lower(y), '%r is %sequal to %r ignoring case')


class Have(object):

    name = 'have'

    def __call__(self, count):
        self._count = count
        return self

    def __getattr__(self, collection_name):
        self._collection_name = collection_name
        self._humanized_collection_name = collection_name.replace('_', ' ')
        return self

    def match(self, lvalue):
        self._lvalue = lvalue
        if hasattr(self._lvalue, self._collection_name):
            self._collection = getattr(self._lvalue, self._collection_name)
            if not self._is_iterable(self._collection):
                if callable(self._collection):
                    self._collection = self._collection()
                    if not self._is_iterable(self._collection):
                        raise TypeError("target's '%s()' does not return an iterable" % self._collection_name)
                else:
                    raise TypeError("target's %r is not an iterable" % self._collection_name)
        elif self._is_iterable(self._lvalue):
            self._collection = self._lvalue
        elif self._is_collection_through():
            owned_by_owned, owned = self._collection_name.split('_on_')
            owned_object = self._retrieve_owned_object(self._lvalue, owned)
            owned_by_owned_object = self._retrieve_owned_object(owned_object, owned_by_owned)
            if not self._is_iterable(owned_by_owned_object):
                if callable(getattr(owned_object, owned_by_owned)):
                    raise TypeError("target's '%s()' does not return an iterable" % owned_by_owned)
                else:
                    raise TypeError("target's %r is not an iterable" % owned_by_owned)
            self._collection = owned_by_owned_object
        else:
            raise TypeError("target does not have a %r collection, nor it is an iterable" % (
                self._collection_name))
        return self._compare()

    def _retrieve_owned_object(self, object_, owned):
        owned_object = getattr(object_, owned)
        if callable(owned_object):
            owned_object = owned_object()
        return owned_object

    def _is_collection_through(self):
        splitted = self._collection_name.split('_on_')
        if len(splitted) == 1:
            return False
        owned_by_owned, owned = splitted

        if not hasattr(self._lvalue, owned):
            return False
        owned_object = self._retrieve_owned_object(self._lvalue, owned)
        return hasattr(owned_object, owned_by_owned)

    def _compare(self):
        return self._count == len(self._collection)

    def message_for_failed_should(self):
        if self.name == 'have':
            description = ''
        else:
            description = "%s " % self.name[5:].replace('_', ' ')
        return "expected %s%r %r, got %r" % (description, self._count,
            self._humanized_collection_name, len(self._collection))

    def message_for_failed_should_not(self):
        return "expected target not to %s %d %r, got %r" % (
            self.name.replace('_', ' '), self._count,
            self._humanized_collection_name, len(self._collection))

    def _is_iterable(self, objekt):
        return hasattr(objekt, '__len__')

matcher(Have)


class HaveAtLeast(Have):

    name = 'have_at_least'

    def _compare(self):
        return len(self._collection) >= self._count


matcher(HaveAtLeast)


class HaveAtMost(Have):

    name = 'have_at_most'

    def _compare(self):
        return len(self._collection) <= self._count

matcher(HaveAtMost)


class RespondTo(object):

    name = 'respond_to'

    def __call__(self, method_name):
        self._method_name = method_name
        return self

    def match(self, lvalue):
        self._lvalue = lvalue
        return hasattr(self._lvalue, self._method_name)

    def message_for_failed_should(self):
        return "expected %r to respond to %r" % (self._lvalue,
            self._method_name)

    def message_for_failed_should_not(self):
        return "expected %r not to respond to %r" % (self._lvalue,
            self._method_name)

matcher(RespondTo)


class CloseTo(object):

    name = 'close_to'

    def __call__(self, expected, delta):
        self._expected, self._delta = expected, delta
        return self

    def match(self, actual):
        self._actual = actual
        return abs(Decimal(str(self._actual)) - Decimal(str(self._expected))) <= Decimal(str(self._delta))

    def message_for_failed_should(self):
        return "expected to be close to %s (within +/- %s), got %s" % (
            self._expected, self._delta, self._actual)

    def message_for_failed_should_not(self):
        return "expected not to be close to %s (within +/- %s), got %s" % (
            self._expected, self._delta, self._actual)

matcher(CloseTo)


class Change(object):

    name = 'change'

    def __init__(self):
        self._by = None
        self._from_to = False
        self._only_to = False

    def __call__(self, verifier):
        self._verifier = self._to_callable(verifier)
        return self

    def match(self, action):
        self._action = self._to_callable(action)

        self._before_result = self._verifier()
        self._action()
        self._after_result = self._verifier()

        if self._by is not None:
            self._actual_difference = self._after_result - self._before_result
            return self._by.comparison(self._expected_difference, self._actual_difference)
        elif self._from_to:
            return self._before_result == self._from_value and self._after_result == self._to_value
        elif self._only_to:
            self._failure_on_to_initial_value = False
            if self._before_result == self._to_value:
                self._failure_on_to_initial_value = True
                return False
            else:
                return self._after_result == self._to_value
        else:
            return self._after_result != self._before_result

    def message_for_failed_should(self):
        if self._by is not None:
            return 'result should have changed %s %r, but was changed by %r' % (
                self._by.name, self._expected_difference, self._actual_difference)
        elif self._from_to:
            return 'result should have changed from %r to %r, but was changed from %r to %r' % (
                self._from_value, self._to_value, self._before_result, self._after_result)
        elif self._only_to:
            if self._failure_on_to_initial_value:
                return 'result should have been changed to %r, but is now %r' % (
                    self._to_value, self._before_result)
            else:
                return 'result should have changed to %r, but was changed to %r' % (
                    self._to_value, self._after_result)
        else:
            return 'result should have changed, but is still %r' % (
                self._before_result)

    def message_for_failed_should_not(self):
        if self._from_to:
            return 'result should not have changed from %r to %r' % (
                  self._from_value, self._to_value)
        elif self._only_to:
            return 'result should not have changed to %r' % self._to_value
        else:
            return 'should not have changed, but did change from %r to %r' % (
                self._before_result, self._after_result)

    def by(self, difference):
        self._expected_difference = difference
        self._by = Change._By(lambda exp_dif, act_dif: act_dif == exp_dif)
        return self

    def  by_at_least(self, difference):
        self._expected_difference = difference
        self._by = Change._By(lambda exp_dif, act_dif: act_dif >= exp_dif, 'at least')
        return self

    def by_at_most(self, difference):
        self._expected_difference = difference
        self._by = Change._By(lambda exp_dif, act_dif: act_dif <= exp_dif, 'at most')
        return self

    def from_(self, from_value):
        self._from_value = from_value
        self._from_to = True
        return self

    def to(self, to_value):
        self._only_to = not self._from_to
        self._to_value = to_value
        return self

    def _to_callable(self, objekt):
        if hasattr(objekt, '__call__'):
            return objekt
        type_error_message = 'parameter passed to change must be a callable or a iterable having a callable as its first element'
        if not getattr(objekt, '__getitem__', False) or not hasattr(objekt[0], '__call__'):
            raise TypeError(type_error_message)
        return lambda *params: objekt[0](*objekt[1:])

    class _By(object):
        def __init__(self, comparison, name=''):
            self.name = ('by ' + name).strip()
            self.comparison = comparison

matcher(Change)


# matchers for backwards compatibility
@matcher
def into():
    return be_into()


@matcher
def greater_than():
    return be_greater_than()


@matcher
def greater_than_or_equal_to():
    return be_greater_than_or_equal_to()


@matcher
def less_than():
    return be_less_than()


@matcher
def less_than_or_equal_to():
    return be_less_than_or_equal_to()


@matcher
def thrown_by():
    return be_thrown_by()


@matcher
def in_any_order():
    return include_in_any_order()


@matcher
def all_of():
    return include_all_of()


@matcher
def any_of():
    return include_any_of()


@matcher
def kind_of():
    return be_kind_of()


@matcher
def ended_with():
    return (lambda x, y: x.endswith(y), "%r is %sended with %r")


class Like(BeLike):
    name = 'like'

matcher(Like)


class IncludeDictElement(object):

    def __call__(self, *elements):
        self._expected_elements = elements
        return self

    def match(self, dictionary):
        self._ensure_it_is_really_a_dict(dictionary)
        self._actual_elements = self._get_element_values(dictionary)
        self._undesired_elements = []
        if self.run_with_negate:
            self._undesired_elements = [elem for elem in self._expected_elements if elem in self._actual_elements]
            return len(self._undesired_elements) != 0
        else:
            self._undesired_elements = [elem for elem in self._expected_elements if elem not in self._actual_elements]
            return len(self._undesired_elements) == 0

    def message_for_failed_should(self):
        return "expected target to include %s %s" % (
            self._pluralize_element(), self._humanize_undesired_elements())

    def message_for_failed_should_not(self):
        return "expected target to not include %s %s" % (
            self._pluralize_element(), self._humanize_undesired_elements())

    def _pluralize_element(self):
        return len(self._undesired_elements) > 1 and ('%ss' % self._element_name) or self._element_name

    def _humanize_undesired_elements(self):
        list_ = self._undesired_elements
        if len(list_) == 1:
            return repr(list_[0])
        list_ = [repr(x) for x in list_]
        last = list_.pop()
        list_[-1] = "%s and %s" % (list_[-1], last)
        return ', '.join(list_)

    def _ensure_it_is_really_a_dict(self, target):
        if not isinstance(target, dict):
            raise TypeError('target must be a dictionary')


class IncludeKeys(IncludeDictElement):

    name = 'include_keys'

    def __init__(self):
        self._element_name = 'key'
        self._get_element_values = lambda d: d.keys()


matcher(IncludeKeys)


class IncludeValues(IncludeDictElement):

    name = 'include_values'

    def __init__(self):
        self._element_name = 'value'
        self._get_element_values = lambda d: d.values()


matcher(IncludeValues)


class BeEmpty(object):

    name = 'be_empty'

    def __call__(self):
        return self

    def match(self, container):
        self._container = container
        return len(container) == 0

    def message_for_failed_should(self):
        return "expected %s to be empty" % repr(self._container)

    def message_for_failed_should_not(self):
        return "expected %s not to be empty" % repr(self._container)


matcher(BeEmpty)

class HaveSameAttributeValues(object):

    name = 'have_same_attribute_values_as'

    def __call__(self, other_object):
        self._other_object = other_object
        return self

    def match(self, actual_object):
        self._actual_object = actual_object
        found_different_attribute = False

        for key in self._other_object.__dict__.keys():
            got = self._actual_object.__dict__.get(key)
            expected =  self._other_object.__dict__.get(key)
            if got != expected:
                found_different_attribute = True
                break

        return found_different_attribute == False

    def message_for_failed_should(self):
        return "expected %r to have the same attribute values as %r" % (self._actual_object, self._other_object)

    def message_for_failed_should_not(self):
        return "expected %r to have not the same attribute values as %r" % (self._actual_object, self._other_object)

matcher(HaveSameAttributeValues)
