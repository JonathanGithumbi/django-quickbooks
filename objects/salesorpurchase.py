from django_quickbooks import QUICKBOOKS_ENUMS
from django_quickbooks.objects.base import BaseObject
from django_quickbooks.validators import SchemeValidator


class SalesOrPurchase(BaseObject):
    fields = dict(
        Desc=dict(validator=dict(type=SchemeValidator.STRTYPE)),
        Price=dict(validator=dict(type=SchemeValidator.DECIMALTYPE)),
        Account=dict(validator=dict(type=SchemeValidator.OBJTYPE)),
    )
