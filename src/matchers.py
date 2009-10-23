from should_dsl import matcher
import re

@matcher
def equal_to():
    return (lambda x, y: x == y, '%s is %sequal to %s')

@matcher
def into():
    return (lambda item, container: item in container, '%s is %sinto %s')

@matcher
def greater_than():
    return (lambda x, y: x > y, '%s is %sgreater than %s')

@matcher
def greater_than_or_equal_to():
    return (lambda x, y: x >= y, '%s is %sgreater than or equal to %s')

@matcher
def less_than():
    return (lambda x, y: x < y, '%s is %sless than %s')

@matcher
def less_than_or_equal_to():
    return (lambda x, y: x <= y, '%s is %sless than or equal to %s')

@matcher
def thrown_by():
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
    return (check_exception, '%s is %sthrown by %s')

@matcher
def in_any_order():
    def contains_in_any_order(container, elements):
        for element in elements:
            if element not in container:
                return False
        return True
    return (contains_in_any_order, "%s does %shave in any order %s")

@matcher
def all_of():
    return (in_any_order()[0], "%s does %shave all of %s")

@matcher
def any_of():
    def have_any_of(container, elements):
        for element in elements:
            if element in container:
                return True
        return False
    return (have_any_of, "%s does %shave any of %s")

@matcher
def kind_of():
    return (lambda obj, kind: isinstance(obj, kind), "%s is %s a kind of %s")

@matcher
def ended_with():
    return (lambda x, y: x.endswith(y), "%s is %sended with %s")

@matcher
def like():
    return (lambda string, regex: re.match(regex, string) is not None, '"%s" is %slike "%s"')
