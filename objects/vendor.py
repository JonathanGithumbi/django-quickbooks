from django_quickbooks.objects.base import BaseObject
from django_quickbooks.validators import SchemeValidator


class Vendor(BaseObject):
    fields = dict(
        ListID=dict(validator=dict(type=SchemeValidator.IDTYPE)),
        TimeCreated=dict(validator=dict(type=SchemeValidator.STRTYPE)),
        TimeModified=dict(validator=dict(type=SchemeValidator.STRTYPE)),
        EditSequence=dict(validator=dict(type=SchemeValidator.ESTYPE)),
        Name=dict(required=False, validator=dict(
            type=SchemeValidator.STRTYPE)),
        IsActive=dict(validator=dict(type=SchemeValidator.BOOLTYPE)),
    )

    def __init__(self, Name=None, IsActive=None, **kwargs):
        if Name:
            self.Name = Name

        if IsActive:
            self.IsActive = IsActive

        super().__init__(**kwargs)

    @staticmethod
    def get_service():
        from django_quickbooks.services.vendor import VendorService
        return VendorService
