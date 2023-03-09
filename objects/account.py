from django_quickbooks import QUICKBOOKS_ENUMS
from django_quickbooks.objects.base import BaseObject
from django_quickbooks.validators import SchemeValidator


class Account(BaseObject):
    fields = dict(
        ListID=dict(validator=dict(type=SchemeValidator.IDTYPE)),
        TimeCreated=dict(validator=dict(type=SchemeValidator.STRTYPE)),
        TimeModified=dict(validator=dict(type=SchemeValidator.STRTYPE)),
        EditSequence=dict(validator=dict(type=SchemeValidator.ESTYPE)),
        FullName=dict(required=True, validator=dict(
            type=SchemeValidator.STRTYPE)),
        Sublevel=dict(validator=dict(type=SchemeValidator.STRTYPE)),
        Name=dict(validator=dict(type=SchemeValidator.STRTYPE)),
        AccountType=dict(validator=dict(type=SchemeValidator.STRTYPE)),
        IsActive=dict(validator=dict(type=SchemeValidator.BOOLTYPE)),
    )

    @staticmethod
    def get_service():
        from django_quickbooks.services.account import AccountService
        return AccountService
