megrok.paypal
*************

PayPal support for Grok_/Zope_ applications.

*This package is not in a useable state, currently!*

We aim to support integration with `PayPal Payments Standard`_.

Currently, no other PayPal service is supported. `PayPal Payments
Standard`_ provides two ways of payment notification: Payment Data
Transfer (PDT) or Instant Payment Notification (IPN). At the moment
we only support IPN.

Instant Payment Notifications (IPN)
===================================

IPN roughly works like this: when a user wants to pay something on the
PayPal site, a request is sent from PayPal to your site. You must
handle this request and must validate the data sent in this request
for successful processing of the whole payment.


.. _Grok:: http://grok.zope.org/
.. _Zope:: https://zope.org/
.. _`PayPal Payments Standard`:: https://developer.paypal.com/webapps/developer/docs/classic/paypal-payments-standard/integration-guide/wp_standard_overview/
