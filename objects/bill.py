from django_quickbooks import QUICKBOOKS_ENUMS
from django_quickbooks.objects.base import BaseObject
from django_quickbooks.validators import SchemeValidator


class ItemLine(BaseObject):
    fields = dict(
        Item=dict(validator=dict(type=SchemeValidator.OBJTYPE)),
        Desc=dict(validator=dict(type=SchemeValidator.STRTYPE)),
        Quantity=dict(validator=dict(type=SchemeValidator.DECIMALTYPE)),
        Cost=dict(validator=dict(type=SchemeValidator.DECIMALTYPE)),
        Amount=dict(validator=dict(type=SchemeValidator.DECIMALTYPE)),
    )
# class ExpenseLine(BaseObject):
#    fields = dict(
#        Account=dict(validator=dict(type=SchemeValidator.OBJTYPE)),
#        Amount=dict(validator=dict(type=SchemeValidator.DECIMALTYPE)),
#        Memo
#    )


class Bill(BaseObject):
    fields = dict(
        TxnID=dict(validator=dict(type=SchemeValidator.IDTYPE)),
        TimeCreated=dict(validator=dict(type=SchemeValidator.STRTYPE)),
        TimeModified=dict(validator=dict(type=SchemeValidator.STRTYPE)),
        EditSequence=dict(validator=dict(type=SchemeValidator.STRTYPE)),
        Vendor=dict(validator=dict(type=SchemeValidator.OBJTYPE)),
        APAccount=dict(validator=dict(type=SchemeValidator.OBJTYPE)),
        TxnDate=dict(validator=dict(type=SchemeValidator.STRTYPE)),
        DueDate=dict(validator=dict(type=SchemeValidator.STRTYPE)),
        RefNumber=dict(validator=dict(type=SchemeValidator.STRTYPE)),
        Memo=dict(validator=dict(type=SchemeValidator.STRTYPE)),
        ItemLine=dict(many=True, validator=dict(
            type=SchemeValidator.OBJTYPE)),
    )

    @staticmethod
    def get_service():
        from django_quickbooks.services.bill import BillService
        return BillService


class Txn(BaseObject):
    fields = dict(
        TxnID=dict(validator=dict(type=SchemeValidator.IDTYPE)),
        TxnType=dict(validator=dict(type=SchemeValidator.STRTYPE)),
    )

    def as_xml(self, class_name=None, indent=0, opp_type=QUICKBOOKS_ENUMS.OPP_ADD,
               version=QUICKBOOKS_ENUMS.VERSION_13, **kwargs):
        xml = super(Txn, self).as_xml(
            class_name, indent, opp_type, version,  **kwargs)

        return xml\
            .replace(f'<{__class__.__name__}{opp_type}>', '')\
            .replace(f'</{__class__.__name__}{opp_type}>', '')\
            .replace('<TxnType>', f'<Txn{opp_type}Type>')\
            .replace('</TxnType>', f'</Txn{opp_type}Type>')
