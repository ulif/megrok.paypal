# tests for testing.
import requests
import unittest
from megrok.paypal.testing import http_server


class TestHTTPServerContextManager(unittest.TestCase):

    def test_http_server(self):
        # we can use the http_server context manager
        with http_server() as server:
            response = requests.get(server.url)
        self.assertEqual(response.text, 'Ok')


class TestFakePaypalServer(unittest.TestCase):

    def test_get(self):
        # we can GET docs from server
        with http_server() as server:
            response = requests.get(server.url)
        self.assertEqual(response.text, 'Ok')

    def test_post(self):
        # we can POST data to server
        with http_server() as server:
            response = requests.post(server.url)
        self.assertEqual(response.text, u'VERIFIED')

    def test_ssl(self):
        # we can POST data with SSL
        with http_server(do_ssl=True) as server:
            response = requests.post(server.url, verify=False)
        self.assertEqual(response.text, u'VERIFIED')

    def test_invalid_post(self):
        # we can POST and retrieve invalid
        with http_server(paypal_mode="invalid") as server:
            response = requests.post(server.url)
        self.assertEqual(response.text, u'INVALID')

    def test_post_data_stored(self):
        # data we POST to the server is stored
        with http_server() as server:
            requests.post(server.url, data="var1=1&var2=foo")
            body1 = server.last_request_body
            requests.post(server.url, data="var2=bar&var1=baz")
            body2 = server.last_request_body
        assert body1 == 'var1=1&var2=foo'
        assert body2 == 'var2=bar&var1=baz'

    def test_post_content_type_stored(self):
        # the content type of last request is stored
        with http_server() as server:
            requests.post(server.url, data={'var': 'value'})
            content_type = server.last_request_content_type
        assert content_type == 'application/x-www-form-urlencoded'
