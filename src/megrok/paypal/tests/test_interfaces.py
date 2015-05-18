# Tests for megrok.paypal.interfaces
import grok
import unittest
from zope.component import queryUtility, getUtility
from zope.schema.interfaces import IVocabularyFactory
from zope.i18nmessageid import MessageFactory
from zope.interface.verify import verifyObject, verifyClass
from megrok.paypal.interfaces import _, PaymentStatesVocabularyFactory


class TestInterfacesModule(unittest.TestCase):

    def test_message_factory(self):
        # the interfaces module provides a message factory.
        assert isinstance(_, MessageFactory)

    def test_payment_states_vocab_retrievable(self):
        # we can get a payment states vocab as a named utility
        grok.testing.grok("megrok.paypal.interfaces")
        util = queryUtility(IVocabularyFactory,
                            name="megrok.paypal.payment_states")
        assert util is not None
        assert isinstance(util, PaymentStatesVocabularyFactory)

    def test_payment_states_vocab_factory_fullfills_iface(self):
        # the payment states vocab factory fullfills interface contracts.
        grok.testing.grok("megrok.paypal.interfaces")
        util = getUtility(
            IVocabularyFactory, name="megrok.paypal.payment_states")
        verifyClass(IVocabularyFactory, PaymentStatesVocabularyFactory)
        verifyObject(IVocabularyFactory, util)
