from django_quickbooks import QUICKBOOKS_ENUMS

from django_quickbooks.services.base import Service
from django_quickbooks.objects.invoice import Txn


class TransferService(Service):
    ref_fields = ['TransferToAccount', 'TransferFromAccount']

    def add(self, object):
        return self._add(QUICKBOOKS_ENUMS.RESOURCE_TRANSFER, object)

    def update(self, object):
        return self._update(QUICKBOOKS_ENUMS.RESOURCE_TRANSFER, object)

    def all(self):
        return self._all(QUICKBOOKS_ENUMS.RESOURCE_TRANSFER)

    # def void(self, object):
    #    return self._void(
    #        QUICKBOOKS_ENUMS.RESOURCE_TXN, Txn(
    #            TxnID=object.TxnID, TxnType=QUICKBOOKS_ENUMS.RESOURCE_TRANSFER)
    #    )
#
    # def delete(self, object):
    #    return self._delete(
    #        QUICKBOOKS_ENUMS.RESOURCE_TXN, Txn(
    #            TxnID=object.TxnID, TxnType=QUICKBOOKS_ENUMS.RESOURCE_TRANSFER)
    #    )
#
    # def find_by_id(self, id):
    #    return self._find_by_id(QUICKBOOKS_ENUMS.RESOURCE_TRANSFER, id, field_name='TxnID')
#
