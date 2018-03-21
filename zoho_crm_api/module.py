from zoho_crm_api.session import ZohoSession


class ModuleBase(object):

    def __init__(self, session: ZohoSession, module_name: str):
        self.session = session
        self.module_name = module_name
        self.results_name = 'data'

    def _get_all(self, url, start_page=1, per_page=200, params=None):
        if not isinstance(start_page, int) or per_page < 1 or per_page > 200:
            raise TypeError('limit must be an integer >= 1 and smaller than 200')

        if not isinstance(start_page, int) or start_page < 1:
            raise ValueError('from_index must be an integer >= 1')

        params = params or {}
        params['page'] = start_page
        params['per_page'] = per_page

        more_pages = True
        while more_pages:
            batch = self.session.get(url, params=params)
            if not batch:
                return

            more_pages = batch['info']['more_records']
            params['page'] += 1
            for record in batch[self.results_name]:
                yield record


class ReadOnlyModule(ModuleBase):

    def get(self, record_id):
        return self.session.get(f'{self.module_name}/{record_id}')[self.results_name][0]


class RecordModule(ReadOnlyModule):

    def all(self, fields=(), start_page=1, per_page=200, converted='false', params=None):
        if not isinstance(fields, (list, tuple)):
            raise TypeError('fields must be a list or tuple')

        params = params or {}
        params['converted'] = converted

        if fields:
            fields = ','.join(fields)
            params['fields'] = fields

        yield from self._get_all(url=self.module_name, start_page=start_page, per_page=per_page, params=params)

    def _perform_operation(self, method, records=None, params=None):
        is_single = not isinstance(records, list) and records is not None
        records = [records] if is_single else records
        if records is not None:
            data = {
                'data': records,
                'trigger': [],
            }
            results = self.session.request(method, self.module_name, json=data, params=params)['data']
        else:
            results = self.session.request(method, self.module_name, params=params)['data']

        results = [record['details'] if record['status'] == 'success' else {'error': record} for record in results]

        if is_single:
            return results[0]

        return results

    def create(self, records):
        return self._perform_operation('POST', records)

    def update(self, records):
        return self._perform_operation('PUT', records)

    def delete(self, record_ids):
        return self._perform_operation('DELETE', params=dict(ids=','.join(record_ids)))
