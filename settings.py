from importlib import import_module

from django.conf import settings

DEFAULTS = {
    'UPDATE_PAUSE_SECONDS': 35,
    'MINIMUM_UPDATE_SECONDS': 15,
    'MINIMUM_RUN_EVERY_NSECONDS': 30,
    'MINIMUM_RUN_EVERY_NMINUTES': 15,

    'SESSION_MANAGER_CLASS': 'django_quickbooks.session_manager.SessionManager',

    'REALM_MODEL_CLASS': 'django_quickbooks.models.Realm',
    'REALM_SESSION_MODEL_CLASS': 'django_quickbooks.models.RealmSession',
    'QBD_TASK_MODEL_CLASS': 'django_quickbooks.models.QBDTask',

    'REALM_CONNECTION_DECORATOR': 'django_quickbooks.decorators.base_realm_connection',

    'RESPONSE_PROCESSORS': (
        'django_quickbooks.processors.account.AccountModResponseProcessor',
        'django_quickbooks.processors.account.AccountAddResponseProcessor',
        'django_quickbooks.processors.account.AccountQueryResponseProcessor',
        'django_quickbooks.processors.customer.CustomerQueryResponseProcessor',
        'django_quickbooks.processors.customer.CustomerModResponseProcessor',
        'django_quickbooks.processors.customer.CustomerAddResponseProcessor',
        'django_quickbooks.processors.invoice.InvoiceQueryResponseProcessor',
        'django_quickbooks.processors.invoice.InvoiceAddResponseProcessor',
        'django_quickbooks.processors.invoice.InvoiceModResponseProcessor',
        'django_quickbooks.processors.itemservice.ItemServiceAddResponseProcessor',
        'django_quickbooks.processors.itemservice.ItemServiceModResponseProcessor',
        'django_quickbooks.processors.receivepayment.ReceivePaymentAddResponseProcessor',
        'django_quickbooks.processors.receivepayment.ReceivePaymentModResponseProcessor',
        'django_quickbooks.processors.vendor.VendorAddResponseProcessor',
        'django_quickbooks.processors.vendor.VendorModResponseProcessor',
        'django_quickbooks.processors.bill.BillAddResponseProcessor',
        'django_quickbooks.processors.bill.BillModResponseProcessor',
        'django_quickbooks.processors.itemnoninventory.ItemNonInventoryAddResponseProcessor',
        'django_quickbooks.processors.itemnoninventory.ItemNonInventoryModResponseProcessor',
        'django_quickbooks.processors.billpaymentcheck.BillPaymentCheckAddResponseProcessor',
        'django_quickbooks.processors.billpaymentcheck.BillPaymentCheckModResponseProcessor',
        'django_quickbooks.processors.transfer.TransferAddResponseProcessor',
        'django_quickbooks.processors.transfer.TransferModResponseProcessor',
        'django_quickbooks.processors.creditmemo.CreditMemoAddResponseProcessor',
        'django_quickbooks.processors.creditmemo.CreditMemoModResponseProcessor',
    ),

    'RABBITMQ_DEFAULT_HOST': 'localhost',
    'RABBITMQ_DEFAULT_USER': 'quickbooks',
    'RABBITMQ_DEFAULT_PASS': 'quickbooks',
    'RABBITMQ_DEFAULT_VHOST': 'quickbooks',

    'APP_URL': 'http://localhost:8000/quickbooks-desktop/',
    'APP_SUPPORT': 'http://localhost:8000/quickbooks-desktop/support/',
    'APP_ID': '',
    'APP_NAME': 'Some App',
    'APP_DESCRIPTION': 'Some App Description',
    'QB_TYPE': 'QBFS',
    'OWNER_ID': '{1ee58da6-3051-11ea-b499-9cda3ea7afc1}',

    'LOCAL_MODEL_CLASSES': {
        'Invoice': 'invoice.models.Invoice',
        'Customer': 'student.models.Student',
        'ItemService': 'fees_structure.models.BillingItem',
        'Account': 'account.models.Account',
        'ReceivePayment': 'payment.models.Payment',
        'Vendor': 'vendor.models.Vendor',
        'Bill': 'bill.models.Bill',
        'ItemNonInventory': 'item.models.Item',
        'BillPaymentCheck': 'bill.models.BillPayment',
        'Transfer': 'account.models.Transfer',
        'CreditMemo': 'payment.models.CreditMemo',
        'Grade':'grade.models.Grade'
    }
}

IMPORT_STRINGS = (
    'RESPONSE_PROCESSORS',
    'SESSION_MANAGER_CLASS',
    'REALM_MODEL_CLASS',
    'REALM_SESSION_MODEL_CLASS',
    'QBD_TASK_MODEL_CLASS',
    'REALM_CONNECTION_DECORATOR',
)


def perform_import(val, setting_name):
    """
    If the given setting is a string import notation,
    then perform the necessary import or imports.
    """
    if val is None:
        return None
    elif isinstance(val, str):
        return import_from_string(val, setting_name)
    elif isinstance(val, (list, tuple)):
        return [import_from_string(item, setting_name) for item in val]
    return val


def import_from_string(val, setting_name):
    """
    Attempt to import a class from a string representation.
    """
    try:
        # Nod to tastypie's use of importlib.
        module_path, class_name = val.rsplit('.', 1)
        module = import_module(module_path)
        return getattr(module, class_name)
    except (ImportError, AttributeError) as e:
        msg = "Could not import '%s' for Quickbooks Web Connector setting '%s'. %s: %s." \
              % (val, setting_name, e.__class__.__name__, e)
        raise ImportError(msg)


class QBWCSettings(object):
    """
    A settings object, that allows Quickbooks Web Connector settings to be accessed as properties.
    """

    def __init__(self, user_settings=None, defaults=None, import_strings=None):
        if user_settings:
            self._user_settings = user_settings
        self.defaults = defaults or DEFAULTS
        self.import_strings = import_strings or IMPORT_STRINGS

    @property
    def user_settings(self):
        if not hasattr(self, '_user_settings'):
            self._user_settings = getattr(settings, 'QBWC_SETTINGS', {})
        return self._user_settings

    def __getattr__(self, attr):
        if attr not in self.defaults:
            raise AttributeError(
                "Invalid Quickbooks Web Connector setting: '%s'" % attr)

        try:
            # Check if present in user settings
            val = self.user_settings[attr]
        except KeyError:
            # Fall back to defaults
            val = self.defaults[attr]

        # Coerce import strings into classes
        if attr in self.import_strings:
            val = perform_import(val, attr)

        if attr == 'LOCAL_MODEL_CLASSES':
            for key, value in val.items():
                # So the import_from_string expects a key:value pair
                val[key] = import_from_string(value, value)

        setattr(self, attr, val)
        return val


qbwc_settings = QBWCSettings(None, DEFAULTS, IMPORT_STRINGS)
