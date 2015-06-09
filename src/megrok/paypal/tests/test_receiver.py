# Tests for IPN- and other receivers
import grok
import unittest
import megrok.paypal.tests
from zope.app.wsgi.testlayer import BrowserLayer, Browser
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


class SampleApp(grok.Context):
    # a sample context
    pass


class SampleAppView(grok.View):
    # a view for a sample context
    grok.context(SampleApp)
    grok.name('foo')

    def render(self, *args, **kw):
        return u"Hi from SampleAppView"


class TestPayPalIPNReceiverFunctional(unittest.TestCase):

    layer = FunctionalLayer

    def setUp(self):
        # grok ourselves to get views etc, registered
        grok.testing.grok('megrok.paypal.tests.test_receiver')

    def test_get_rootfolder(self):
        # TEMPORARY test. Make sure we can get a root folder.
        assert self.layer.getRootFolder() is not None

    def test_use_test_browser(self):
        # TEMPORARY test. Make sure we can use a virtual browser.
        app = SampleApp()
        self.layer.getRootFolder()['app'] = app
        browser = Browser()
        browser.open("http://localhost/app/@@foo")
        assert browser.contents == 'Hi from SampleAppView'
