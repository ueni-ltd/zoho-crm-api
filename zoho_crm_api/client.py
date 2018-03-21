from zoho_crm_api.module import RecordModule
from zoho_crm_api.leads import LeadsModule
from zoho_crm_api.related_module import RelatedModule
from zoho_crm_api.session import ZohoSession
from zoho_crm_api.users import UsersModule


class ZohoCRMClient:

    def __init__(self, refresh_token, client_id, client_secret, domain='eu', api_version='v2'):
        self._session = ZohoSession(refresh_token, client_id, client_secret, domain, api_version)

        self.accounts = RecordModule(session=self._session, module_name='Accounts')
        self.accounts.notes = RelatedModule(self._session, module_name='Accounts', related_module_name='Notes')
        self.accounts.activities = RelatedModule(
            self._session, module_name='Accounts', related_module_name='Activities'
        )

        self.campaigns = RecordModule(session=self._session, module_name='Campaigns')
        self.campaigns.leads = RelatedModule(self._session, module_name='Campaigns', related_module_name='Leads')

        self.contacts = RecordModule(session=self._session, module_name='Contacts')
        self.deals = RecordModule(session=self._session, module_name='Deals')
        self.leads = LeadsModule(session=self._session, module_name='Leads')

        self.users = UsersModule(session=self._session)
