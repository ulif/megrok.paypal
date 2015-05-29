import decimal
import grok
from zope.i18nmessageid import MessageFactory
from zope.interface import Interface
from zope import schema
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from megrok.paypal.charsets import CHARSETS
from megrok.paypal.countries import (
    COUNTRIES_DICT, COUNTRY_CODES_DICT,
)


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


class CountryCodesVocabularyFactory(grok.GlobalUtility):
    grok.implements(IVocabularyFactory)
    grok.name("megrok.paypal.countrycodes")

    def __call__(self, context):
        terms = [SimpleTerm(value=x[0], token=x[0], title=x[1])
                 for x in COUNTRY_CODES_DICT.items()]
        return SimpleVocabulary(terms)


class IPayPalStandardBase(Interface):

    #
    # Transaction and notification-related vars.
    #
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

    test_ipn = schema.Bool(
        title=u"Test IPN?",
        default=False,
    )

    txn_id = schema.TextLine(
        title=u"Transaction ID",
        description=u"PayPal transaction ID",
        max_length=19,
    )

    txn_type = schema.TextLine(
        title=u"Transacion Type",
        description=u"PayPal transaction type.",
        max_length=128,
    )

    verify_sign = schema.TextLine(
        title=u"???",
        max_length=255,
    )

    #
    # Buyer related infos
    #
    address_country = schema.TextLine(
        title=u"Country",
        max_length=64,
    )

    address_city = schema.TextLine(
        title=u"City",
        max_length=40,
    )

    address_country_code = schema.Choice(
        title=u"Country Code",
        description=u"ISO 3166.1 country code (2-letter)",
        vocabulary="megrok.paypal.contrycodes",
    )

    address_name = schema.TextLine(
        title=u"Name",
        max_length=128,
    )

    address_state = schema.TextLine(
        title=u"State",
        max_length=40,
    )

    address_status = schema.TextLine(
        title=u"Status",
        description=(
            u"Whether the customer provided a confirmed address. It "
            u"is one of the following values: "
            u"confirmed - Customer provided a confirmed address. "
            u"unconfirmed - Customer provided an unconfirmed address."),
        max_length=11,
    )

    address_street = schema.TextLine(
        title=u"Street",
        description=u"Customer's street address.",
        max_length=200,
    )

    address_zip = schema.TextLine(
        title=u"Zip code",
        description=u"Zip code of customer's address.",
        max_length=20,
    )

    contact_phone = schema.TextLine(
        title=u"Phone",
        description=u"Customer's telephone number.",
        max_length=20,
    )

    first_name = schema.TextLine(
        title=u"First Name",
        description=u"Customer's first name",
        max_length=64,
    )

    last_name = schema.TextLine(
        title=u"Last Name",
        description=u"Customer's last name",
        max_length=64,
    )

    payer_business_name = schema.TextLine(
        title=u"Payer Business Name",
        description=u"Customer's company name, if customer is a business",
        max_length=127,
    )

    payer_email = schema.TextLine(
        title=u"Payer Email",
        description=(
            u"Customer's primary email address. Use this email "
            u"to provide any credits."),
        max_length=127,
    )

    payer_id = schema.TextLine(
        title=u"Payer ID",
        description=u"Unique customer ID.",
        max_length=13,
    )

    #
    # Payment info vars
    # (https://developer.paypal.com/docs/classic/ipn/integration-guide/
    #  IPNandPDTVariables/)
    #
    auth_amount = schema.Decimal(
        title=u"Amount",
        description=u"Authorization amount",
        default=decimal.Decimal("0.00"),
        )

    auth_exp = schema.TextLine(
        title=u"Authorization Expiration Datetime",
        description=(
            u"Authorization expiration date and time, in the following "
            u"format: HH:MM:SS DD Mmm YY, YYYY PST"
            ),
        max_length=28,
        )

    auth_id = schema.TextLine(
        title=u"Auth ID",
        description=u"Authorization Identification Number",
        max_length=19,
        )

    auth_status = schema.TextLine(
        title=u"Auth Status",
        description=u"Status of Authorization",
        max_length=9,
        )

    exchange_rate = schema.Decimal(
        title=u"Exchange Rate",
        description=(
            u"Exchange rate used if a currency conversion occurred."
            ),
        default=decimal.Decimal("1.00"),
        )

    invoice = schema.TextLine(
        title=u"Invoice",
        description=(
            u"Pass-through variable you can use to identify your "
            u"Invoice Number for this purchase. If omitted, no variable "
            u"is passed back."
            ),
        max_length=127,
        )

    item_name = schema.TextLine(
        title=u"Item Name",
        description=(
            u"Item name as passed by you, the merchant. Or, if not "
            u"passed by you, as entered by your customer. If this is a "
            u"shopping cart transaction, PayPal will append the number of "
            u"the item (e.g., item_name1, item_name2, and so forth)."
            ),
        max_length=127,
        )

    item_number = schema.TextLine(
        title=u"Item Number",
        description=(
            u"Pass-through variable for you to track purchases. It will "
            u"get passed back to you at the completion of the payment. "
            u"If omitted, no variable will be passed back to you. If this "
            u"is a shopping cart transaction, PayPal will append the "
            u"number of the item (e.g., item_number1, item_number2, and "
            u"so forth)"
            ),
        max_length=127,
        )
