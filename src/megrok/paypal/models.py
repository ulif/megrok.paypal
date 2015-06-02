import decimal
import grok
from megrok.paypal.interfaces import IPayPalPaymentForm


class PayPalForm(object):

    grok.implements(IPayPalPaymentForm)

    @property
    def notify_url(self):
        return None

    @property
    def return_url(self):
        return None

    @property
    def cancel_return(self):
        return None

    def __init__(self, business=None, item_name=None,
                  amount=decimal.Decimal("0.00"), invoice=None):
        self.invoice = invoice
        self.business = business
        self.item_name = item_name
        self.amount = amount
