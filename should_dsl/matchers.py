import re
import sys
from decimal import Decimal
from should_dsl import matcher


@matcher
def be():
    return (lambda x, y: x is y, "%r is %s%r")


@matcher
def include():
    return (lambda container, item: item in container, "%r does %sinclude %r")


@matcher
def contain():
    return (lambda container, item: item in container, "%r does %scontain %r")


@matcher
def equal_to():
    return (lambda x, y: x == y, '%r is %sequal to %r')


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
        callable = callable_and_possible_params[0]
        params = callable_and_possible_params[1:]
    else:
        callable = callable_and_possible_params
        params = []

    try:
        callable(*params)
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

    def __call__(self, exception, message=None):
        if message is None and isinstance(exception, Exception):
            self._expected_message = str(exception)
            self._expected_exception = exception.__class__
        else:
            self._expected_exception = exception
            self._expected_message = message
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
            if self._expected_message is None:
                return True
            self._actual_message = str(e)
            return self._actual_message == self._expected_message
        except Exception:
            e = sys.exc_info()[1]
            self._actual_exception = e.__class__
            return False

    def message_for_failed_should(self):
        message = "expected to throw %r" % self._expected_exception.__name__
        if self._expected_message is not None:
            message += " with the message %r" % self._expected_message
        if self._actual_exception is None:
            message += ', got no exception'
        else:
            message += ', got %r' % self._actual_exception.__name__
        if hasattr(self, '_actual_message'):
            message += ' with %r' % self._actual_message
        return message

    def message_for_failed_should_not(self):
        message = "expected not to throw %r" % self._expected_exception.__name__
        if self._expected_message is not None:
            message += " with the message %r" % self._expected_message
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
                if self._is_function(self._collection):
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
                if self._is_function(getattr(owned_object, owned_by_owned)):
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
        if self._is_function(owned_object):
            owned_object = owned_object()
        return owned_object

    def _is_function(self, object_):
        return (hasattr(object_, 'im_func') or hasattr(object_, '__func__'))

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

