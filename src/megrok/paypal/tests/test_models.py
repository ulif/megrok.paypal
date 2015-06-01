import unittest
from zope.interface.verify import verifyClass, verifyObject
from megrok.paypal.interfaces import IPayPalPaymentForm
from megrok.paypal.models import PayPalForm


class TestPayPalForm(unittest.TestCase):

    def test_iface(self):
        # PayPalForm complies with its interface
        verifyClass(IPayPalPaymentForm, PayPalForm)
        form = PayPalForm()
        verifyObject(IPayPalPaymentForm, form)
