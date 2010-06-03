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
def have_in_any_order():
    def contains_in_any_order(container, elements):
        for element in elements:
            if element not in container:
                return False
        return True
    return (contains_in_any_order, "%s does %shave in any order %s")

@matcher
def have_all_of():
    return (have_in_any_order()[0], "%s does %shave all of %s")

@matcher
def have_any_of():
    def have_any_of_func(container, elements):
        for element in elements:
            if element in container:
                return True
        return False
    return (have_any_of_func, "%s does %shave any of %s")

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
    return have_in_any_order()

@matcher
def all_of():
    return have_all_of()

@matcher
def any_of():
    return have_any_of()

@matcher
def kind_of():
    return be_kind_of()

@matcher
def ended_with():
    return (lambda x, y: x.endswith(y), "%s is %sended with %s")

@matcher
def like():
    return be_like()

