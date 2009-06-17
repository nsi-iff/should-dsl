class Should(object):
    
    def __init__(self, negate=False):
        self._negate = negate
        self._is_thrown_by = False
        self._matchers_by_name = dict()
        self.__set_default_matcher()
    
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
        return self

    def __or__(self, rvalue):
        self._rvalue = rvalue
        return self._check_expectation()
    
    __rshift__ = __ror__
    __rlshift__ = __or__ 
    
    def __set_default_matcher(self):
        '''The default behavior for a should object, called on constructor'''
        self._func = lambda x, y: x is y
        self._error_message = '%s is %s%s'
    
    def _make_a_copy(self, func, error_message):
        clone = Should(self._negate)
        clone._is_thrown_by = self._is_thrown_by
        clone._matchers_by_name = self._matchers_by_name
        clone._func = func
        clone._error_message = error_message
        return clone
    
    @property
    def equal_to(self):
        return self._make_a_copy(func=lambda x, y: x == y, 
                                error_message='%s is %sequal to %s')
        
    @property
    def into(self):
        return self._make_a_copy(func=lambda item, container: item in container, 
                                error_message='%s is %sinto %s')
    
    @property
    def have(self): 
        return self._make_a_copy(func=lambda container, item: item in container, 
                                error_message='%s does %shave %s')
    
    @property
    def greater_than(self):
        return self._make_a_copy(func=lambda x, y: x > y, 
                                error_message='%s is %sgreater than %s') 
    
    @property
    def greater_than_or_equal_to(self):
        return self._make_a_copy(func=lambda x, y: x >= y, 
                                error_message='%s is %sgreater than or equal to %s')
    
    @property
    def less_than(self):
        return self._make_a_copy(func=lambda x, y: x < y, 
                                error_message='%s is %sless than %s')
    
    @property
    def less_than_or_equal_to(self):
        return self._make_a_copy(func=lambda x, y: x <= y, 
                                error_message='%s is %sless than or equal to %s')
    
    @property
    def thrown_by(self):
        def check_exception(exception, callable, *args, **kw):
            try:
                callable(*args, **kw)
                return False
            except exception:
                return True
            except Exception:
                return False
        clone = self._make_a_copy(func=check_exception, 
                                 error_message='%s is %sthrown by %s')
        clone._is_thrown_by = True
        return clone

    def _rvalue_is_container(self):
        return getattr(self._rvalue, '__getitem__', False)

    def _thrown_by_was_called_with_parameters(self):
       return self._is_thrown_by and\
              self._rvalue_is_container() and\
              len(self._rvalue) > 1
    
    def _check_expectation(self):
        rvalue = self._rvalue
        params = []
        if self._thrown_by_was_called_with_parameters():
            rvalue = self._rvalue[0]
            params = self._rvalue[1:]
        evaluation = self._evaluate(self._func(self._lvalue, rvalue, *params)) 
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

    def __getattr__(self, method_name):
        '''if it can't find method_name in the instance
           it will look in _matchers_by_name'''
        if str(method_name) not in self._matchers_by_name:
            raise AttributeError("%s object has no matcher '%s'" % (
                self.__class__.__name__, str(method_name)))
        function = self._matchers_by_name[str(method_name)]
        result = function()
        clone = self._make_a_copy(func=result[0], error_message=result[1])
        return clone
    
            
class ShouldNotSatisfied(AssertionError):
    '''Extends AssertionError for unittest compatibility'''

should_be = Should(negate=False)
should_not_be = Should(negate=True)
should_have = Should(negate=False).have
should_not_have = Should(negate=True).have

def matcher(matcher_function):
    '''Create customer should_be matchers. We recommend you use it as a decorator'''
    should_be.add_matcher(matcher_function)
    should_not_be.add_matcher(matcher_function)
    return matcher_function
