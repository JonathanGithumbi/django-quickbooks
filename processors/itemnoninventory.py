from django_quickbooks import QUICKBOOKS_ENUMS, qbwc_settings
from django_quickbooks.objects.itemnoninventory import ItemNonInventory
from django_quickbooks.processors.base import ResponseProcessor, ResponseProcessorMixin

LocalItemNonInventory = qbwc_settings.LOCAL_MODEL_CLASSES['ItemNonInventory']


class ItemNonInventoryQueryResponseProcessor(ResponseProcessor):
    resource = QUICKBOOKS_ENUMS.RESOURCE_ITEMNONINVENTORY
    op_type = QUICKBOOKS_ENUMS.OPP_QR
    local_model_class = LocalItemNonInventory
    obj_class = ItemNonInventory

    def process(self, realm):
        cont = super().process(realm)
        if not cont:
            return False

        return True


class ItemNonInventoryAddResponseProcessor(ResponseProcessor, ResponseProcessorMixin):
    resource = QUICKBOOKS_ENUMS.RESOURCE_ITEMNONINVENTORY
    op_type = QUICKBOOKS_ENUMS.OPP_ADD
    local_model_class = LocalItemNonInventory
    obj_class = ItemNonInventory

    def process(self, realm):
        cont = super().process(realm)
        if not cont:
            return False
        for itemnoninventory_ret in list(self._response_body):
            itemnoninventory = self.obj_class.from_lxml(itemnoninventory_ret)
            local_itemnoninventory = None
            if itemnoninventory.Name:
                local_itemnoninventory = self.find_by_name(itemnoninventory.Name)
            if local_itemnoninventory:
                self.update(local_itemnoninventory, itemnoninventory)
        return True


class ItemNonInventoryModResponseProcessor(ResponseProcessor, ResponseProcessorMixin):
    resource = QUICKBOOKS_ENUMS.RESOURCE_ITEMNONINVENTORY
    op_type = QUICKBOOKS_ENUMS.OPP_MOD
    local_model_class = LocalItemNonInventory
    obj_class = ItemNonInventory

    def process(self, realm):
        cont = super().process(realm)
        if not cont:
            return False
        for itemnoninventory_ret in list(self._response_body):
            itemnoninventory = self.obj_class.from_lxml(itemnoninventory_ret)
            local_itemnoninventory = None
            if itemnoninventory.ListID:
                local_itemnoninventory = self.find_by_list_id(itemnoninventory.ListID)
            elif not local_itemnoninventory and itemnoninventory.Name:
                local_itemnoninventory = self.find_by_name(itemnoninventory.Name)

            if local_itemnoninventory:
                self.update(local_itemnoninventory, itemnoninventory)
        return True
