# Tests for IPN- and other receivers
import grok
import unittest
import megrok.paypal.tests
from zope.app.wsgi.testlayer import BrowserLayer
from zope.component import getMultiAdapter
from zope.interface.verify import verifyClass, verifyObject
from zope.publisher.browser import TestRequest
from zope.testbrowser.wsgi import Browser
from megrok.paypal.interfaces import (
    IPayPalIPNReceiver, IInstantPaymentNotification, )
from megrok.paypal.receiver import (
    PayPalIPNReceiver, InstantPaymentNotification, )
from megrok.paypal.testing import http_server


FunctionalLayer = BrowserLayer(megrok.paypal.tests, 'ftesting.zcml')


class TestPayPalIPNReceiver(unittest.TestCase):

    def test_iface(self):
        # the ipn receiver fullfills interface contracts
        receiver = PayPalIPNReceiver()
        verifyClass(IPayPalIPNReceiver, PayPalIPNReceiver)
        verifyObject(IPayPalIPNReceiver, receiver)

    def test_validate_no_notification_url(self):
        # we require a notification URL for validation requests
        receiver = PayPalIPNReceiver()
        receiver.validation_url = None
        assert receiver.validate('foo') is None
        receiver.validation_url = ''
        assert receiver.validate('bar') is None

    def test_validate_no_post_var_string(self):
        # if we got no post-var-string (or it is empty) we do not validate
        receiver = PayPalIPNReceiver()
        assert receiver.validate(None) is None
        assert receiver.validate('') is None

    def test_validate(self):
        # we can validate instant payment messages
        receiver = PayPalIPNReceiver()
        result = None
        with http_server(paypal_mode='valid') as server:
            receiver.validation_url = server.url
            result = receiver.validate('some-fake-data')
            sent_body = server.last_request_body
        assert result == "VERIFIED"
        assert sent_body == 'cmd=_notify-validate&some-fake-data'


class TestInstantPaymentNotfication(unittest.TestCase):

    def test_iface(self):
        # ensure we fullfill all interface contracts
        ipn = InstantPaymentNotification()
        verifyClass(IInstantPaymentNotification, InstantPaymentNotification)
        verifyObject(IInstantPaymentNotification, ipn)

    def test_constructor(self):
        # we can set data with the constructor.
        ipn = InstantPaymentNotification("some-data")
        assert ipn.data == "some-data"
        assert ipn.timestamp_received is not None


class SampleApp(grok.Context):
    # a sample context
    pass


class SampleAppView1(grok.View):
    # a view for a sample context
    grok.context(SampleApp)
    grok.name('foo')

    def render(self, *args, **kw):
        form_data = "VARS: %s" % sorted(self.request.form.items())
        return u"Hi from SampleAppView, %s" % form_data


class SampleAppView2(grok.View):
    # another view for sample context
    grok.context(SampleApp)
    grok.name('bar')

    def render(self):
        body_data = self.request.bodyStream.getCacheStream().read()
        content_type = self.request.headers.get("Content-Type")
        return u"INPUT: %s CONTENT-TYPE %s" % (body_data, content_type)


class ModifiedReceiver(PayPalIPNReceiver):
    # An IPN receiver that stores last sent notification string

    call_args = None

    def got_notification(self, post_var_string):
        self.call_args = post_var_string


class FakePayPal(grok.Model):
    # a fake paypal to send ipns to.

    # in `last_request` we store the last request received.
    last_request = None

    def __init__(self, mode='success'):
        # mode can be 'success',  'fail', or 'mirror'. 'mirror' means:
        # send back a body with received headers and body
        # data. 'success' and 'fail' should trigger to mimic positive
        # or negative validations.
        self.mode = mode


