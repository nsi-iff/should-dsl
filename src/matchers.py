from should_dsl import matcher
import re
from decimal import Decimal

@matcher
def be():
    return (lambda x, y: x is y, "%s is %s%s")

@matcher
def include():
    return (lambda container, item: item in container, "%s does %sinclude %s")

@matcher
def contain():
    return (lambda container, item: item in container, "%s does %scontain %s")

@matcher
def equal_to():
    return (lambda x, y: x == y, '%s is %sequal to %s')

@matcher
def be_into():
    return (lambda item, container: item in container, '%s is %sinto %s')

@matcher
def be_greater_than():
    return (lambda x, y: x > y, '%s is %sgreater than %s')

@matcher
def be_greater_than_or_equal_to():
    return (lambda x, y: x >= y, '%s is %sgreater than or equal to %s')

@matcher
def be_less_than():
    return (lambda x, y: x < y, '%s is %sless than %s')

@matcher
def be_less_than_or_equal_to():
    return (lambda x, y: x <= y, '%s is %sless than or equal to %s')

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
    return (check_exception, '%s is %sthrown by %s')

@matcher
class Throw:

    name = 'throw'

    def __call__(self, exception, message=None):
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
        except self._expected_exception, e:
            self._actual_exception = self._expected_exception
            if self._expected_message is None:
                return True
            self._actual_message = str(e)
            return self._actual_message == self._expected_message
        except Exception, e:
            self._actual_exception = e.__class__
            return False

    def message_for_failed_should(self):
        message = "expected to throw %s" % self._expected_exception.__name__
        if self._expected_message is not None:
            message += " with the message %r" % self._expected_message
        if self._actual_exception is None:
            message += ', got no exception'
        else:
            message += ', got %s' % self._actual_exception.__name__
        if hasattr(self, '_actual_message'):
            message += ' with %r' % self._actual_message
        return message

    def message_for_failed_should_not(self):
        message = "expected not to throw %s" % self._expected_exception.__name__
        if self._expected_message is not None:
            message += " with the message %r" % self._expected_message
        return "%s, but got it" % message


@matcher
def include_in_any_order():
    def contains_in_any_order(container, elements):
        for element in elements:
            if element not in container:
                return False
        return True
    return (contains_in_any_order, "%s does %sinclude in any order %s")

@matcher
def include_all_of():
    return (include_in_any_order()[0], "%s does %sinclude all of %s")

@matcher
def include_any_of():
    def include_any_of_func(container, elements):
        for element in elements:
            if element in container:
                return True
        return False
    return (include_any_of_func, "%s does %sinclude any of %s")

@matcher
def be_kind_of():
    return (lambda obj, kind: isinstance(obj, kind), "%s is %s a kind of %s")

@matcher
def end_with():
    return (lambda x, y: x.endswith(y), "%s do %send with %s")

@matcher
def be_like():
    return (lambda string, regex: re.match(regex, string) is not None, '"%s" is %slike "%s"')

@matcher
def equal_to_ignoring_case():
    return (lambda x, y: unicode(x, 'utf-8').lower() == unicode(y, 'utf-8').lower(), '"%s" is %sequal to "%s" ignoring case')


@matcher
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
                if hasattr(self._collection, 'im_func'):
                    self._collection = self._collection()
                    if not self._is_iterable(self._collection):
                        raise TypeError("target's %s() does not return an iterable" % self._collection_name)
                else:
                    raise TypeError("target's %s is not an iterable" % self._collection_name)
        elif self._is_iterable(self._lvalue):
            self._collection = self._lvalue
        else:
            raise TypeError("target does not have a %s collection, nor it is an iterable" % (
                self._collection_name))
        return self._compare()

    def _compare(self):
        return self._count == len(self._collection)

    def message_for_failed_should(self):
        if self.name == 'have':
            description = ''
        else:
            description = "%s " % self.name[5:].replace('_', ' ')
        return "expected %s%s %s, got %s" % (description, self._count,
            self._humanized_collection_name, len(self._collection))

    def message_for_failed_should_not(self):
        return "expected target not to %s %d %s, got %d" % (
            self.name.replace('_', ' '), self._count,
            self._humanized_collection_name, len(self._collection))

    def _is_iterable(self, objekt):
        return hasattr(objekt, '__len__')


@matcher
class HaveAtLeast(Have):

    name = 'have_at_least'

    def _compare(self):
        return len(self._collection) >= self._count


@matcher
class HaveAtMost(Have):

    name = 'have_at_most'

    def _compare(self):
        return len(self._collection) <= self._count


@matcher
class RespondTo(object):

    name = 'respond_to'

    def __call__(self, method_name):
        self._method_name = method_name
        return self

    def match(self, lvalue):
        self._lvalue = lvalue
        return hasattr(self._lvalue, self._method_name)

    def message_for_failed_should(self):
        return "expected %s to respond to %s" % (self._lvalue,
            self._method_name)

    def message_for_failed_should_not(self):
        return "expected %s not to respond to %s" % (self._lvalue,
            self._method_name)


@matcher
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


@matcher
class Change(object):

    name = 'change'

    def __init__(self):
        self._by = None
        self._using_from_to = False

    def __call__(self, verifier):
        self._verifier = self._to_callable(verifier)
        return self

    def match(self, action):
        self._action = self._to_callable(action)
        self._before_result = self._verifier()
        self._action()
        self._after_result = self._verifier()
        if self._by is not None:
            self._actual_difference = abs(self._before_result - self._after_result)
            return self._by[1](self._expected_difference, self._actual_difference)
        elif self._using_from_to:
            return self._before_result == self._from_value and self._after_result == self._to_value
        else:
            return self._after_result != self._before_result


    def message_for_failed_should(self):
        if self._by is not None:
            return 'result should have changed %s %s, but was changed by %s' %(
                self._by[0], self._expected_difference, self._actual_difference)
        elif self._using_from_to:
            return 'result should have changed from %s to %s, but was changed from %s to %s' % (
                self._from_value, self._to_value, self._before_result, self._after_result)
        else:
            return 'result should have changed, but is still %s' % (
                self._before_result)

    def message_for_failed_should_not(self):
        if self._using_from_to:
            return 'result should not have changed from %s to %s' % (
                self._from_value, self._to_value)
        else:
            return 'should not have changed, but did change from %s to %s' % (
                self._before_result, self._after_result)

    def by(self, difference):
        self._handle_by(difference, 'by', lambda exp_dif, act_dif: act_dif == exp_dif)
        return self

    def  by_at_least(self, difference):
        self._handle_by(difference, 'by at least', lambda exp_dif, act_dif: act_dif >= exp_dif)
        return self

    def by_at_most(self, difference):
        self._handle_by(difference, 'by at most', lambda exp_dif, act_dif: act_dif <= exp_dif)
        return self

    def _handle_by(self, difference, method, comparison):
        self._expected_difference = difference
        self._by = (method, comparison)

    def _from(self, from_value):
        self._from_value = from_value
        self._using_from_to = True
        return self

    def to(self, to_value):
        self._to_value = to_value
        return self

    def _to_callable(self, objekt):
        if callable(objekt):
            return objekt
        type_error_message = 'parameter passed to change must be a callable or a iterable having a callable as its first element'
        if not getattr(objekt, '__getitem__', False) or not callable(objekt[0]):
            raise TypeError(type_error_message)
        return lambda *params: objekt[0](*objekt[1:])


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
    return (lambda x, y: x.endswith(y), "%s is %sended with %s")

@matcher
def like():
    return be_like()

