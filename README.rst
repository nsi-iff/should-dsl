Should DSL: Improved readability for should-style expectations
==============================================================

The goal of *Should DSL* is to write should expectations in Python as clear and readable as possible.

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
    3 |should_be.into| (0, 1, 2)  # will raise a ShouldNotSatisfied exception


The *equal_to* matcher verifies object equality. If you want to ensure identity, you must use *should_be* with no matcher:

::


    2 |should_be| 2


A nice example of exceptions would be:

::

    def raise_zerodivisionerror():
        return 1/0
    ZeroDivisionError |should_be.thrown_by| raise_zerodivisionerror


Both *should_have* and *should_be* have versions for negation:

::

    2 |should_not_be.into| [1, 3, 5]    # will be true
    'should' |should_not_have| 'oul'    # will raise a ShouldNotSatisfied exception


Extending the DSL with custom matchers is easy:

::

    @matcher
    def the_square_root_of():
        import math
        return (lambda x, y: x == math.sqrt(y), "%s is %sthe square root of %s")

    3 |should_be.the_square_root_of| 9    # will be true
    4 |should_be.the_square_root_of| 9    # will raise a ShouldNotSatisfiedException


*should-dsl* is unittest-compatible, so, on a unittest test case, failures on should expectations will result on unittest failures, not errors.

