from django_quickbooks import QUICKBOOKS_ENUMS
from django_quickbooks.objects.base import BaseObject
from django_quickbooks.validators import SchemeValidator


class AppliedToTxnAdd(BaseObject):
    fields = dict(
        TxnID=dict(validator=dict(type=SchemeValidator.IDTYPE)),
        PaymentAmount=dict(validator=dict(type=SchemeValidator.DECIMALTYPE)),
    )
