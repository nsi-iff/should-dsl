#!/usr/bin/env python
import doctest
import os
from tests import unittest_example

flags = doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS

if __name__ == '__main__':
    doctests_path = os.path.join(os.path.dirname(__file__), 'doctests')
    for doctest_file in os.listdir(doctests_path):
        if not doctest_file.endswith('.txt'):
            continue
        doctest.testfile(os.path.join(doctests_path, doctest_file),
                         optionflags=flags)

#    for module in [unittest_example,]:
#        doctest.testmod(module, optionflags=flags)

