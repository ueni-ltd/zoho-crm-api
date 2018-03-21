from datetime import datetime
from datetime import timedelta

import requests
from requests import Session
from requests import HTTPError

from zoho_crm_api.exceptions import ZohoAPIError


class ZohoSession(Session):

    def __init__(self, refresh_token, client_id, client_secret, domain='eu', api_version='v2'):
        super().__init__()
        self.domain = domain
        self.api_version = api_version
        self.base_url = f'https://www.zohoapis.{domain}/crm/{api_version}/'
        self.client_id = client_id
        self.client_secret = client_secret
        self.refresh_token = refresh_token
        self.access_token = None
        self.expires_at = datetime.now() - timedelta(days=1)
        self.headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Simple Zoho CRM Client',
        }

    def refresh_access_token(self):
        response = requests.post(
            url=f'https://accounts.zoho.{self.domain}/oauth/{self.api_version}/token',
            params=dict(
                refresh_token=self.refresh_token,
                client_id=self.client_id,
                client_secret=self.client_secret,
                grant_type='refresh_token',
            )
        )
        try:
            response.raise_for_status()
        except HTTPError:
            raise ZohoAPIError(response=response, text=f"Couldn't refresh access token. Reason : {response.content}")

        response = response.json()
        self.access_token = response['access_token']
        self.expires_at = datetime.now() + timedelta(seconds=response['expires_in_sec'])

    def update_header(self):
        if self.expires_at <= datetime.now():
            self.refresh_access_token()
            self.headers['Authorization'] = 'Zoho-oauthtoken ' + self.access_token

    @staticmethod
    def check_for_error(response):
        data = response.get('data')
        if data and len(data) == 1 and 'status' in data[0] and data[0]['status'] == 'error':
            raise ZohoAPIError(response=data[0])

    def request(self, method, url, **kwargs):
        self.update_header()
        url = self.base_url + url.lstrip('/')
        response = super().request(method, url, **kwargs)
        try:
            response.raise_for_status()
        except HTTPError:
            raise ZohoAPIError(response=response)

        if response.status_code == 204:
            # No content
            response = None
        else:
            response = response.json()
            self.check_for_error(response)

        return response
