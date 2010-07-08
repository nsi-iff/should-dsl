.. ..include:: ../README.rst

=============================================================
Should-DSL: Improve readability for should-style expectations
=============================================================

Contents:

.. toctree::
    :maxdepth: 1

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
    True
    >>> 'should' |should| include('oul')
    True
    >>> 3 |should| be_into([0, 1, 2])
    Traceback (most recent call last):
    ...
    ShouldNotSatisfied: 3 is not into [0, 1, 2]

Installing Should-DSL
=====================


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
