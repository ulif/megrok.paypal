"""Receiver for PayPal messages like IPN.

IPN infos:

  https://developer.paypal.com/webapps/developer/docs/
          classic/ipn/integration-guide/IPNIntro/

IPN simulator:

  https://developer.paypal.com/webapps/developer/docs/
          classic/ipn/integration-guide/IPNSimulator/

"""
import grok
import requests
from megrok.paypal.interfaces import IPayPalIPNReceiver


class PayPalIPNReceiver(grok.Container):
    """A receiver for IPN messages sent from paypal.
    """
    grok.implements(IPayPalIPNReceiver)

    validation_url = "https://www.sandbox.paypal.com/cgi-bin/webscr/"

    def got_notification(self, post_var_string):
        """The receiver got an instant payment notification (IPN).

        The `post_var_string` is the data payload sent by the notification.
        """
        pass

    def validate(self, post_var_string):
        """Ask Paypal for validation.

        Sends an HTTP POST request to `validation_url` and returns the
        result, i.e. the content of the received document.

        Returns `None` if no `validation_url` is set or the
        `post_var_string` is empty.
        """
        if not self.validation_url:
            return None
        if not post_var_string:
            return None
        response = requests.post(
            self.validation_url,
            data='cmd=_notify-validate&%s' % post_var_string)
        return response.text


class NotifyView(grok.View):
    """A view we can offer paypal for instant payment notifications.
    """
    grok.context(IPayPalIPNReceiver)
    grok.name('index')

    def update(self):
        body_data = self.request.bodyStream.getCacheStream().read()
        self.context.got_notification(body_data)

    def render(self):
        return ''
