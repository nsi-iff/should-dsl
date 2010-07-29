#!/usr/bin/env python
import doctest
import unittest
import os
import sys
import glob


def test_suite():
    flags = doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS
    if sys.version_info >= (3,):
        flags |= doctest.IGNORE_EXCEPTION_DETAIL
    doctests_path = os.path.join('should_dsl', 'doctests')
    suite = unittest.TestSuite()
    for doc in glob.glob('docs/*.rst') + ['README.rst']:
        suite.addTest(doctest.DocFileSuite(doc, optionflags=flags))
    suite.addTest(doctest.DocFileSuite('README.rst', optionflags=flags))
    for doctest_file in os.listdir(doctests_path):
        if doctest_file.endswith('.txt'):
            suite.addTest(doctest.DocFileSuite(os.path.join(doctests_path,
                                                            doctest_file),
                                               optionflags=flags))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite())
    sys.exit(int(bool(result.failures or result.errors)))
