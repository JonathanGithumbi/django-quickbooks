from django_quickbooks import QUICKBOOKS_ENUMS
from django_quickbooks.objects.base import BaseObject
from django_quickbooks.validators import SchemeValidator


class Transfer(BaseObject):
    fields = dict(
        TxnID=dict(validator=dict(type=SchemeValidator.IDTYPE)),
        TimeCreated=dict(validator=dict(type=SchemeValidator.STRTYPE)),
        TimeModified=dict(validator=dict(type=SchemeValidator.STRTYPE)),
        EditSequence=dict(validator=dict(type=SchemeValidator.STRTYPE)),
        TxnDate=dict(validator=dict(type=SchemeValidator.STRTYPE)),
        TransferFromAccount=dict(validator=dict(type=SchemeValidator.OBJTYPE)),
        TransferToAccount=dict(validator=dict(type=SchemeValidator.OBJTYPE)),
        Class=dict(validator=dict(type=SchemeValidator.OBJTYPE)),
        Amount=dict(validator=dict(type=SchemeValidator.DECIMALTYPE)),
        Memo=dict(validator=dict(type=SchemeValidator.STRTYPE)),
    )

    @staticmethod
    def get_service():
        from django_quickbooks.services.transfer import TransferService
        return TransferService
