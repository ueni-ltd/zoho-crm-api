from zoho_crm_api.module import ModuleBase
from zoho_crm_api.session import ZohoSession


class RelatedModule(ModuleBase):

    def __init__(self, session: ZohoSession, module_name, related_module_name: str):
        super().__init__(session, module_name)
        self.related_module_name = related_module_name

    def all(self, record_id, start_page=1, per_page=200):
        url = f'{self.module_name}/{record_id}/{self.related_module_name}'

        yield from self._get_all(url=url, start_page=start_page, per_page=per_page)

    def update(self, record_id, related_record_id, data):
        assert isinstance(data, dict), 'Only one related record can be updated at once'

        url = f'{self.module_name}/{record_id}/{self.related_module_name}/{related_record_id}'
        return self.session.put(url, json={'data': [data]})['data'][0]
