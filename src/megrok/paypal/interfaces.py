import grok
from zope.i18nmessageid import MessageFactory
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm


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


class PaymentStatesVocabularyFactory(grok.GlobalUtility):
    grok.provides(IVocabularyFactory)
    grok.name("megrok.paypal.payment_states")

    def __call__(self, context):
        terms = [
            SimpleTerm(value=x[0], token=x[0], title=x[1])
            for x in PAYMENT_STATES_DICT.items()
        ]
        return SimpleVocabulary(terms)
