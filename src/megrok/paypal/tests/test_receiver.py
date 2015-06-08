# Tests for IPN- and other receivers
import unittest
import megrok.paypal.tests
from zope.app.wsgi.testlayer import BrowserLayer
from zope.interface.verify import verifyClass, verifyObject
from megrok.paypal.interfaces import IPayPalIPNReceiver
from megrok.paypal.receiver import PayPalIPNReceiver


FunctionalLayer = BrowserLayer(megrok.paypal.tests, 'ftesting.zcml')


class TestPayPalIPNReceiver(unittest.TestCase):

    def test_iface(self):
        # the ipn receiver fullfills interface contracts
        receiver = PayPalIPNReceiver()
        verifyClass(IPayPalIPNReceiver, PayPalIPNReceiver)
        verifyObject(IPayPalIPNReceiver, receiver)


class TestPayPalIPNReceiverFunctional(unittest.TestCase):

    layer = FunctionalLayer

    def test_get_rootfolder(self):
        # TEMPORARY test. Make sure we can get a root folder.
        assert self.layer.getRootFolder() is not None
