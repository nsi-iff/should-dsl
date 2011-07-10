class Mock(object):

    called = False
    args = ()
    kw = {}
    return_value = None

    def __init__(self, return_value=None):
        self.return_value = return_value

    def __call__(self, *args, **kw):
        self._args = args
        self._kw = kw
        self.called = True
        return self.return_value

    def called_with(self, args, kw):
        return self._args == args and self._kw == kw


