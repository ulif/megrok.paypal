import unittest
from zope.interface.verify import verifyClass, verifyObject
from megrok.paypal.interfaces import IPayPalPayment
from megrok.paypal.models import PayPalForm


class TestPayPalForm(unittest.TestCase):

    def test_iface(self):
        # PayPalForm complies with its interface
        verifyClass(IPayPalPayment, PayPalForm)
        form = PayPalForm()
        verifyObject(IPayPalPayment, form)
