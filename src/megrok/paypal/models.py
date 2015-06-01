import grok
from megrok.paypal.interfaces import IPayPalPaymentForm


class PayPalForm(grok.Model):

    grok.implements(IPayPalPaymentForm)
