from django_quickbooks import QUICKBOOKS_ENUMS, qbwc_settings
from django_quickbooks.objects.vendor import Vendor
from django_quickbooks.processors.base import ResponseProcessor, ResponseProcessorMixin


LocalVendor = qbwc_settings.LOCAL_MODEL_CLASSES['Vendor']


class VendorQueryResponseProcessor(ResponseProcessor, ResponseProcessorMixin):
    resource = QUICKBOOKS_ENUMS.RESOURCE_VENDOR
    op_type = QUICKBOOKS_ENUMS.OPP_QR
    local_model_class = LocalVendor
    obj_class = Vendor

    def process(self, realm):
        cont = super().process(realm)
        if not cont:
            return False
        for vendor_ret in list(self._response_body):
            vendor = self.obj_class.from_lxml(vendor_ret)
            local_vendor = None
            if vendor.ListID:
                local_vendor = self.find_by_list_id(vendor.ListID)
            if not local_vendor and vendor.Name:
                local_vendor = self.find_by_name(vendor.Name)

            if local_vendor:
                self.update(local_vendor, vendor)
            else:
                self.create(vendor)
        return True


class VendorAddResponseProcessor(ResponseProcessor, ResponseProcessorMixin):
    resource = QUICKBOOKS_ENUMS.RESOURCE_VENDOR
    op_type = QUICKBOOKS_ENUMS.OPP_ADD
    local_model_class = LocalVendor
    obj_class = Vendor

    def process(self, realm):
        cont = super().process(realm)
        if not cont:
            return False
        for vendor_ret in list(self._response_body):
            vendor = self.obj_class.from_lxml(vendor_ret)
            local_vendor = None
            if vendor.Name:
                local_vendor = self.find_by_name(vendor.Name)

            if local_vendor:
                self.update(local_vendor, vendor)
        return True


class VendorModResponseProcessor(ResponseProcessor, ResponseProcessorMixin):
    resource = QUICKBOOKS_ENUMS.RESOURCE_VENDOR
    op_type = QUICKBOOKS_ENUMS.OPP_MOD
    local_model_class = LocalVendor
    obj_class = Vendor

    def process(self, realm):
        cont = super().process(realm)
        if not cont:
            return False
        for vendor_ret in list(self._response_body):
            vendor = self.obj_class.from_lxml(vendor_ret)
            local_vendor = None
            if vendor.ListID:
                local_vendor = self.find_by_list_id(vendor.ListID)
            elif not local_vendor and vendor.Name:
                local_vendor = self.find_by_name(vendor.Name)

            if local_vendor:
                self.update(local_vendor, vendor)
        return True
