#from django_quickbooks.signals.qbd_task import *
#from django_quickbooks.signals.invoice import *
#from django_quickbooks.signals.customer import *
from django.dispatch import Signal

qbd_task_create = Signal(providing_args=[
    "qb_operation",
    "qb_resource",
    "object_id",
    "content_type",
    "realm_id",
    "instance",
])

account_updated = Signal(providing_args=["qbd_model_mixin_obj", "realm_id"])
account_created = Signal(providing_args=["qbd_model_mixin_obj", "realm_id"])
customer_created = Signal(providing_args=["qbd_model_mixin_obj", "realm_id"])
customer_updated = Signal(providing_args=["qbd_model_mixin_obj", "realm_id"])
invoice_created = Signal(providing_args=["qbd_model_mixin_obj", "realm_id"])
invoice_updated = Signal(providing_args=["qbd_model_mixin_obj", "realm_id"])
itemservice_created = Signal(
    providing_args=["qbd_model_mixin_obj", "realm_id"])
itemservice_updated = Signal(
    providing_args=["qbd_model_mixin_obj", "realm_id"])
salesorpurchase_created = Signal(
    providing_args=["qbd_model_mixin_obj", "realm_id"])
salesorpurchase_updated = Signal(
    providing_args=["qbd_model_mixin_obj", "realm_id"])
receivepayment_created = Signal(
    providing_args=["qbd_model_mixin_obj", "realm_id"])
receivepayment_updated = Signal(
    providing_args=["qbd_model_mixin_obj", "realm_id"])
vendor_created = Signal(providing_args=["qbd_model_mixin_obj", "realm_id"])
vendor_updated = Signal(providing_args=["qbd_model_mixin_obj", "realm_id"])
bill_created = Signal(providing_args=["qbd_model_mixin_obj", "realm_id"])
bill_updated = Signal(providing_args=["qbd_model_mixin_obj", "realm_id"])
itemnoninventory_created = Signal(
    providing_args=["qbd_model_mixin_obj", "realm_id"])
itemnoninventory_updated = Signal(
    providing_args=["qbd_model_mixin_obj", "realm_id"])
billpaymentcheck_created = Signal(
    providing_args=["qbd_model_mixin_obj", "realm_id"])
billpaymentcheck_updated = Signal(
    providing_args=["qbd_model_mixin_obj", "realm_id"])
transfer_created = Signal(providing_args=["qbd_model_mixin_obj", "realm_id"])
transfer_updated = Signal(providing_args=["qbd_model_mixin_obj", "realm_id"])
creditmemo_created = Signal(providing_args=["qbd_model_mixin_obj", "realm_id"])
creditmemo_updated = Signal(providing_args=["qbd_model_mixin_obj", "realm_id"])
realm_authenticated = Signal(providing_args=["realm"])
qbd_first_time_connected = Signal(providing_args=["realm_id"])
