from django_quickbooks import QUICKBOOKS_ENUMS
from django_quickbooks.objects.base import BaseObject
from django_quickbooks.validators import SchemeValidator


class AppliedToTxnAdd(BaseObject):
    fields = dict(
        TxnID=dict(validator=dict(type=SchemeValidator.IDTYPE)),
        PaymentAmount=dict(validator=dict(type=SchemeValidator.DECIMALTYPE)),
    )


class ReceivePayment(BaseObject):
    fields = dict(
        TxnID=dict(validator=dict(type=SchemeValidator.IDTYPE)),
        TimeCreated=dict(validator=dict(type=SchemeValidator.STRTYPE)),
        TimeModified=dict(validator=dict(type=SchemeValidator.STRTYPE)),
        EditSequence=dict(validator=dict(type=SchemeValidator.STRTYPE)),
        TxnDate=dict(validator=dict(type=SchemeValidator.STRTYPE)),
        Customer=dict(validator=dict(type=SchemeValidator.OBJTYPE)),
        ARAccount=dict(validator=dict(type=SchemeValidator.OBJTYPE)),
        RefNumber=dict(validator=dict(type=SchemeValidator.STRTYPE)),
        TotalAmount=dict(validator=dict(type=SchemeValidator.DECIMALTYPE)),
        PaymentMethod=dict(validator=dict(type=SchemeValidator.OBJTYPE)),
        DepositToAccount=dict(validator=dict(type=SchemeValidator.OBJTYPE)),
        AppliedToTxnAdd=dict(validator=dict(type=SchemeValidator.OBJTYPE)),
    )

    @staticmethod
    def get_service():
        from django_quickbooks.services.receivepayment import ReceivePaymentService
        return ReceivePaymentService
