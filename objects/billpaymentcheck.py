from django_quickbooks import QUICKBOOKS_ENUMS
from django_quickbooks.objects.base import BaseObject
from django_quickbooks.validators import SchemeValidator

class BillPaymentCheck(BaseObject):
    fields = dict(
        TxnID=dict(validator=dict(type=SchemeValidator.IDTYPE)),
        TimeCreated=dict(validator=dict(type=SchemeValidator.STRTYPE)),
        TimeModified=dict(validator=dict(type=SchemeValidator.STRTYPE)),
        EditSequence=dict(validator=dict(type=SchemeValidator.STRTYPE)),
        PayeeEntity=dict(validator=dict(type=SchemeValidator.OBJTYPE)),
        APAccount=dict(validator=dict(type=SchemeValidator.OBJTYPE)),
        TxnDate=dict(validator=dict(type=SchemeValidator.STRTYPE)),
        BankAccount=dict(validator=dict(type=SchemeValidator.OBJTYPE)), 
        RefNumber=dict(validator=dict(type=SchemeValidator.STRTYPE)),
        Memo=dict(validator=dict(type=SchemeValidator.STRTYPE)),
        AppliedToTxnAdd=dict(validator=dict(type=SchemeValidator.OBJTYPE)),
        AppliedToTxnMod=dict(validator=dict(type=SchemeValidator.OBJTYPE)),
    )

    @staticmethod
    def get_service():
        from django_quickbooks.services.billpaymentcheck import BillPaymentCheckService
        return BillPaymentCheckService
