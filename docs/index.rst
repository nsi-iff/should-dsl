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

::

    >>> from should_dsl import should, should_not
    >>> import os
    >>> import unittest

    >>> class UsingShouldExample(unittest.TestCase):
    ...     def test_showing_should_not_be_works(self):
    ...         'hello world!' |should_not| equal_to('Hello World!')
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


Documentation
=============

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


