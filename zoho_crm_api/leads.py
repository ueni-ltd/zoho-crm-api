from .module import RecordModule


class LeadsModule(RecordModule):

    def convert(self, record_id, owner, deal=None):
        data = {
            'overwrite': True,
            'notify_lead_owner': False,
            'notify_new_entity_owner': False,
            'assign_to': owner,
        }
        if deal:
            data['Deals'] = deal

        data = {'data': [data]}
        return self.session.post(f'{self.module_name}/{record_id}/actions/convert', json=data)['data'][0]
