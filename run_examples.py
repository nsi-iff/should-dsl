#!/usr/bin/env python
import doctest
import unittest
import sys

def test_suite(docs):
    suite = unittest.TestSuite()
    for doc in docs:
        suite.addTest(doctest.DocFileSuite(doc, optionflags=flags()))
    return suite

def flags():
    flags = doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS
    if sys.version_info >= (3,):
        flags |= doctest.IGNORE_EXCEPTION_DETAIL
    return flags

def run(docs):
    suite = test_suite(docs)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    sys.exit(int(bool(result.failures or result.errors)))

if __name__ == '__main__':
    run(sys.argv)

