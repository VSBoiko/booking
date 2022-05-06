from datetime import datetime

import requests
import logging

from settings import BNOVO_API, BNOVO_PUBLIC_API, BNOVO_ACCOUNT_ID, BNOVO_USERNAME, BNOVO_PASSWORD, dump


class BnovoRequest:
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    api = BNOVO_API
    public_api = BNOVO_PUBLIC_API

    def __init__(self):
        pass

    # Авторизация
    def _user_authorization(self) -> dict:
        """
        Авторизация пользователя

        Метод API позволяет авторизовать пользователя по его логину и паролю. В ответ будет возвращен
        токен авторизации, который нужно использовать для последующих обращений к API методам, требующим
        авторизации (token в параметрах запросов). После истечения 1 часа, начиная с момента последнего
        использования, токен становится недействительным. Разрешено генерировать неограниченное количество
        токенов на одну пару логин-пароль. Ранее выданный токен при генерации нового не аннулируется.

        :return:
        Пример return:
        (status 200)
        {
          "token": "e51ea80a247d592eb425ff2062621c20"
        }

        Пример return в случае ошибки:
        (status 401)
        {
          "code": 401,
          "message": "Unauthorized"
        }
        """
        return self._send_request(
            method="post",
            url=f'{self.api}/auth',
            headers=self.headers,
            params={},
            data={
                "username": BNOVO_USERNAME,
                "password": BNOVO_PASSWORD,
            }
        )

    def _user_information(self, token: str) -> dict:
        """
        Информация об авторизованном пользователе

        Метод API позволяет получить информацию о пользователе, которому был выдан определенный
        токен. Кроме информации о пользователе будет возвращена информация о глобальных ролях,
        которыми обладает пользователь и список аккаунтов, владельцем которых он является.

        :param token: токен авторизации

        :return:
        Пример return:
        (status 200)
        {
          "user": {
            "id": 1,
            "name": "Иван",
            "surname": "Иванов",
            "username": "user@mail.com",
            "last_login": "2017-06-19 10:48:13",
            "create_date": "2017-06-09 10:48:13",
            "update_date": "2017-06-09 10:48:13",
            "global_roles": [
              {
                "user_id": 1,
                "role": "account_owner",
                "create_date": "2017-06-09 10:48:13",
                "update_date": "2017-06-09 10:48:13"
              }
            ],
            "accounts": [
              {
                "id": 1,
                "name": "Hotel",
                "phone": "7 (999) 111-22-33",
                "email": "hotel@hotel.com",
                "address": "123456, Россия, г. Санкт-Петербург, Невский проспект, д. 77",
                "role": "account_owner",
                "create_date": "2017-06-09 10:48:13",
                "update_date": "2017-06-09 10:48:13"
              }
            ]
          }
        }

        Пример return в случае ошибки:
        (status 401)
        {
          "code": 401,
          "message": "Unauthorized"
        }
        """
        return self._send_request(
            method="get",
            url=f'{self.api}/auth',
            headers=self.headers,
            params={
                "token": token
            },
            data={}
        )

    def _token_deactivation(self, token: str) -> dict:
        """
        Деактивация токена

        Метод API позволяет досрочно прекратить действие выданного ранее токена. Обычное
        время действия токена - 1 час, начиная с момента последнего использования.

        :param token: токен авторизации

        :return:
        Пример return:
        (status 200)
        {
          "logout": true
        }

        Пример return в случае ошибки:
        (status 401)
        {
          "code": 401,
          "message": "Unauthorized"
        }
        """
        return self._send_request(
            method="delete",
            url=f'{self.api}/auth',
            headers=self.headers,
            params={},
            data={
                "token": token
            }
        )

    # Наличие номеров (из публичного API)
    def _rooms(self, date_from: datetime, date_to: datetime):
        """
        Получить список доступных номеров

        Метод API позволяет получить доступные номера по всем категориям аккаунта.
        В ответ будет возвращен список с полным описанием доступных номеров.

        :param date_from: дата начала периода
        :param date_to: дата конца периода

        :return:
        Пример return
        {
          "rooms": [
            {
              "id": 23644,
              "parent_id": 0,
              "name": "Французские номера",
              "description": "",
              "adults": 2,
              "children": 0,
              "available": 4,
              "photos": null,
              "plans": [...],
              "order": null,
              "accommodation_type": 0,
              "youtube_url": null,
              "subrooms": [],
              "amenities": [],
              "extra_array": null,
              "name_ru": "Французские номера",
              "description_ru": null,
              "cancellation_rules_ru": null,
              "booking_guarantee_description_ru": null,
              "prices": {
                "2022-04-01": "17500.00",
                "2022-04-02": "17500.00"
              },
              "price": 35000
            },
            ...
          ]
        }
        """
        return self._send_request(
            method="get",
            url=f'{self.public_api}/rooms',
            headers=self.headers,
            params={
                "account_id": BNOVO_ACCOUNT_ID,
                "dfrom": date_from.strftime("%d-%m-%Y"),
                "dto": date_to.strftime("%d-%m-%Y"),
            },
            data={}
        )

    # Бронирования - создание, изменение и отмена бронирований
    def _add_booking(self):
        pass


    def _send_request(self, method: str, url: str, headers: dict, params: dict,
                      data: dict):
        try:
            req = {
                "method": method,
                "url": url,
                "headers": headers,
            }
            if params:
                req.update({"params": params})
            if data:
                req.update({"json": data})

            response = requests.request(**req)
            return self.__validate(response=response, params=params)

        except Exception as e:
            logging.exception(e)
            return False

    def __validate(self, response, params):
        if response.status_code == 200:
            data = response.json()
            if data.get('error'):
                print("status_code", response.status_code)
                print("headers", self.headers)
                print("params", params)
                print("response", data)
            else:
                return data
        else:
            print(response.status_code, response.text)


# test = BnovoRequest()
# token = test._user_authorization()
# dump(token)
#
# info = test._user_information(token["token"])
# dump(info)
#
# deact = test._token_deactivation(token["token"])
# dump(deact)
