import sys

if sys.version_info >= (3,):
    string_types = (str,)
else:
    string_types = (basestring,)
