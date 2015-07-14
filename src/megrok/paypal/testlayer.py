"""Testlayers.
"""
import megrok.paypal.tests
from megrok.paypal.testing import BrowserHTTPServerLayer


browser_http_layer = BrowserHTTPServerLayer(
    megrok.paypal.tests, 'ftesting.zcml')
