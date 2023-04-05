from django_quickbooks.objects.base import BaseObject
from django_quickbooks.validators import SchemeValidator


class CreditMemoLine(BaseObject):
    fields = dict(
        Item=dict(validator=dict(type=SchemeValidator.OBJTYPE)),
        Desc=dict(validator=dict(type=SchemeValidator.STRTYPE)),
        Amount=dict(validator=dict(type=SchemeValidator.DECIMALTYPE)),

    )


class CreditMemo(BaseObject):
    fields = dict(
        TxnID=dict(validator=dict(type=SchemeValidator.IDTYPE)),
        TimeCreated=dict(validator=dict(type=SchemeValidator.STRTYPE)),
        TimeModified=dict(validator=dict(type=SchemeValidator.STRTYPE)),
        EditSequence=dict(validator=dict(type=SchemeValidator.STRTYPE)),
        Customer=dict(validator=dict(type=SchemeValidator.OBJTYPE)),
        ARAccount=dict(validator=dict(type=SchemeValidator.OBJTYPE)),
        TxnDate=dict(validator=dict(type=SchemeValidator.STRTYPE)),
        RefNumber=dict(validator=dict(type=SchemeValidator.STRTYPE)),
        Memo=dict(validator=dict(type=SchemeValidator.STRTYPE)),
        CreditMemoLine=dict(validator=dict(type=SchemeValidator.OBJTYPE)),
    )

    @staticmethod
    def get_service():
        from django_quickbooks.services.creditmemo import CreditMemoService
        return CreditMemoService
