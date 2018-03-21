from zoho_crm_api.module import ReadOnlyModule


class UsersModule(ReadOnlyModule):

    USER_TYPES = (
        'AllUsers',
        'ActiveUsers',
        'DeactiveUsers',
        'ConfirmedUsers',
        'NotConfirmedUsers',
        'DeletedUsers',
        'ActiveConfirmedUsers',
        'AdminUsers',
        'ActiveConfirmedAdmins',
        'CurrentUser',
    )

    def __init__(self, session):
        super().__init__(session, 'users')
        self.results_name = 'users'

    def all(self, user_type='AllUsers', params=None):
        if user_type not in self.USER_TYPES:
            raise ValueError('User type {} is not in allowed types.'.format(user_type))

        params = params or {}
        params['type'] = user_type

        yield from self._get_all(self.module_name, params=params)
