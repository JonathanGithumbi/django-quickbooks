from django_quickbooks import QUICKBOOKS_ENUMS
from django_quickbooks.services.base import Service


class VendorService(Service):
    def add(self, object):
        return self._add(QUICKBOOKS_ENUMS.RESOURCE_VENDOR, object)

    def update(self, object):
        return self._update(QUICKBOOKS_ENUMS.RESOURCE_VENDOR, object)

    def all(self):
        return self._all(QUICKBOOKS_ENUMS.RESOURCE_VENDOR)

    def find_by_id(self, id):
        return self._find_by_id(QUICKBOOKS_ENUMS.RESOURCE_VENDOR, id)

    def find_by_full_name(self, full_name):
        return self._find_by_full_name(QUICKBOOKS_ENUMS.RESOURCE_VENDOR, full_name)
