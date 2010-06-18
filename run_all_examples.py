import doctest
import unittest
import os
import sys

flags = doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS|doctest.IGNORE_EXCEPTION_DETAIL

if __name__ == '__main__':
    doctests_path = os.path.join(os.path.dirname(__file__),  'src', 'doctests')
    suite = unittest.TestSuite()
    runner = unittest.TextTestRunner()

    suite.addTest(doctest.DocFileSuite('README.rst', optionflags=flags))
    for doctest_file in os.listdir(doctests_path):
        if doctest_file.endswith('.txt'):
            suite.addTest(doctest.DocFileSuite(os.path.join(doctests_path,
                                                            doctest_file),
                                               optionflags=flags))
    result = runner.run(suite)
    sys.exit(int(bool(result.failures or result.errors)))

