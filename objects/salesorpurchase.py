from django_quickbooks.objects.base import BaseObject
from django_quickbooks.validators import SchemeValidator


class SalesOrPurchase(BaseObject):
    fields = dict(
        Desc=dict(validator=dict(type=SchemeValidator.STRTYPE)),
        Price=dict(validator=dict(type=SchemeValidator.FLOATTYPE)),
        AccountRef=dict(validator=dict(type=SchemeValidator.OBJTYPE)),
    )

    @staticmethod
    def get_service():
        from django_quickbooks.services.salesorpurchase import SalesOrPurchaseService
        return SalesOrPurchaseService
