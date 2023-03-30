from django_quickbooks import QUICKBOOKS_ENUMS
from django_quickbooks.objects.bill import Txn
from django_quickbooks.services.base import Service


class BillService(Service):
    ref_fields = ['Vendor', 'APAccount', 'Item']
    add_fields = ['ItemLine']
    mod_fields = ['ItemLine']

    def add(self, object):
        return self._add(QUICKBOOKS_ENUMS.RESOURCE_BILL, object)

    def update(self, object):
        return self._update(QUICKBOOKS_ENUMS.RESOURCE_BILL, object)

    def all(self):
        return self._all(QUICKBOOKS_ENUMS.RESOURCE_BILL)

    def void(self, object):
        return self._void(
            QUICKBOOKS_ENUMS.RESOURCE_TXN, Txn(
                TxnID=object.TxnID, TxnType=QUICKBOOKS_ENUMS.RESOURCE_BILL)
        )

    def delete(self, object):
        return self._delete(
            QUICKBOOKS_ENUMS.RESOURCE_TXN, Txn(
                TxnID=object.TxnID, TxnType=QUICKBOOKS_ENUMS.RESOURCE_BILL)
        )

    def find_by_id(self, id):
        return self._find_by_id(QUICKBOOKS_ENUMS.RESOURCE_BILL, id, field_name='TxnID')
