Basic Usage
===========

.. toctree::
    :maxdepth: 2
    :hidden:

    available_matchers
    predicate_matchers
    custom_matchers
    contributing
    license


The goal of *Should-DSL* is to write should expectations in Python as clear and readable as possible, using **"almost"** natural language (limited - sometimes - by the Python language constraints).

In order to use this DSL, you need to import ``should`` and ``should_not`` objects from ``should_dsl`` module.

example.py::

    import unittest
    from should_dsl import should, should_not

    class UsingShouldExample(unittest.TestCase):

      def test_hello_world(self):
          'hello world!' |should_not| equal_to('Hello World!')

      def test_include(self):
          [1, 2, 3] |should| include(5)


    if __name__ == '__main__':
      unittest.main()

.. code-block:: bash

    $ python example.py -vvv
    test_hello_world (__main__.UsingShouldExample) ... ok
    test_include (__main__.UsingShouldExample) ... FAIL

    ======================================================================
    FAIL: test_include (__main__.UsingShouldExample)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "example.py", line 10, in test_include
        [1, 2, 3] |should| include(5)
      File "build/bdist.macosx-10.6-universal/egg/should_dsl/dsl.py", line 38, in __or__
        return self._check_expectation()
      File "build/bdist.macosx-10.6-universal/egg/should_dsl/dsl.py", line 42, in _check_expectation
        raise ShouldNotSatisfied(self._negate and self._rvalue.message_for_failed_should_not() or self._rvalue.message_for_failed_should())
    ShouldNotSatisfied: [1, 2, 3] does not include 5

    ----------------------------------------------------------------------
    Ran 2 tests in 0.002s

    FAILED (failures=1)


Documentation
=============

`Should-DSL Matchers <available_matchers.html>`_: check all available matchers

`Predicate Matchers <predicate_matchers.html>`_: predicate matchers are the matchers work with boolean methods and attributes and thetgive users more freedom to write more readable specifications.

`Custom Matchers <custom_matchers.html>`_: extending Should-DSL with custom matchers is very easy. It is possible to add matchers through functions and classes, for simple and complex behaviors.

`Contributing <contributing.html>`_: see how you can contribute to Should-DSL development

`License <license.html>`_: MIT License


Installation
------------

Should-DSL can be installed through PyPI, using :command:`pip` or :command:`easy_install`.

.. code-block:: bash

    $ pip install should-dsl
    # maybe you need to run it as sudo
