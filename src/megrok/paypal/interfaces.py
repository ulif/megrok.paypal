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


class AddressStatusVocabularyFactory(grok.GlobalUtility):
    grok.implements(IVocabularyFactory)
    grok.name("megrok.paypal.address_status")

    def __call__(self, context):
        terms = [SimpleTerm(value=x[0], token=x[0], title=x[1])
                 for x in [('confirmed', _('confirmed')),
                           ('unconfrimed', _('unconfirmed'))]]
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
            u"Email address or account ID of the payment recipient (that is, "
            u"the merchant). Equivalent to the values of receiver_email "
            u"(if payment is sent to primary account) and business set in "
            u"the Website Payment HTML. Value of this variable is normalized "
            u"to lowercase characters"
        ),
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
            "Custom value as passed by you, the merchant. These are "
            u"pass-through variables that are never presented to your "
            u"customer"
        ),
        max_length=255,
    )

    notify_version = schema.Decimal(
        title=u"notify_version",
        description=u"Message's version number",
        default=decimal.Decimal("0.00"),
    )

    parent_txn_id = schema.TextLine(
        title=u"Parent transaction ID",
        description=(
            u"In the case of a refund, reversal, or canceled reversal, "
            u"this variable contains the txn_id of the original "
            u"transaction, while txn_id contains a new ID for the new "
            u"transaction."
        ),
        max_length=19,
    )

    receiver_email = schema.TextLine(
        title=u"Receiver Email",
        description=(
            u"Primary email address of the payment recipient (that is, "
            u"the merchant). If the payment is sent to a non-primary "
            u"email address on your PayPal account, the receiver_email is "
            u"still your primary email. Value of this variable is normalized "
            u"to lowercase characters."
        ),
        max_length=127,
    )

    receiver_id = schema.TextLine(
        title=u"Receiver ID",
        description=(
            u"Unique account ID of the payment recipient (i.e., the "
            u"merchant). This is the same as the recipient's referral ID."
        ),
        max_length=13,
    )

    residence_country = schema.Choice(
        title=u"(Merchant's) residence country",
        description=(
            u"ISO 3166 country code associated with the country of residence."
        ),
        vocabulary="megrok.paypal.countrycodes",
    )

    test_ipn = schema.Bool(
        title=u"Is message IPN test?",
        description=(
            u"Whether the message is a test message. It is one of the "
            u"following values: 1 - the message is directed to the Sandbox"
        ),
        default=False,
    )

    txn_id = schema.TextLine(
        title=u"Transaction ID",
        description=(
            u"The merchant's original transaction identification "
            u"number for the payment from the buyer, against which the "
            u"case was registered."
        ),
        max_length=19,
    )

    txn_type = schema.TextLine(
        title=u"Transacion Type",
        description=(
            u"The kind of transaction for which the IPN message was sent."
        ),
        max_length=128,
    )

    verify_sign = schema.TextLine(
        title=u"Verify sign",
        description=(
            u"Encrypted string used to validate the authenticity of the "
            u"transaction"
        ),
    )

    #
    # Buyer related infos
    #
    address_country = schema.TextLine(
        title=u"Country",
        description=u"Country of customer's address",
        max_length=64,
    )

    address_city = schema.TextLine(
        title=u"City",
        description=u"City of customer's address",
        max_length=40,
    )

    address_country_code = schema.Choice(
        title=u"Country Code",
        description=(
            u"ISO 3166.1 country code (2-letter) associated with "
            u"customer's address."
            ),
        vocabulary="megrok.paypal.contrycodes",
    )

    address_name = schema.TextLine(
        title=u"Name",
        description=(
            u"Name used with address (included when the customer "
            u"provides a Gift Address)"
            ),
        max_length=128,
    )

    address_state = schema.TextLine(
        title=u"State",
        description=u"State of customer's address",
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

    item_nameX = schema.TextLine(
        title=u"Item Name",
        description=(
            u"Item name as passed by you, the merchant. Or, if not "
            u"passed by you, as entered by your customer. If this is a "
            u"shopping cart transaction, PayPal will append the number of "
            u"the item (e.g., item_name1, item_name2, and so forth)."
            ),
        max_length=127,
        )

    item_numberX = schema.TextLine(
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

    mc_currency = schema.TextLine(
        title=u"Payment Currency",
        description=(
            u"For payment IPN notifications, this is the currency of the "
            u"payment. For non-payment subscription IPN notifications "
            u"(i.e., txn_type= signup, cancel, failed, eot, or modify), "
            u"this is the currency of the subscription. For payment "
            u"subscription IPN notifications, it is the currency of the "
            u"payment (i.e., txn_type = subscr_payment)"
            ),
        default=u"USD",
        max_length=32,
        )

    mc_fee = schema.Decimal(
        title=u"Transaction Fee",
        description=(
            u"Transaction fee associated with the payment. mc_gross minus "
            u"mc_fee equals the amount deposited into the receiver_email "
            u"account. Equivalent to payment_fee for USD payments. If this "
            u"amount is negative, it signifies a refund or reversal, and "
            u"either of those payment statuses can be for the full or partial "
            u"amount of the original transaction fee."
            ),
        default=decimal.Decimal("0.00"),
        )

    mc_gross = schema.Decimal(
        title=u"Payment Gross",
        description=(
            u"Full amount of the customer's payment, before transaction "
            u"fee is subtracted. Equivalent to payment_gross for USD "
            u"payments. If this amount is negative, it signifies a refund "
            u"or reversal, and either of those payment statuses can be for "
            u"the full or partial amount of the original transaction."
            ),
        default=decimal.Decimal("0.00"),
        )

    mc_handling = schema.Decimal(
        title=u"Handling fees",
        description=u"Total handling amount associated with the transaction.",
        default=decimal.Decimal("0.00"),
        )

    mc_shipping = schema.Decimal(
        title=u"Shipping costs",
        description=u"Total shipping amount associated with the transaction.",
        default=decimal.Decimal("0.00"),
        )

    memo = schema.TextLine(
        title=u"Memo",
        description=(
            u"Memo as entered by your customer in PayPal Website Payments "
            u"note field."
            ),
        max_length=255,
        )

    num_cart_items = schema.Int(
        title=u"Number of cart items",
        description=(
            u"If this is a PayPal Shopping Cart transaction, number of "
            u"items in cart."
            ),
        default=0,
        )

    option_name1 = schema.TextLine(
        title=u"Option name 1",
        description=(
            u"Option 1 name as requested by you. PayPal appends the "
            u"number of the item where x represents the number of the "
            u"shopping cart detail item (e.g., option_name1, option_name2)."
            ),
        max_length=64,
        )

    option_name2 = schema.TextLine(
        title=u"Option name 2",
        description=(
            u"Option 2 name as requested by you. PayPal appends the "
            u"number of the item where x represents the number of the "
            u"shopping cart detail item (e.g., option_name2, option_name2)."
            ),
        max_length=64,
        )

    payer_status = schema.TextLine(
        title=u"Payer Status",
        description=(
            u"Whether the customer has a verified PayPal account. "
            u"verified - Customer has a verified PayPal account. "
            u"unverified - Customer has an unverified PayPal account."
            ),
        max_length=10,
        )

    payment_date = schema.TextLine(
        title=u"Payment Date",
        description=(
            u"Time/date stamp generated by PayPal."
            u"Format: HH:MM:SS DD Mmm YY, YYYY PST"
            ),
        max_length=28,
        )

    payment_gross = schema.Decimal(
        title=u"Payment Gross",
        description=(
            u"Full USD amount of the customer's payment, "
            u"before transaction fee is subtracted. Will be empty for "
            u"non-USD payments. This is a legacy field replaced by "
            u"mc_gross. If this amount is negative, it signifies a refund "
            u"or reversal, and either of those payment statuses can be for "
            u"the full or partial amount of the original transaction."
            ),
        default=decimal.Decimal("0.00"),
        )

    payment_status = schema.TextLine(
        title=u"Payment Status",
        description=(
            u"The status of the payment: "

            u"Canceled_Reversal: A reversal has been canceled. For "
            u"example, you won a dispute with the customer, and the "
            u"funds for the transaction that was reversed have been "
            u"returned to you. "
            u" "
            u"Completed: The payment has been completed, and the funds "
            u"have been added successfully to your account balance. "
            u" "
            u"Created: A German ELV payment is made using Express Checkout. "
            u" "
            u"Denied: The payment was denied. This happens only if the "
            u"payment was previously pending because of one of the reasons "
            u"listed for the pending_reason variable or the "
            u"Fraud_Management_Filters_x variable. "
            u" "
            u"Expired: This authorization has expired and cannot be captured."
            u" "
            u"Failed: The payment has failed. This happens only if "
            u"the payment was made from your customer's bank account."
            u" "
            u"Pending: The payment is pending. See pending_reason for "
            u"more information."
            u" "
            u"Refunded: You refunded the payment."
            u" "
            u"Reversed: A payment was reversed due to a chargeback or "
            u"other type of reversal. The funds have been removed from "
            u"your account balance and returned to the buyer. The "
            u"reason for the reversal is specified in the ReasonCode element."
            u" "
            u"Processed: A payment has been accepted."
            u" "
            u"Voided: This authorization has been voided."
            ),
        max_length=17,
        )

    payment_type = schema.TextLine(
        title=u"Payment Type",
        description=(
            u"echeck: This payment was funded with an eCheck. "
            u"instant: This payment was funded with PayPal balance, "
            u"credit card, or Instant Transfer."
            ),
        max_length=7,
        )

    pending_reason = schema.TextLine(
        title=u"Pending Reason",
        description=(
            u"This variable is set only if payment_status is Pending. "
            u" "
            u"address: The payment is pending because your customer did "
            u"not include a confirmed shipping address and your "
            u"Payment Receiving Preferences is set yo allow you to "
            u"manually accept or deny each of these payments. To change "
            u"your preference, go to the Preferences section of your Profile."
            u" "
            u"authorization: You set the payment action to Authorization "
            u"and have not yet captured funds."
            u" "
            u"echeck: The payment is pending because it was made by an "
            u"eCheck that has not yet cleared."
            u" "
            u"intl: The payment is pending because you hold a non-U.S. "
            u"account and do not have a withdrawal mechanism. You must "
            u"manually accept or deny this payment from your Account "
            u"Overview."
            u" "
            u"multi_currency: You do not have a balance in the currency "
            u"sent, and you do not have your profiles's Payment Receiving "
            u"Preferences option set to automatically convert and accept "
            u"this payment. As a result, you must manually accept or "
            u"deny this payment."
            u" "
            u"order: You set the payment action to Order and have not "
            u"yet captured funds."
            u" "
            u"paymentreview: The payment is pending while it is reviewed "
            u"by PayPal for risk."
            u" "
            u"regulatory_review: The payment is pending because "
            u"PayPal is reviewing it for compliance with government "
            u"regulations. PayPal will complete this review within "
            u"72 hours. When the review is complete, you will receive "
            u"a second IPN message whose payment_status/reason code "
            u"variables indicate the result."
            u" "
            u"unilateral: The payment is pending because it was made "
            u"to an email address that is not yet registered or confirmed."
            u" "
            u"upgrade: The payment is pending because it was made via "
            u"credit card and you must upgrade your account to Business "
            u"or Premier status before you can receive the funds. "
            u"upgrade can also mean that you have reached the monthly "
            u"limit for transactions on your account."
            u" "
            u"verify: The payment is pending because you are not yet "
            u"verified. You must verify your account before you can "
            u"accept this payment."
            u" "
            u"other: The payment is pending for a reason other than "
            u"those listed above. For more information, contact PayPal "
            u"Customer Service."
            ),
        max_length=14,
        )

    protection_eligibility = schema.TextLine(
        title=u"Protection Eligibility",
        description=(
            u"ExpandedSellerProtection: Seller is protected by Expanded "
            u"seller protection "
            u"SellerProtection: Seller is protected by PayPal's "
            u"Seller Protection Policy "
            u"None: Seller is not protected under Expanded seller "
            u"protection nor the Seller Protection Policy"
            ),
        max_length=32,
        )

    quantity = schema.Int(
        title=u"Quantity",
        description=(
            u"Quantity as entered by your customer or as passed by "
            u"you, the merchant. If this is a shopping cart "
            u"transaction, PayPal appends the number of the item "
            u"(e.g. quantity1, quantity2)."
            ),
        default=1,
        )

    reason_code = schema.TextLine(
        title=u"Reason Code",
        description=(
            u"This variable is set if payment_status is Reversed, "
            u"Refunded, Canceled_Reversal, or Denied. "
            u" "
            u"adjustment_reversal: Reversal of an adjustment. "
            u" "
            u"admin_fraud_reversal: The transaction has been reversed "
            u"due to fraud detected by PayPal administrators."
            u" "
            u"admin_reversal: The transaction has been reversed by "
            u"PayPal administrators."
            u" "
            u"buyer-complaint: The transaction has been reversed due "
            u"to a complaint from your customer."
            u" "
            u"chargeback: The transaction has been reversed due to "
            u"a chargeback by your customer."
            u" "
            u"chargeback_reimbursement: Reimbursement for a chargeback."
            u" "
            u"chargeback_settlement: Settlement of a chargeback."
            u" "
            u"guarantee: The transaction has been reversed because your "
            u"customer exercised a money-back guarantee."
            u" "
            u"other: Unspecified reason."
            u" "
            u"refund: The transaction has been reversed because you "
            u"gave the customer a refund."
            u" "
            u"regulatory_block: PayPal blocked the transaction due to a "
            u"violation of a government regulation. In this case, "
            u"payment_status is Denied."
            u" "
            u"regulatory_reject: PayPal rejected the transaction due "
            u"to a violation of a government regulation and returned "
            u"the funds to the buyer. In this case, payment_status is Denied."
            u" "
            u"regulatory_review_exceeding_sla: PayPal did not complete "
            u"the review for compliance with government regulations "
            u"within 72 hours, as required. Consequently, PayPal "
            u"auto-reversed the transaction and returned the funds to "
            u"the buyer. In this case, payment_status is Denied. Note "
            u"that 'sla' stand for 'service level agreement'."
            u" "
            u"unauthorized_claim: The transaction has been reversed "
            u"because it was not authorized by the buyer."
            u" "
            u"unauthorized_spoof: The transaction has been reversed due to "
            u"a customer dispute in which an unauthorized spoof is suspected."
            ),
        max_length=15,
        )

    remaining_settle = schema.Decimal(
        title=u"Remaining Settle",
        description=(
            u"Remaining amount that can be captured with Authorization "
            u"and Capture"
            ),
        default=decimal.Decimal("0.00"),
        )

    settle_amount = schema.Decimal(
        title=u"Settle Amount",
        description=(
            u"Amount that is deposited into the account's primary balance "
            u"after a currency conversion from automatic conversion "
            u"(through your Payment Receiving Preferences) or manual "
            u"conversion (through manually accepting a payment)."
            ),
        default=decimal.Decimal("0.00"),
        )

    settle_currency = schema.TextLine(
        title=u"Settle Currency",
        description=u"Currency of settle_amount",
        max_length=32,
        )

    shipping = schema.Decimal(
        title=u"Shipping",
        description=(
            u"Shipping charges associated with this transaction. "
            u"Format: unsigned, no currency symbol, two decimal places."
            ),
        default=decimal.Decimal("0.00"),
        )

    shipping_method = schema.TextLine(
        title=u"Shipping Method",
        description=(
            u"The name of a shipping method from the Shipping "
            u"Calculations section of the merchant's account profile. "
            u"The buyer selected the named shipping method for this "
            u"transaction."
            ),
        max_length=255,
        )

    tax = schema.Decimal(
        title=u"Tax",
        description=(
            u"Amount of tax charged on payment. PayPal appends the "
            u"number of the item (e.g., item_name1, item_name2). The "
            u"taxx variable is included only if there was a specific tax "
            u"amount applied to a particular shopping cart item. Because "
            u"total tax may apply to other items in the cart, the sum "
            u"of taxx might not total to tax."
            ),
        default=decimal.Decimal("0.00"),
        )

    transaction_entity = schema.TextLine(
        title=u"Transaction Entity",
        description=u"Authorization and Capture transaction entity",
        max_length=7,
        )


class IPayPalPayment(Interface):

    business = schema.TextLine(
        title=u"Merchant email or id",
        description=(
            u"Email address or account ID of the payment recipient (that is, "
            u"the merchant). Equivalent to the values of receiver_email "
            u"(if payment is sent to primary account) and business set in "
            u"the Website Payment HTML. Value of this variable is normalized "
            u"to lowercase characters"
        ),
        max_length=127,
        required=True,
        )

    amount = schema.Decimal(
        title=u"Amount",
        default=decimal.Decimal("0.00"),
        required=True,
        )

    notify_url = schema.URI(
        title=u"URL where PayPal should deliver notifications.",
        required=True,
        )

    return_url = schema.URI(
        title=u"Where users are sent after successfull payment.",
        required=True,
        )

    cancel_return = schema.URI(
        title=u"Where users are sent after payment cancellation.",
        required=True,
        )

    item_name = schema.TextLine(
        title=u"Item Name",
        required=False,
        )

    invoice = schema.TextLine(
        title=u"Unique Invoice ID",
        required=False,
        )

