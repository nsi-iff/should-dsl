import doctest
import unittest
import os

flags = doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS

if __name__ == '__main__':
    doctests_path = os.path.join(os.path.dirname(__file__),  'src', 'doctests')
    suite = unittest.TestSuite()
    runner = unittest.TextTestRunner()

    suite.addTest(doctest.DocFileSuite('README.rst'))
    for doctest_file in os.listdir(doctests_path):
        if doctest_file.endswith('.txt'):
            suite.addTest(doctest.DocFileSuite(os.path.join(doctests_path,
                                                            doctest_file),
                                               optionflags=flags))
    runner.run(suite)
