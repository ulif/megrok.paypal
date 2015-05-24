# Tests for megrok.paypal.interfaces
import grok
import unittest
from zope.component import queryUtility, getUtility, globalSiteManager
from zope.schema.interfaces import IVocabularyFactory, IVocabulary
from zope.i18nmessageid import MessageFactory
from zope.interface.verify import verifyObject, verifyClass
from megrok.paypal.interfaces import (
    _, PaymentStatesVocabularyFactory, CharsetsVocabularyFactory,
    CountriesVocabularyFactory,
)


class TestInterfacesModule(unittest.TestCase):

    def setUp(self):
        # make sure, grokked components are unregistered at the beginning
        for name in [
                "megrok.paypal.payment_states",
                "megrok.paypal.charsets",
                "megrok.paypal.countries"]:
            util = queryUtility(
                IVocabularyFactory, name=name)
            if util is not None:
                globalSiteManager.unregisterUtility(util)

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

    def test_charsets_vocab_retrievable(self):
        # we can get a charsets vocab as a named utility
        grok.testing.grok("megrok.paypal.interfaces")
        util = queryUtility(IVocabularyFactory,
                            name="megrok.paypal.charsets")
        assert util is not None
        assert isinstance(util, CharsetsVocabularyFactory)

    def test_countries_vocab_retrievable(self):
        # we can get a countries vocab as a named utility
        grok.testing.grok("megrok.paypal.interfaces")
        util = queryUtility(IVocabularyFactory,
                            name="megrok.paypal.countries")
        assert util is not None
        assert isinstance(util, CountriesVocabularyFactory)

    def test_payment_states_vocab_factory_fullfills_iface(self):
        # the payment states vocab factory fullfills interface contracts.
        factory = PaymentStatesVocabularyFactory()
        verifyClass(IVocabularyFactory, PaymentStatesVocabularyFactory)
        verifyObject(IVocabularyFactory, factory)

    def test_charsets_vocab_factory_fullfills_iface(self):
        # the charsets vocab factory fullfills interface contracts.
        factory = CharsetsVocabularyFactory()
        verifyClass(IVocabularyFactory, CharsetsVocabularyFactory)
        verifyObject(IVocabularyFactory, factory)

    def test_countries_vocab_factory_fullfills_iface(self):
        # the countries vocab factory fullfills interface contracts.
        factory = CountriesVocabularyFactory()
        verifyClass(IVocabularyFactory, CountriesVocabularyFactory)
        verifyObject(IVocabularyFactory, factory)

    def test_payment_states_vocab_fullfills_iface(self):
        # the delivered vocabulary fullfills all interface contracts
        factory = PaymentStatesVocabularyFactory()
        vocab = factory(context=None)
        verifyObject(IVocabulary, vocab)

    def test_charsets_vocab_fullfills_iface(self):
        # the delivered vocabulary fullfills all interface contracts
        factory = CharsetsVocabularyFactory()
        vocab = factory(context=None)
        verifyObject(IVocabulary, vocab)

    def test_countries_vocab_fullfills_iface(self):
        # the delivered vocabulary fullfills all interface contracts
        factory = CountriesVocabularyFactory()
        vocab = factory(context=None)
        verifyObject(IVocabulary, vocab)


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(TestInterfacesModule))
    return suite
