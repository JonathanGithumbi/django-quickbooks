from django_quickbooks import QUICKBOOKS_ENUMS

from django_quickbooks.services.base import Service


class CreditMemoService(Service):
    ref_fields = ['Item', 'Customer', 'ARAccount', ]
    add_fields = ['CreditMemoLine']
    mod_fields = ['CreditMemoLine']

    def add(self, object):
        return self._add(QUICKBOOKS_ENUMS.RESOURCE_CREDITMEMO, object)

    def update(self, object):
        return self._update(QUICKBOOKS_ENUMS.RESOURCE_CREDITMEMO, object)

    def all(self):
        return self._all(QUICKBOOKS_ENUMS.RESOURCE_CREDITMEMO)

    def find_by_id(self, id):
        return self._find_by_id(QUICKBOOKS_ENUMS.RESOURCE_CREDITMEMO, id, field_name='TxnID')
