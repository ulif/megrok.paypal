"""Receiver for PayPal messages like IPN.

IPN infos:

  https://developer.paypal.com/webapps/developer/docs/
          classic/ipn/integration-guide/IPNIntro/

IPN simulator:

  https://developer.paypal.com/webapps/developer/docs/
          classic/ipn/integration-guide/IPNSimulator/

"""
import grok
from megrok.paypal.interfaces import IPayPalIPNReceiver


class PayPalIPNReceiver(grok.Container):
    """A receiver for IPN messages sent from paypal.
    """
    grok.implements(IPayPalIPNReceiver)

    response_uri = "https://www.sandbox.paypal.com/cgi-bin/webscr/"

    def got_notification(self, post_var_string):
        """The receiver got an instant payment notification (IPN).

        The `post_var_string` is the data payload sent by the notification.
        """
        pass


class NotifyView(grok.View):
    """A view we can offer paypal for instant payment notifications.
    """
    grok.context(IPayPalIPNReceiver)
    grok.name('notify')

    def render(self):
        return ''
