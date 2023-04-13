from django_quickbooks import QUICKBOOKS_ENUMS, qbwc_settings
from django_quickbooks.objects.customer import Customer
from django_quickbooks.processors.base import ResponseProcessor, ResponseProcessorMixin
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

LocalCustomer = qbwc_settings.LOCAL_MODEL_CLASSES['Customer']
LocalGrade = qbwc_settings.LOCAL_MODEL_CLASSES['Grade']


class CustomerQueryResponseProcessor(ResponseProcessor, ResponseProcessorMixin):
    resource = QUICKBOOKS_ENUMS.RESOURCE_CUSTOMER
    op_type = QUICKBOOKS_ENUMS.OPP_QR
    local_model_class = LocalCustomer
    obj_class = Customer

    def process(self, realm):
        cont = super().process(realm)
        if not cont:
            return False
        for customer_ret in list(self._response_body):
            customer = self.obj_class.from_lxml(customer_ret)
            local_customer = None
            if customer.ListID:
                local_customer = self.find_by_list_id(customer.ListID)
            if not local_customer and customer.Name:
                local_customer = self.find_by_name(customer.Name)

            if local_customer:
                self.update(local_customer, customer)
            else:
                self.create(customer)
        return True


class CustomerAddResponseProcessor(ResponseProcessor, ResponseProcessorMixin):
    resource = QUICKBOOKS_ENUMS.RESOURCE_CUSTOMER
    op_type = QUICKBOOKS_ENUMS.OPP_ADD
    local_model_class = LocalCustomer
    obj_class = Customer

    def process(self, realm):
        cont = super().process(realm)
        if not cont:
            return False
        for customer_ret in list(self._response_body):
            customer = self.obj_class.from_lxml(customer_ret)
            local_customer = None
            if customer.Name:
                local_customer = self.find_by_name(customer.Name)

            if local_customer:
                self.update(local_customer, customer)
        return True

    def find_by_name(self, name):
        try:
            # Checks in the Students table
            return self.local_model_class.objects.get(name=name)
        except ObjectDoesNotExist:
            try:
                local_model_class = LocalGrade  # Checks in the Grades  table
                return local_model_class.objects.get(name=name)
            except ObjectDoesNotExist:
                    return None
            

    def update(self, local_obj, obj):
        local_obj.qbd_object_id = obj.ListID
        local_obj.qbd_object_updated_at = timezone.now() + timezone.timedelta(minutes=1)
        local_obj.qbd_object_version = obj.EditSequence
        local_obj.save()


class CustomerModResponseProcessor(ResponseProcessor, ResponseProcessorMixin):
    resource = QUICKBOOKS_ENUMS.RESOURCE_CUSTOMER
    op_type = QUICKBOOKS_ENUMS.OPP_MOD
    local_model_class = LocalCustomer
    obj_class = Customer

    def process(self, realm):
        cont = super().process(realm)
        if not cont:
            return False
        for customer_ret in list(self._response_body):
            customer = self.obj_class.from_lxml(customer_ret)
            local_customer = None
            if customer.ListID:
                local_customer = self.find_by_list_id(customer.ListID)
            elif not local_customer and customer.Name:
                local_customer = self.find_by_name(customer.Name)

            if local_customer:
                self.update(local_customer, customer)
        return True
