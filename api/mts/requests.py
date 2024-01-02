import json
import logging
import random
import string

import aiohttp
from aiohttp import ClientError

from api.mts.models import BaseRequestModel, MyTariffsList, MyTariff, TariffList, Tariff, ActivationResponse


class BaseRequest(object):
    def __init__(self, base_url):
        self.base_url = base_url
        self.headers = {'Authorization': 'OAuth y0_AgAAAABsmBQLAAKkvAAAAADkYx2aUFS5mnJkTP-InW6Z-ecJJM0iMLI'}
        self.proxy = None
        self.debug = True

    async def _request(self, method, endpoint, **params) -> BaseRequestModel:
        url = f"{self.base_url}/{endpoint}"
        try:
            if self.debug:
                dict_params = {**params}
                print(f'[DEBUG] Request URL: {url} Params: {dict_params}')
            async with aiohttp.ClientSession() as session:
                async with session.request(method, url, headers=self.headers,
                                           proxy=self.proxy, **params) as response:
                    response.raise_for_status()
                    if self.debug:
                        print(f'[DEBUG] Response URL: {url} Response: {await response.text()}')
                    return BaseRequestModel(text=await response.text(encoding="utf-8"), status_code=response.status)

        except ClientError as e:
            logging.error(f"Error during API request: {e}")
            raise  # Re-raise the exception


class MtsAPI(BaseRequest):
    def __init__(self, base_url='https://api.music.yandex.net/payclick'):
        super().__init__(base_url=base_url)

    async def get_tariff_now(self, phone_number: str) -> MyTariffsList:
        params = {"msisdn": phone_number}
        response = await self._request(method='GET', endpoint='subscriptions', params=params)
        return MyTariffsList(tariffs=[MyTariff(**iter_data) for iter_data in json.loads(response.text)])

    async def get_tariff_list(self, phone_number: str) -> TariffList:
        params = {"msisdn": phone_number}
        response = await self._request(method='GET', endpoint='content-provider/available-subscriptions', params=params)
        return TariffList(tariffs=[Tariff(**iter_data) for iter_data in json.loads(response.text)])

    async def activate_mts_premium(self, phone_number: str, content_id: str) -> ActivationResponse:
        uid = await self._generate_uid
        bid = await self._generate_bid
        json_data = {
            "userId": f"00000000100090099{uid}",
            "bindingId": f"88b32A591b86Dbcaa98b{bid}",
            "msisdn": phone_number.replace("+", "", 1),
            "contentId": content_id
        }
        response = await self._request(method='POST', endpoint='subscriptions', json=json_data)
        return ActivationResponse(**json.loads(response.text))

    @property
    async def _generate_uid(self):
        return ''.join(random.choice(string.digits) for _ in range(3))

    @property
    async def _generate_bid(self):
        return ''.join(random.choice(string.hexdigits) for _ in range(12))
