from django_quickbooks import QUICKBOOKS_ENUMS, qbwc_settings
from django_quickbooks.objects.itemservice import ItemService
from django_quickbooks.processors.base import ResponseProcessor, ResponseProcessorMixin
from django.utils import timezone

LocalItemService = qbwc_settings.LOCAL_MODEL_CLASSES['ItemService']


class ItemServiceQueryResponseProcessor(ResponseProcessor):
    resource = QUICKBOOKS_ENUMS.RESOURCE_ITEMSERVICE
    op_type = QUICKBOOKS_ENUMS.OPP_QR
    local_model_class = LocalItemService
    obj_class = ItemService

    def process(self, realm):
        cont = super().process(realm)
        if not cont:
            return False

        return True


class ItemServiceAddResponseProcessor(ResponseProcessor, ResponseProcessorMixin):
    resource = QUICKBOOKS_ENUMS.RESOURCE_ITEMSERVICE
    op_type = QUICKBOOKS_ENUMS.OPP_ADD
    local_model_class = LocalItemService
    obj_class = ItemService


    def process(self, realm):
        cont = super().process(realm)
        if not cont:
            return False
        for itemservice_ret in list(self._response_body):
            itemservice = self.obj_class.from_lxml(itemservice_ret)
            local_itemservice = None
            if itemservice.Name:
                local_itemservice = self.find_by_name(itemservice.Name)
            if local_itemservice:
                self.update(local_itemservice, itemservice)
        return True
    
    


class ItemServiceModResponseProcessor(ResponseProcessor, ResponseProcessorMixin):
    resource = QUICKBOOKS_ENUMS.RESOURCE_ITEMSERVICE
    op_type = QUICKBOOKS_ENUMS.OPP_MOD
    local_model_class = LocalItemService
    obj_class = ItemService

    def process(self, realm):
        cont = super().process(realm)
        if not cont:
            return False
        for itemservice_ret in list(self._response_body):
            itemservice = self.obj_class.from_lxml(itemservice_ret)
            local_itemservice = None
            if itemservice.ListID:
                local_itemservice = self.find_by_list_id(itemservice.ListID)
            elif not local_itemservice and itemservice.Name:
                local_itemservice = self.find_by_name(itemservice.Name)

            if local_itemservice:
                self.update(local_itemservice, itemservice)
        return True
