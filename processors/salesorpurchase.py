from django_quickbooks import QUICKBOOKS_ENUMS, qbwc_settings
from django_quickbooks.objects.salesorpurchase import SalesOrPurchase
from django_quickbooks.processors.base import ResponseProcessor, ResponseProcessorMixin


LocalSalesOrPurchase = qbwc_settings.LOCAL_MODEL_CLASSES['SalesOrPurchase']


class SalesOrPurchaseQueryResponseProcessor(ResponseProcessor, ResponseProcessorMixin):
    resource = QUICKBOOKS_ENUMS.RESOURCE_SALESORPURCHASE
    op_type = QUICKBOOKS_ENUMS.OPP_QR
    local_model_class = LocalSalesOrPurchase
    obj_class = SalesOrPurchase

    def process(self, realm):
        cont = super().process(realm)
        if not cont:
            return False
        for salesorpurchase_ret in list(self._response_body):
            salesorpurchase = self.obj_class.from_lxml(salesorpurchase_ret)
            local_salesorpurchase = None
            if salesorpurchase.ListID:
                local_salesorpurchase = self.find_by_list_id(salesorpurchase.ListID)
            if not local_salesorpurchase and salesorpurchase.Name:
                local_salesorpurchase = self.find_by_name(salesorpurchase.Name)

            if local_salesorpurchase:
                self.update(local_salesorpurchase, salesorpurchase)
            else:
                self.create(salesorpurchase)
        return True


class SalesOrPurchaseAddResponseProcessor(ResponseProcessor, ResponseProcessorMixin):
    resource = QUICKBOOKS_ENUMS.RESOURCE_SALESORPURCHASE
    op_type = QUICKBOOKS_ENUMS.OPP_ADD
    local_model_class = LocalSalesOrPurchase
    obj_class = SalesOrPurchase

    def process(self, realm):
        cont = super().process(realm)
        if not cont:
            return False
        for salesorpurchase_ret in list(self._response_body):
            salesorpurchase = self.obj_class.from_lxml(salesorpurchase_ret)
            local_salesorpurchase = None
            if salesorpurchase.Name:
                local_salesorpurchase = self.find_by_name(salesorpurchase.Name)

            if local_salesorpurchase:
                self.update(local_salesorpurchase, salesorpurchase)
        return True


class SalesOrPurchaseModResponseProcessor(ResponseProcessor, ResponseProcessorMixin):
    resource = QUICKBOOKS_ENUMS.RESOURCE_SALESORPURCHASE
    op_type = QUICKBOOKS_ENUMS.OPP_MOD
    local_model_class = LocalSalesOrPurchase
    obj_class = SalesOrPurchase

    def process(self, realm):
        cont = super().process(realm)
        if not cont:
            return False
        for salesorpurchase_ret in list(self._response_body):
            salesorpurchase = self.obj_class.from_lxml(salesorpurchase_ret)
            local_salesorpurchase = None
            if salesorpurchase.ListID:
                local_salesorpurchase = self.find_by_list_id(salesorpurchase.ListID)
            elif not local_salesorpurchase and salesorpurchase.Name:
                local_salesorpurchase = self.find_by_name(salesorpurchase.Name)

            if local_salesorpurchase:
                self.update(local_salesorpurchase, salesorpurchase)
        return True
