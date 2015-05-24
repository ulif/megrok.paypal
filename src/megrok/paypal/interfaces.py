import decimal
import grok
from zope.i18nmessageid import MessageFactory
from zope.interface import Interface
from zope import schema
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from megrok.paypal.charsets import CHARSETS
from megrok.paypal.countries import COUNTRIES_DICT


_ = MessageFactory("megrok.paypal")

PAYMENT_STATE_ACTIVE = "active"
PAYMENT_STATE_CANCELLED = "cancelled"
PAYMENT_STATE_CANCELED_REVERSAL = 'canceled_reversal'
PAYMENT_STATE_CLEARED = 'cleared'
PAYMENT_STATE_COMPLETED = 'completed'
PAYMENT_STATE_CREATED = 'created'
PAYMENT_STATE_DENIED = 'denied'
PAYMENT_STATE_EXPIRED = 'expired'
PAYMENT_STATE_FAILED = 'failed'
PAYMENT_STATE_PAID = 'paid'
PAYMENT_STATE_PENDING = 'pending'
PAYMENT_STATE_PROCESSED = 'processed'
PAYMENT_STATE_REFUNDED = 'refunded'
PAYMENT_STATE_REFUSED = 'refused'
PAYMENT_STATE_REVERSED = 'reversed'
PAYMENT_STATE_REWARDED = 'rewarded'
PAYMENT_STATE_UNCLAIMED = 'unclaimed'
PAYMENT_STATE_UNCLEARED = 'uncleared'
PAYMENT_STATE_VOIDED = 'voided'


PAYMENT_STATES_DICT = dict(
    [
        (x, _(x)) for x in [
            PAYMENT_STATE_ACTIVE, PAYMENT_STATE_CANCELLED,
            PAYMENT_STATE_CANCELED_REVERSAL, PAYMENT_STATE_CLEARED,
            PAYMENT_STATE_COMPLETED, PAYMENT_STATE_CREATED,
            PAYMENT_STATE_DENIED, PAYMENT_STATE_EXPIRED,
            PAYMENT_STATE_FAILED, PAYMENT_STATE_PAID, PAYMENT_STATE_PENDING,
            PAYMENT_STATE_PROCESSED, PAYMENT_STATE_REFUNDED,
            PAYMENT_STATE_REFUSED, PAYMENT_STATE_REVERSED,
            PAYMENT_STATE_REWARDED, PAYMENT_STATE_UNCLAIMED,
            PAYMENT_STATE_UNCLEARED, PAYMENT_STATE_VOIDED
        ]
    ]
)


CHARSETS_DICT = dict([(x, _(x)) for x in CHARSETS])


class PaymentStatesVocabularyFactory(grok.GlobalUtility):
    grok.implements(IVocabularyFactory)
    grok.name("megrok.paypal.payment_states")

    def __call__(self, context):
        terms = [
            SimpleTerm(value=x[0], token=x[0], title=x[1])
            for x in PAYMENT_STATES_DICT.items()
        ]
        return SimpleVocabulary(terms)


class CharsetsVocabularyFactory(grok.GlobalUtility):
    grok.implements(IVocabularyFactory)
    grok.name("megrok.paypal.charsets")

    def __call__(self, context):
        terms = [SimpleTerm(value=x[0], token=x[0], title=x[1])
                 for x in CHARSETS_DICT.items()]
        return SimpleVocabulary(terms)


class CountriesVocabularyFactory(grok.GlobalUtility):
    grok.implements(IVocabularyFactory)
    grok.name("megrok.paypal.countries")

    def __call__(self, context):
        terms = [SimpleTerm(value=x[0], token=x[0], title=x[1])
                 for x in COUNTRIES_DICT.items()]
        return SimpleVocabulary(terms)


class IPayPalStandardBase(Interface):

    status = schema.Choice(
        title=u"Status",
        vocabulary="megrok.paypal.payment_states",
        required=True,
        )

    # transaction and notification related
    business = schema.TextLine(
        title=u"Merchant email or id",
        description=(
            u"Your PayPal ID or an email address associated "
            u"with your PayPal account. Email addresses must be confirmed."),
        max_length=127,
        )

    charset = schema.Choice(
        title=u"Charset",
        description=(
            u"Sets the character set and character encoding "
            u"for the billing information/log-in page on the PayPal "
            u"website. In addition, this variable sets the same values "
            u"for information that you send to PayPal in your HTML "
            u"button code. The default is based on the language "
            u"encoding settings in your Account Profile."),
        vocabulary="megrok.paypal.charsets",
        )

    custom = schema.TextLine(
        title=u"Custom",
        description=(
            u"Pass-through variable for your own tracking purposes, "
            u"which buyers do not see."
        ),
        max_length=255,
        )

    notify_version = schema.Decimal(
        title=u"notify_version",
        default=decimal.Decimal("0.00"),
    )

    parent_txn_id = schema.Int(
        title=u"Parent transaction ID",
        default=0,
    )

    receiver_email = schema.TextLine(
        title=u"???",
        max_length=127,
    )

    receiver_id = schema.TextLine(
        title=u"???",
        max_length=127,
    )

    residence_country = schema.Choice(
        title=u"Residence country",
        vocabulary="megrok.paypal.countries",
    )
