Should DSL: Improved readability for should-style assertions
============================================================

The goal of *Should DSL* is to write should assertions in Python as clear and readable as possible.

It would be good to be as close as:

::

    SOME_VALUE should be equal to ANOTHER VALUE
    or
    SOME_EXCEPTION should be thrown by SOME_CALLABLE
    or
    SOME_VALUE should not be into SOME_CONTAINER


For using this DSL, you need to import all the module's namespace, as:

::

    from should_dsl import *


For example:

::


    1  |should_be.equal_to| 1     # will be true
    'should' |should_have| 'oul'  # will also be true	
    3 |should_be.into| (0, 1, 2)  # will be false


A nice example of exceptions would be:

::

    def raise_zerodivisionerror():
        return 1/0
    ZeroDivisionError |should_be.thrown_by| raise_zerodivisionerror


Extending the DSL with custom matchers is easy:

::

    @matcher
    def the_square_root_of():
        import math
        return (lambda x, y: x == math.sqrt(y), "%s is %sthe square root of %s")
        
    3 |should_be.the_square_root_of| 9    # will be true
    4 |should_be.the_square_root_of| 9    # will be false

 