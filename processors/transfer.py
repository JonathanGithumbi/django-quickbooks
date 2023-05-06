from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

from django_quickbooks import QUICKBOOKS_ENUMS, qbwc_settings
from django_quickbooks.objects.transfer import Transfer
from django_quickbooks.processors.base import ResponseProcessor, ResponseProcessorMixin

LocalTransfer = qbwc_settings.LOCAL_MODEL_CLASSES['Transfer']


class TransferAddResponseProcessor(ResponseProcessor, ResponseProcessorMixin):
    local_model_class = LocalTransfer
    obj_class = Transfer

    resource = QUICKBOOKS_ENUMS.RESOURCE_TRANSFER
    op_type = QUICKBOOKS_ENUMS.OPP_ADD

    def process(self, realm):
        cont = super().process(realm)
        if not cont:
            return False
        for transfer_ret in list(self._response_body):
            transfer = self.obj_class.from_lxml(transfer_ret)
            local_transfer = None

            if transfer.TxnID:
                local_transfer = self.find_by_id(
                    transfer.Memo)

            if local_transfer:
                self.update(local_transfer, transfer)

        return True

    def find_by_id(self, id):
        try:
            return self.local_model_class.objects.get(id=id)
        except ObjectDoesNotExist:
            return None

    def update(self, local_obj, obj):
        local_obj.qbd_object_id = obj.TxnID
        local_obj.qbd_object_updated_at = timezone.now() + timezone.timedelta(minutes=1)
        local_obj.qbd_object_version = obj.EditSequence
        local_obj.save()


class TransferModResponseProcessor(ResponseProcessor, ResponseProcessorMixin):
    local_model_class = LocalTransfer
    obj_class = Transfer

    resource = QUICKBOOKS_ENUMS.RESOURCE_TRANSFER
    op_type = QUICKBOOKS_ENUMS.OPP_MOD

    def process(self, realm):
        cont = super().process(realm)
        if not cont:
            return False
        for transfer_ret in list(self._response_body):
            transfer = self.obj_class.from_lxml(transfer_ret)
            local_transfer = None

            if transfer.TxnID:
                local_transfer = self.find_by_id(
                    transfer.Memo)

            if local_transfer:
                self.update(local_transfer, transfer)

        return True

    def find_by_id(self, id):
        try:
            return self.local_model_class.objects.get(id=id)
        except ObjectDoesNotExist:
            return None

    def update(self, local_obj, obj):
        local_obj.qbd_object_id = obj.TxnID
        local_obj.qbd_object_updated_at = timezone.now() + timezone.timedelta(minutes=1)
        local_obj.qbd_object_version = obj.EditSequence
        local_obj.save()


class TransferQueryResponseProcessor(ResponseProcessor, ResponseProcessorMixin):
    local_model_class = LocalTransfer
    obj_class = Transfer

    resource = QUICKBOOKS_ENUMS.RESOURCE_TRANSFER
    op_type = QUICKBOOKS_ENUMS.OPP_QR
