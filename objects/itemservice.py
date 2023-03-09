from django_quickbooks import QUICKBOOKS_ENUMS
from django_quickbooks.objects.base import BaseObject
from django_quickbooks.validators import SchemeValidator


class ItemService(BaseObject):
    fields = dict(
        ListID=dict(validator=dict(type=SchemeValidator.IDTYPE)),
        Name=dict(validator=dict(type=SchemeValidator.STRTYPE)),
        FullName=dict(validator=dict(type=SchemeValidator.STRTYPE)),
        SalesOrPurchase=dict(validator=dict(type=SchemeValidator.OBJTYPE)),
    )

    @staticmethod
    def get_service():
        from django_quickbooks.services.itemservice import ServiceOfItemService
        return ServiceOfItemService


#class SalesOrPurchase(BaseObject):
#    fields = dict(
#        Desc=dict(validator=dict(SchemeValidator.STRTYPE)),
#        Price=dict(validator=dict(SchemeValidator.FLOATTYPE)),
#        AccountRef=dict(validator=dict(SchemeValidator.OBJTYPE)),
#    )
