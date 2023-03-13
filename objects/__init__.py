from django.utils.module_loading import import_string

from django_quickbooks.exceptions import QBObjectNotImplemented

ALTERNATIVES = {
    'ItemService': ('Item',),
}


def import_object_cls(resource_name):
    for class_name, alternatives in ALTERNATIVES.items():
        if resource_name in alternatives:
            resource_name = class_name

    try:
        return import_string('%s.%s' % (__package__, resource_name))
    except ImportError:
        raise QBObjectNotImplemented


from django_quickbooks.objects.customer import \
    Customer

from django_quickbooks.objects.address import \
    BillAddress, \
    ShipAddress

from django_quickbooks.objects.invoice import \
    InvoiceLine, \
    Invoice

from django_quickbooks.objects.itemservice import \
    ItemService

from django_quickbooks.objects.account import \
    Account

from django_quickbooks.objects.salesorpurchase import \
    SalesOrPurchase