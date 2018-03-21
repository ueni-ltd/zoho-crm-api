
class ZohoAPIError(Exception):

    def __init__(self, response=None, text=None):
        self.response = response
        if text is not None:
            super().__init__(text)
        else:
            response = response if isinstance(response, dict) else response.json()
            super().__init__(f'{response["code"]} - {response["message"]} - {response["details"]}')