class FakePayPalView(grok.View):
    grok.name('index')
    grok.context(FakePayPal)

    def mirror(self):
        body_data = self.request.bodyStream.getCacheStream().read()
        content_type = self.request.headers.get("Content-Type")
        return 'BODY: %s\nCONTENT_TYPE: %s' % (body_data, content_type)

    def render(self):
        self.context.last_request = self.mirror()
        if self.context.mode == 'success':
            return 'VERIFIED'
        elif self.context.mode == 'mirror':
            return self.context.last_request
        return 'INVALID'


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
        assert browser.contents == 'Hi from SampleAppView, VARS: []'

    def test_post_data(self):
        # TEMPORARY test. Make sure we can post data.
        app = SampleApp()
        self.layer.getRootFolder()['app'] = app
        browser = Browser()
        browser.post("http://localhost/app/@@foo", "x=1&y=2")
        assert browser.contents == (
            "Hi from SampleAppView, VARS: [(u'x', u'1'), (u'y', u'2')]"
            )

    def test_can_access_post_data_line(self):
        # TEMPORARY test. We can access the body line with the post data.
        app = SampleApp()
        self.layer.getRootFolder()['app'] = app
        browser = Browser()
        browser.handleErrors = False
        browser.post("http://localhost/app/@@bar", "x=1&y=2")
        assert browser.contents == (
            "INPUT: x=1&y=2 "
            "CONTENT-TYPE application/x-www-form-urlencoded"
        )
        browser.post("http://localhost/app/@@bar", "y=1&x=2")
        assert browser.contents == (
            "INPUT: y=1&x=2 "
            "CONTENT-TYPE application/x-www-form-urlencoded"
        )

    def test_can_set_content_type(self):
        # TEMPORARY test. We can set the content type of a post request.
        app = SampleApp()
        self.layer.getRootFolder()['app'] = app
        browser = Browser()
        browser.handleErrors = False
        browser.post("http://localhost/app/@@bar", "x=1&y=2",
                     "application/x-javascript")
        assert browser.contents == (
            "INPUT: x=1&y=2 "
            "CONTENT-TYPE application/x-javascript"
            )

    def test_has_index_view(self):
        # we have an 'index' view for PayPalIPNReceivers
        receiver = PayPalIPNReceiver()
        request = TestRequest()
        view = getMultiAdapter((receiver, request), name='index')
        assert view is not None

    def test_index_returns_200_Ok(self):
        # if we deliver normal data we will get a 200 Ok.
        receiver = PayPalIPNReceiver()
        receiver.validation_url = ''
        self.layer.getRootFolder()['app'] = receiver
        browser = Browser()
        browser.open('http://localhost/app/@@index')
        assert browser.headers.get("status") == "200 Ok"

    def test_index_returns_empty_body(self):
        # if we deliver normal data we will return with an empty doc.
        receiver = PayPalIPNReceiver()
        receiver.validation_url = ''
        self.layer.getRootFolder()['app'] = receiver
        browser = Browser()
        browser.open('http://localhost/app/@@index')
        assert browser.contents == ''

    def test_index_calls_got_notification(self):
        # the index view informs the receiver.
        receiver = ModifiedReceiver()
        receiver.validation_url = ''
        self.layer.getRootFolder()['app'] = receiver
        browser = Browser()
        browser.post("http://localhost/app/@@index", "y=1&x=2")
        assert receiver.call_args == 'y=1&x=2'
        browser.post("http://localhost/app/@@index", "x=1&y=2")
        assert receiver.call_args == 'x=1&y=2'

    def test_index_is_default_view(self):
        # the index view is called by default.
        receiver = ModifiedReceiver()
        receiver.validation_url = ''
        self.layer.getRootFolder()['app'] = receiver
        browser = Browser()
        # we do not give a view name here.
        browser.post("http://localhost/app", "got_it=1")
        assert receiver.call_args == 'got_it=1'

    def test_validate_no_action_wo_validation_url(self):
        #  a receiver does not perform any action w/o a validation_url set.
        receiver = PayPalIPNReceiver()
        receiver.validation_url = ''
        assert receiver.validate('x=1') is None
        receiver.validation_url = None
        assert receiver.validate('x=1') is None

    def test_fake_paypal_success(self):
        # we can use FakePayPal for testing successful validations
        fake_paypal = FakePayPal(mode='success')
        root = self.layer.getRootFolder()
        root['fake_paypal'] = fake_paypal
        browser = Browser()
        browser.post('http://localhost/fake_paypal/@@index', 'x=2')
        assert browser.contents == 'VERIFIED'
        assert fake_paypal.last_request == (
            'BODY: x=2\n'
            'CONTENT_TYPE: application/x-www-form-urlencoded'
            )

    def test_fake_paypal_fail(self):
        # we can use FakePayPal for testing failed validations
        fake_paypal = FakePayPal(mode='fail')
        root = self.layer.getRootFolder()
        root['fake_paypal'] = fake_paypal
        browser = Browser()
        browser.post('http://localhost/fake_paypal/@@index', 'x=3')
        assert browser.contents == 'INVALID'
        assert fake_paypal.last_request == (
            'BODY: x=3\n'
            'CONTENT_TYPE: application/x-www-form-urlencoded'
            )

    def test_fake_paypal_mirror(self):
        # we can use FakePayPal for mirroring our posts
        fake_paypal = FakePayPal(mode='mirror')
        root = self.layer.getRootFolder()
        root['fake_paypal'] = fake_paypal
        browser = Browser()
        browser.post('http://localhost/fake_paypal/@@index', 'x=4')
        assert browser.contents == (
            'BODY: x=4\n'
            'CONTENT_TYPE: application/x-www-form-urlencoded'
            )
        assert fake_paypal.last_request == (
            'BODY: x=4\n'
            'CONTENT_TYPE: application/x-www-form-urlencoded'
            )
