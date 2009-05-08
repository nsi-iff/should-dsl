#coding: utf-8

class Should(object):
    
    def __init__(self, negate=False):
        self._negate = negate
        self._is_thrown_by = False
        self.should_functions_by_name = dict()
    
    def _evaluate(self, value):
        if self._negate:
            return not value
        return value
    
    def _negate_str(self):
        if not self._negate:
            return 'not '
        return ''
    
    def __rlshift__(self, lvalue):
        return self.__ror__(lvalue)
    
    def __ror__(self, lvalue):
        self._lvalue = lvalue
        if not self._has_rvalue:
            return self._check_assertion()
        return self
    
    def __rshift__(self, rvalue):
        return self.__or__(rvalue)
    
    def __or__(self, rvalue):
        self._rvalue = rvalue
        return self._check_assertion()
    
    @property
    def equal_to(self):
        self._func = lambda x, y: x == y
        self._error_message = lambda x, y: '%s is %sequal to %s' % (x, self._negate_str(), y)
        self._has_rvalue = True
        return self
    
    @property
    def true(self):
        self._func = lambda x: x is True
        self._error_message = lambda x: '%s is %sTrue' % (x, self._negate_str())
        self._has_rvalue = False
        return self
    
    @property
    def false(self):
        self._func = lambda x: x is False
        self._error_message = lambda x: '%s is %sFalse' % (x, self._negate_str())
        self._has_rvalue = False
        return self
    
    @property
    def none(self):
        self._func = lambda x: x == None
        self._error_message = lambda x: '%s is %sNone' % (x, self._negate_str())
        self._has_rvalue = False
        return self
    
    @property
    def into(self):
        self._func = lambda item, container: item in container
        self._error_message = lambda item, container: '%s is %sinto %s' % (item, self._negate_str(), container)
        self._has_rvalue = True
        return self 
    
    @property
    def have(self):
        self._func = lambda container, item: item in container
        self._error_message = lambda container, item: '%s does %shave %s' % (container, self._negate_str(), item)
        self._has_rvalue = True
        return self
    
    @property
    def greater_than(self):
        self._func = lambda x, y: x > y
        self._error_message = lambda x, y: '%s is %sgreater than %s' % (x, self._negate_str(), y)
        self._has_rvalue = True
        return self 
    
    @property
    def greater_than_or_equal_to(self):
        self._func = lambda x, y: x >= y
        self._error_message = lambda x, y: '%s is %sgreater than or equal to %s' % (x, self._negate_str(), y)
        self._has_rvalue = True
        return self
    
    @property
    def less_than(self):
        self._func = lambda x, y: x < y
        self._error_message = lambda x, y: '%s is %sless than %s' % (x, self._negate_str(), y)
        self._has_rvalue = True
        return self
    
    @property
    def less_than_or_equal_to(self):
        self._func = lambda x, y: x <= y
        self._error_message = lambda x, y: '%s is %sless than or equal to %s' % (x, self._negate_str(), y)
        self._has_rvalue = True
        return self
    
    @property
    def thrown_by(self):
        def check_exception(exception, callable, *args, **kw):
            try:
                callable(*args, **kw)
                return False
            except exception:
                return True
        self._func = check_exception
        self._error_message = lambda exception, callable: '%s is %sthrown by %s' % (exception, self._negate_str(), callable)
        self._has_rvalue = True
        self._is_thrown_by = True
        return self
    
    def _check_assertion(self):
        if self._has_rvalue:
            evaluation = None 
            if self._is_thrown_by and self._rvalue.__class__ in (tuple, list, dict) and len(self._rvalue) > 1:
                evaluation = self._evaluate(self._func(self._lvalue, self._rvalue[0], *self._rvalue[1:]))
            else:
                evaluation = self._evaluate(self._func(self._lvalue, self._rvalue)) 
            if not evaluation:
                raise ShouldNotSatisfied, self._error_message(self._lvalue, self._rvalue)
            else:
                return True
        else:
            if not self._evaluate(self._func(self._lvalue)):
                raise ShouldNotSatisfied, self._error_message(self._lvalue)
            else:
                return True
            
    def add_should(self, function):
        '''Adds a new should case.
        The function must return a tuple (or any other __getitem__ compatible object)
        containing three elements:
        [0] = a function taking one or two parameters, that will do the desired comparison
        [1] = the error message. this message must contain three %s placeholders. By example,
        "%s is %snicer than %s" can result in "Python is nicer than Ruby" or 
        "Python is not nicer than Ruby" depending whether <<should_be.function_name>> or
        <<should_not_be.function_name>> be applied.
        [2] True if there is a rvalue, otherwise False
        '''
        self.should_functions_by_name[function.__name__] = function

    def __getattr__(self, method_info):
        def method_missing(*args):
            try:
                function = self.should_functions_by_name[str(method_info)]
                result = function()
                self._func = result[0]
                error_message = result[1]
                self._has_rvalue = result[2]
                if self._has_rvalue:
                    self._error_message = lambda x, y: error_message % (x, self._negate_str(), y)
                else:
                    self._error_message = lambda x: error_message % (x, self._negate_str()) 
                return self
            except KeyError:
                raise AttributeError, "'%s' object has no attribute '%s'" % (self.__class__, str(method_info))
        return method_missing()

            
class ShouldNotSatisfied(Exception):
    pass

should_be = Should(negate=False)
should_not_be = Should(negate=True)
should_have = Should(negate=False).have
should_not_have = Should(negate=True).have

def should_case(method):
    should_be.add_should(method)
    should_not_be.add_should(method)
    return method   