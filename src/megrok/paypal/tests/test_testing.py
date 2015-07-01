# tests for testing.
import requests
import unittest
from megrok.paypal.testing import (
    http_server, StoppableHTTPServer, HTTPServerLayer)


class TestHTTPServerContextManager(unittest.TestCase):

    def test_http_server(self):
        # we can use the http_server context manager
        with http_server() as server:
            response = requests.get(server.url)
        self.assertEqual(response.text, 'Ok')


class TestStoppableHTTPServer(unittest.TestCase):

    layer = HTTPServerLayer

    def test_get(self):
        # we can GET docs from server
        response = requests.get(self.layer.server.url)
        self.assertEqual(response.text, 'Ok')

    def test_post(self):
        # we can POST data to server
        response = requests.post(self.layer.server.url)
        self.assertEqual(response.text, u'VERIFIED')

    def test_post_data_stored(self):
        # data we POST to the server is stored
        with http_server() as server:
            requests.post(self.layer.server.url, data="var1=1&var2=foo")
            body1 = self.layer.server.last_request_body
            requests.post(self.layer.server.url, data="var2=bar&var1=baz")
            body2 = self.layer.server.last_request_body
        assert body1 == 'var1=1&var2=foo'
        assert body2 == 'var2=bar&var1=baz'

    def test_post_content_type_stored(self):
        # the content type of last request is stored
        with http_server() as server:
            requests.post(self.layer.server.url, data={'var': 'value'})
            content_type = self.layer.server.last_request_content_type
        assert content_type == 'application/x-www-form-urlencoded'

    def test_ssl(self):
        # we can POST data with SSL
        response = requests.post(self.layer.ssl_server.url, verify=False)
        self.assertEqual(response.text, u'VERIFIED')

    def test_invalid_post(self):
        # we can POST and retrieve invalid
        self.layer.server.paypal_mode = 'invalid'
        response = requests.post(self.layer.server.url)
        self.assertEqual(response.text, u'INVALID')
