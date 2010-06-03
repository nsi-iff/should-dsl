from should_dsl import matcher
import re

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
def throw():
    def local_check_exception(callable_and_possible_params, expected_exception):
        return check_exception(expected_exception=expected_exception,
                               callable_and_possible_params=callable_and_possible_params)
    return (local_check_exception, "%s %sthrows %s")

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

    def __init__(self, lvalue):
        self._lvalue = lvalue

    def __call__(self, count):
        self._count = count
        return self

    def __getattr__(self, collection_name):
        self._collection_name = collection_name
        self._humanized_collection_name = collection_name.replace('_', ' ')
        return self

    def match(self):
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

    def __init__(self, lvalue):
        self._lvalue = lvalue

    def __call__(self, method_name):
        self._method_name = method_name
        return self

    def match(self):
        return hasattr(self._lvalue, self._method_name)

    def message_for_failed_should(self):
        return "expected %s to respond to %s" % (self._lvalue,
            self._method_name)

    def message_for_failed_should_not(self):
        return "expected %s not to respond to %s" % (self._lvalue,
            self._method_name)


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

