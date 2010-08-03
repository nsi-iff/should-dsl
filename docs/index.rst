Basic Usage
===========

.. toctree::
    :maxdepth: 2
    :hidden:

    available_matchers
    predicate_matchers
    custom_matchers
    unittest
    contributing
    license


The goal of *Should-DSL* is to write should expectations in Python as clear and readable as possible, using **"almost"** natural language (limited - sometimes - by the Python language constraints).

In order to use this DSL, you need to import ``should`` and ``should_not`` objects from ``should_dsl`` module.

For example::

    >>> from should_dsl import should

    >>> 1 |should| equal_to(1)

    >>> 'should' |should| include('oul')

    >>> 3 |should| be_into([0, 1, 2])
    Traceback (most recent call last):
    ...
    ShouldNotSatisfied: 3 is not into [0, 1, 2]

Should-DSL with unittest
-------------------------

*should-dsl* is unittest-compatible, so, in any unittest test case, failures on should expectations will result on unittest failures, not errors::

    >>> from should_dsl import *
    >>> import os
    >>> import unittest

    >>> class UsingShouldExample(unittest.TestCase):
    ...     def test_showing_should_not_be_works(self):
    ...         'hello world!' |should_not| be('Hello World!')
    ...
    ...     def test_showing_should_include_fails(self):
    ...         [1, 2, 3] |should| include(5)
    ...
    ...     def test_showing_should_include_works(self):
    ...         'hello world!' |should| include('world')
    ...
    ...     def test_showing_should_not_include_fails(self):
    ...         {'one': 1, 'two': 2} |should_not| include('two')
    ...
    ...     def test_showing_should_not_include_works(self):
    ...         ["that's", 'all', 'folks'] |should_not| include('that')

    >>> devnull = open(os.devnull, 'w')
    >>> runner = unittest.TextTestRunner(stream=devnull)
    >>> suite = unittest.TestLoader().loadTestsFromTestCase(UsingShouldExample)
    >>> runner.run(suite)
    <unittest...TextTestResult run=5 errors=0 failures=2>
    >>> devnull.close()


Should-DSL
==========

Documentation
-------------

`Should-DSL Matchers <available_matchers.html>`_: all available matchers

`Predicate Matchers <predicate_matchers.html>`_: predicate matchers are the matchers work with boolean methods and attributes, to give users more freedom to write more readable specifications.

`Custom Matchers <custom_matchers.html>`_: extending Should-DSL with custom matchers is very easy. It is possible to add matchers through functions and classes, for simple and complex behaviors.

`Contributing <contributing.html>`_: see how you can contribute to Should-DSL development

`License <license.html>`_: MIT license


Installation
------------


Should-DSL can be installed through PyPI, using :command:`pip` or :command:`easy_install`.

.. code-block:: bash

    $ [sudo] pip install should-dsl


Or you can install the last development version from `github repository <http://github.com/hugobr/should-dsl>`_, using :command:`pip`:

.. code-block:: bash

    $ [sudo] pip install -e http://github.com/hugobr/should-dsl.git#egg=should-dsl


If you want to have a clone of Should-DSL's repository and then install Should-DSL:

.. code-block:: bash

    $ git clone http://github.com/hugobr/should-dsl.git
    $ cd should-dsl
    $ [sudo] python setup.py install
    


