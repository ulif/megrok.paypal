import unittest


class TestPackage(unittest.TestCase):

    def test_foo(self):
        assert 1 == 1


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(TestPackage))
    return suite
