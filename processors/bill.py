from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

from django_quickbooks import QUICKBOOKS_ENUMS, qbwc_settings
from django_quickbooks.objects.bill import Bill
from django_quickbooks.processors.base import ResponseProcessor, ResponseProcessorMixin

LocalBill = qbwc_settings.LOCAL_MODEL_CLASSES['Bill']


class BillAddResponseProcessor(ResponseProcessor, ResponseProcessorMixin):
    local_model_class = LocalBill
    obj_class = Bill

    resource = QUICKBOOKS_ENUMS.RESOURCE_BILL
    op_type = QUICKBOOKS_ENUMS.OPP_ADD

    def process(self, realm):
        cont = super().process(realm)
        if not cont:
            return False
        for bill_ret in list(self._response_body):
            bill = self.obj_class.from_lxml(bill_ret)
            local_bill = None

            if bill.TxnID:
                local_bill = self.find_by_id(bill.RefNumber)

            if local_bill:
                self.update(local_bill, bill)

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


class BillModResponseProcessor(ResponseProcessor, ResponseProcessorMixin):
    local_model_class = LocalBill
    obj_class = Bill

    resource = QUICKBOOKS_ENUMS.RESOURCE_BILL
    op_type = QUICKBOOKS_ENUMS.OPP_MOD


class BillQueryResponseProcessor(ResponseProcessor, ResponseProcessorMixin):
    local_model_class = LocalBill
    obj_class = Bill

    resource = QUICKBOOKS_ENUMS.RESOURCE_BILL
    op_type = QUICKBOOKS_ENUMS.OPP_QR
