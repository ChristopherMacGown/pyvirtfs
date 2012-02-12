import os

try:
    import unittest2 as unittest
except ImportError:
    import unittest

def testdata(filename):
    return os.path.join(os.path.dirname(__file__), "data", filename)

class TestHelper(unittest.TestCase):
    def assertNothingRaised(self, caller, *args, **kwargs):
        raised=None
        try:
            caller(*args, **kwargs)
        except Exception:
            raised=True

        self.assertFalse(raised)
