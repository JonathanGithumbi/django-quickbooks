from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

from django_quickbooks import QUICKBOOKS_ENUMS, qbwc_settings
from django_quickbooks.objects.billpaymentcheck import BillPaymentCheck
from django_quickbooks.processors.base import ResponseProcessor, ResponseProcessorMixin

LocalBillPaymentCheck = qbwc_settings.LOCAL_MODEL_CLASSES['BillPaymentCheck']


class BillPaymentCheckAddResponseProcessor(ResponseProcessor, ResponseProcessorMixin):
    local_model_class = LocalBillPaymentCheck
    obj_class = BillPaymentCheck

    resource = QUICKBOOKS_ENUMS.RESOURCE_BILLPAYMENTCHECK
    op_type = QUICKBOOKS_ENUMS.OPP_ADD

    def process(self, realm):
        cont = super().process(realm)
        if not cont:
            return False
        for billpaymentcheck_ret in list(self._response_body):
            billpaymentcheck = self.obj_class.from_lxml(billpaymentcheck_ret)
            local_billpaymentcheck = None

            if billpaymentcheck.TxnID:
                local_billpaymentcheck = self.find_by_id(
                    billpaymentcheck.RefNumber)

            if local_billpaymentcheck:
                self.update(local_billpaymentcheck, billpaymentcheck)

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


class BillPaymentCheckModResponseProcessor(ResponseProcessor, ResponseProcessorMixin):
    local_model_class = LocalBillPaymentCheck
    obj_class = BillPaymentCheck

    resource = QUICKBOOKS_ENUMS.RESOURCE_BILLPAYMENTCHECK
    op_type = QUICKBOOKS_ENUMS.OPP_MOD


class BillPaymentCheckQueryResponseProcessor(ResponseProcessor, ResponseProcessorMixin):
    local_model_class = LocalBillPaymentCheck
    obj_class = BillPaymentCheck

    resource = QUICKBOOKS_ENUMS.RESOURCE_BILLPAYMENTCHECK
    op_type = QUICKBOOKS_ENUMS.OPP_QR
