from django_quickbooks import QUICKBOOKS_ENUMS
from django_quickbooks.services.base import Service


class SalesOrPurchaseService(Service):
    ref_fields = ['AccountRef']

    def add(self, object):
        return self._add(QUICKBOOKS_ENUMS.RESOURCE_SALESORPURCHASE, object)

    def update(self, object):
        return self._update(QUICKBOOKS_ENUMS.RESOURCE_SALESORPURCHASE, object)

    def all(self):
        return self._all(QUICKBOOKS_ENUMS.RESOURCE_SALESORPURCHASE)

    def find_by_id(self, id):
        return self._find_by_id(QUICKBOOKS_ENUMS.RESOURCE_SALESORPURCHASE, id)

    def find_by_full_name(self, full_name):
        return self._find_by_full_name(QUICKBOOKS_ENUMS.RESOURCE_SALESORPURCHASE, full_name)
