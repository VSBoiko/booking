from datetime import datetime, timedelta

from settings import BNOVO_ACCOUNT_ID
from basic import BnovoBasic


class BnovoRooms (BnovoBasic):
    def __init__(self):
        super().__init__()
        self._account_id = BNOVO_ACCOUNT_ID

    def _request_rooms(self, date_from, date_to):
        api_url = f'{self._public_api}/rooms'
        # date_from = datetime.today()
        # date_to = date_from + timedelta(days=by_days)
        params = {
            "account_id": self._account_id,
            "dfrom": date_from.strftime('%d-%m-%Y'),
            "dto": date_to.strftime('%d-%m-%Y'),
        }

        result = self._request(
            method="get",
            url=api_url,
            headers=self._headers,
            params=params,
        )

        return result

    def get_rooms(self, date_from=None, date_to=None):
        if date_from is None:
            date_from = datetime.today()
        if date_to is None:
            date_to = date_from + timedelta(days=1)

        rooms = self._request_rooms(date_from, date_to)

        if "rooms" in rooms:
            return rooms["rooms"]
        else:
            return {
                "error": "Ошибка при получении списка номеро"
            }


test = BnovoRooms()
print(test.get_rooms())
