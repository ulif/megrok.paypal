# Tests for IPN- and other receivers
import datetime
import grok
import unittest
import megrok.paypal.tests
from zope.component import getMultiAdapter
from zope.interface.verify import verifyClass, verifyObject
from zope.publisher.browser import TestRequest
from zope.testbrowser.wsgi import Browser
from megrok.paypal.interfaces import (
    IPayPalIPNReceiver, IInstantPaymentNotification, )
from megrok.paypal.receiver import (
    PayPalIPNReceiver, InstantPaymentNotification, get_uuid)
from megrok.paypal.testing import http_server
from megrok.paypal.testlayer import browser_http_layer


class TestHelpers(unittest.TestCase):

    def test_get_uuid(self):
        # we can get uuids
        assert get_uuid() is not None

    def test_get_uuid_creates_unique_ids(self):
        # generated ids are different
        assert get_uuid() != get_uuid()

    def test_get_uuid_creates_strings(self):
        # we want regular strings
        assert isinstance(get_uuid(), str)


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

    def test_validate_invlid(self):
        # we get it if a payment notification is invalid
        receiver = PayPalIPNReceiver()
        result = None
        with http_server(paypal_mode='invalid') as server:
            receiver.validation_url = server.url
            result = receiver.validate('some-fake-data')
            sent_body = server.last_request_body
        assert result == "INVALID"
        assert sent_body == 'cmd=_notify-validate&some-fake-data'

    def test_store_notification_returns_uuid(self):
        # `store_notification` returns a UUID
        receiver = PayPalIPNReceiver()
        uuid = receiver.store_notification("sample-string")
        assert uuid is not None

    def test_store_notification_returns_passed_in_uuid(self):
        # we get back our own UUID if we pass one in
        receiver = PayPalIPNReceiver()
        uuid = receiver.store_notification("sample-string", uuid="blah")
        assert uuid == u"blah"

    def test_store_notification_stores_notification(self):
        # notifications are really stored
        receiver = PayPalIPNReceiver()
        receiver.store_notification("sample-string", uuid="my-uuid")
        assert "my-uuid" in receiver
        stored = receiver["my-uuid"]
        assert IInstantPaymentNotification.providedBy(stored)


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
        assert ipn.timestamp_validation_requested is None
        assert ipn.timestamp_validation_received is None
        assert ipn.final_verdict is None

    def test_constructor_timestamp_received(self):
        # we can set the `timestamp_received` initially.
        a_timestamp = datetime.datetime(2012, 12, 1, 10, 11, 12)
        ipn = InstantPaymentNotification(
            "some-data", timestamp_received=a_timestamp)
        assert ipn.data == "some-data"
        assert ipn.timestamp_received == a_timestamp

    def test_constructor_other_timestamps(self):
        # also the other timestamps can be set initially
        ts1 = datetime.datetime(2012, 1, 2, 3, 4, 5)
        ts2 = datetime.datetime(2013, 2, 3, 4, 5, 6)
        ipn = InstantPaymentNotification(
            "some-data",
            timestamp_validation_requested=ts1,
            timestamp_validation_received=ts2)
        assert ipn.timestamp_validation_requested == ts1
        assert ipn.timestamp_validation_received == ts2

    def test_constructor_final_verdict(self):
        # we can pass in a verdict in constructor
        ipn = InstantPaymentNotification(
            "some-data", final_verdict="youre lost")
        assert ipn.final_verdict == "youre lost"

    def test_constructor_auto_timestamp_only_with_data(self):
        # we set the timestamp_received only iff there is data and
        # no other timestamp_received passed in
        ipn = InstantPaymentNotification(None)
        assert ipn.timestamp_received is None


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

    def store_notification(self, post_var_string):
        self.call_args = post_var_string


class TestPayPalIPNReceiverFunctional(unittest.TestCase):

    layer = browser_http_layer

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

    def test_index_calls_store_notification(self):
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

    def test_notify_view_validation_valid(self):
        # we can get successful validations with notify
        receiver = PayPalIPNReceiver()
        receiver.validation_url = self.layer.server.url
        root = self.layer.getRootFolder()
        root['app'] = receiver
        browser = Browser()
        browser.post('http://localhost/app/@@index', 'x=2')
        sent_body = self.layer.server.last_request_body
        assert browser.headers.get("status") == "200 Ok"
        assert sent_body == 'cmd=_notify-validate&x=2'
        assert len(list(receiver.keys())) == 1
        notification = receiver[receiver.keys()[0]]
        assert notification.final_verdict == u'VERIFIED'
