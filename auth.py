
from settings import BNOVO_USERNAME, BNOVO_PASSWORD
from basic import BnovoBasic


class BnovoAuth (BnovoBasic):
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    def __init__(self):
        super().__init__()
        self._username = BNOVO_USERNAME
        self._password = BNOVO_PASSWORD
        self._token = self._request_token()

    def _request_token(self):
        api_url = f'{self._api}/auth'
        params = {
            "username": self._username,
            "password": self._password,
        }

        result = self._request(
            method="post",
            url=api_url,
            headers=self._headers,
            params=params,
        )

        return result

    def get_token(self):
        if "token" in self._token:
            return self._token["token"]
        else:
            return {
                "error": "Ошибка при получении токена"
            }


test = BnovoAuth()
print(test.get_token())
