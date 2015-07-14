import unittest
from megrok.paypal.testlayer import browser_http_layer


class TestBrowserHTTPServerLayer(unittest.TestCase):

    layer = browser_http_layer

    def test_layer_provides_expected_attributes(self):
        # make sure, the layer provides all the things we need
        assert hasattr(self.layer, 'server')
        assert hasattr(self.layer, 'ssl_server')
        assert hasattr(self.layer, 'getRootFolder')
