from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

from django_quickbooks import QUICKBOOKS_ENUMS, qbwc_settings
from django_quickbooks.objects.receivepayment import ReceivePayment
from django_quickbooks.processors.base import ResponseProcessor, ResponseProcessorMixin

LocalReceivePayment = qbwc_settings.LOCAL_MODEL_CLASSES['ReceivePayment']


class ReceivePaymentAddResponseProcessor(ResponseProcessor, ResponseProcessorMixin):
    local_model_class = LocalReceivePayment
    obj_class = ReceivePayment

    resource = QUICKBOOKS_ENUMS.RESOURCE_RECEIVEPAYMENT
    op_type = QUICKBOOKS_ENUMS.OPP_ADD

    def process(self, realm):
        cont = super().process(realm)
        if not cont:
            return False
        for receivepayment_ret in list(self._response_body):
            receivepayment = self.obj_class.from_lxml(receivepayment_ret)
            local_receivepayment = None

            if receivepayment.TxnID:
                local_receivepayment = self.find_by_id(
                    receivepayment.RefNumber)

            if local_receivepayment:
                self.update(local_receivepayment, receivepayment)

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


class ReceivePaymentModResponseProcessor(ResponseProcessor, ResponseProcessorMixin):
    local_model_class = LocalReceivePayment
    obj_class = ReceivePayment

    resource = QUICKBOOKS_ENUMS.RESOURCE_RECEIVEPAYMENT
    op_type = QUICKBOOKS_ENUMS.OPP_MOD


class ReceivePaymentQueryResponseProcessor(ResponseProcessor, ResponseProcessorMixin):
    local_model_class = LocalReceivePayment
    obj_class = ReceivePayment

    resource = QUICKBOOKS_ENUMS.RESOURCE_RECEIVEPAYMENT
    op_type = QUICKBOOKS_ENUMS.OPP_QR
