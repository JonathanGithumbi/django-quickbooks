from django_quickbooks import QUICKBOOKS_ENUMS
from django_quickbooks.objects.base import BaseObject
from django_quickbooks.validators import SchemeValidator


class ItemService(BaseObject):
    fields = dict(
        ListID=dict(validator=dict(type=SchemeValidator.IDTYPE)),
        EditSequence=dict(validator=dict(type=SchemeValidator.STRTYPE)),
        Name=dict(validator=dict(type=SchemeValidator.STRTYPE)),
        FullName=dict(validator=dict(type=SchemeValidator.STRTYPE)),
        SalesOrPurchase=dict(validator=dict(type=SchemeValidator.OBJTYPE)),
    )

    @staticmethod
    def get_service():
        from django_quickbooks.services.itemservice import ItemServiceService
        return ItemServiceService



