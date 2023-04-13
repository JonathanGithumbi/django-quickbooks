from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

from django_quickbooks import QUICKBOOKS_ENUMS, qbwc_settings
from django_quickbooks.objects.creditmemo import CreditMemo
from django_quickbooks.processors.base import ResponseProcessor, ResponseProcessorMixin

LocalCreditMemo = qbwc_settings.LOCAL_MODEL_CLASSES['CreditMemo']


class CreditMemoAddResponseProcessor(ResponseProcessor, ResponseProcessorMixin):
    local_model_class = LocalCreditMemo
    obj_class = CreditMemo

    resource = QUICKBOOKS_ENUMS.RESOURCE_CREDITMEMO
    op_type = QUICKBOOKS_ENUMS.OPP_ADD

    def process(self, realm):
        cont = super().process(realm)
        if not cont:
            return False
        for creditmemo_ret in list(self._response_body):
            creditmemo = self.obj_class.from_lxml(creditmemo_ret)
            local_creditmemo = None

            if creditmemo.TxnID:
                local_creditmemo = self.find_by_id(creditmemo.RefNumber)

            if local_creditmemo:
                self.update(local_creditmemo, creditmemo)

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


class CreditMemoModResponseProcessor(ResponseProcessor, ResponseProcessorMixin):
    local_model_class = LocalCreditMemo
    obj_class = CreditMemo

    resource = QUICKBOOKS_ENUMS.RESOURCE_CREDITMEMO
    op_type = QUICKBOOKS_ENUMS.OPP_MOD


class CreditMemoQueryResponseProcessor(ResponseProcessor, ResponseProcessorMixin):
    local_model_class = LocalCreditMemo
    obj_class = CreditMemo

    resource = QUICKBOOKS_ENUMS.RESOURCE_CREDITMEMO
    op_type = QUICKBOOKS_ENUMS.OPP_QR
