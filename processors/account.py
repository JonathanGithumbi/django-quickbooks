from django_quickbooks import QUICKBOOKS_ENUMS, qbwc_settings
from django_quickbooks.objects.account import Account
from django_quickbooks.processors.base import ResponseProcessor, ResponseProcessorMixin


LocalAccount = qbwc_settings.LOCAL_MODEL_CLASSES['Account']


class AccountQueryResponseProcessor(ResponseProcessor, ResponseProcessorMixin):
    resource = QUICKBOOKS_ENUMS.RESOURCE_ACCOUNT
    op_type = QUICKBOOKS_ENUMS.OPP_QR
    local_model_class = LocalAccount
    obj_class = Account

    def process(self, realm):
        cont = super().process(realm)
        if not cont:
            return False
        for account_ret in list(self._response_body):
            account = self.obj_class.from_lxml(account_ret)
            local_account = None
            if account.ListID:
                local_account = self.find_by_list_id(account.ListID)
            if not local_account and account.Name:
                local_account = self.find_by_name(account.Name)

            if local_account:
                self.update(local_account, account)
            else:
                self.create(account)
        return True


class AccountAddResponseProcessor(ResponseProcessor, ResponseProcessorMixin):
    resource = QUICKBOOKS_ENUMS.RESOURCE_ACCOUNT
    op_type = QUICKBOOKS_ENUMS.OPP_ADD
    local_model_class = LocalAccount
    obj_class = Account

    def process(self, realm):
        cont = super().process(realm)
        if not cont:
            return False
        for account_ret in list(self._response_body):
            account = self.obj_class.from_lxml(account_ret)
            local_account = None
            if account.Name:
                local_account = self.find_by_name(account.Name)

            if local_account:
                self.update(local_account, account)
        return True


class AccountModResponseProcessor(ResponseProcessor, ResponseProcessorMixin):
    resource = QUICKBOOKS_ENUMS.RESOURCE_ACCOUNT
    op_type = QUICKBOOKS_ENUMS.OPP_MOD
    local_model_class = LocalAccount
    obj_class = Account

    def process(self, realm):
        cont = super().process(realm)
        if not cont:
            return False
        for account_ret in list(self._response_body):
            account = self.obj_class.from_lxml(account_ret)
            local_account = None
            if account.ListID:
                local_account = self.find_by_list_id(account.ListID)
            elif not local_account and account.Name:
                local_account = self.find_by_name(account.Name)

            if local_account:
                self.update(local_account, account)
        return True
