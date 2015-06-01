import grok
from megrok.paypal.interfaces import IPayPalPayment


class PayPalForm(grok.Model):

    grok.implements(IPayPalPayment)
