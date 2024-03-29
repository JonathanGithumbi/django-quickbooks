from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

from django_quickbooks import QUICKBOOKS_ENUMS, qbwc_settings
from django_quickbooks.objects.invoice import Invoice
from django_quickbooks.processors.base import ResponseProcessor, ResponseProcessorMixin

LocalInvoice = qbwc_settings.LOCAL_MODEL_CLASSES['Invoice']


class InvoiceAddResponseProcessor(ResponseProcessor, ResponseProcessorMixin):
    local_model_class = LocalInvoice
    obj_class = Invoice

    resource = QUICKBOOKS_ENUMS.RESOURCE_INVOICE
    op_type = QUICKBOOKS_ENUMS.OPP_ADD

    def process(self, realm):
        cont = super().process(realm)
        if not cont:
            return False
        for invoice_ret in list(self._response_body):
            invoice = self.obj_class.from_lxml(invoice_ret)
            local_invoice = None
            if invoice.TxnID:
                local_invoice = self.find_by_id(invoice.RefNumber)

            if local_invoice:
                self.update(local_invoice, invoice)

                # i need to update my local invoice lines with the txnlineid from the  invoice's InvoiceLine
                for line_item in invoice.InvoiceLine:
                    # fetch the local invoice's item line based on the line's description
                    local_inv_line = local_invoice.items.get(
                        item__name=line_item.Desc)
                    local_inv_line.txnlineid = line_item.TxnLineID
                    local_inv_line.save()

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


class InvoiceModResponseProcessor(ResponseProcessor, ResponseProcessorMixin):
    local_model_class = LocalInvoice
    obj_class = Invoice

    resource = QUICKBOOKS_ENUMS.RESOURCE_INVOICE
    op_type = QUICKBOOKS_ENUMS.OPP_MOD

    def process(self, realm):
        cont = super().process(realm)
        if not cont:
            return False
        for invoice_ret in list(self._response_body):
            invoice = self.obj_class.from_lxml(invoice_ret)
            local_invoice = None
            if invoice.TxnID:
                local_invoice = self.find_by_id(invoice.RefNumber)

            if local_invoice:
                self.update(local_invoice, invoice)

                # i need to update my local invoice lines with the txnlineid from the  invoice's InvoiceLine
                for line_item in invoice.InvoiceLine:
                    # fetch the local invoice's item line based on the line's description
                    local_inv_line = local_invoice.items.get(
                        item__name=line_item.Desc)
                    local_inv_line.txnlineid = line_item.TxnLineID
                    local_inv_line.save()

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


class InvoiceQueryResponseProcessor(ResponseProcessor, ResponseProcessorMixin):
    local_model_class = LocalInvoice
    obj_class = Invoice

    resource = QUICKBOOKS_ENUMS.RESOURCE_INVOICE
    op_type = QUICKBOOKS_ENUMS.OPP_QR
