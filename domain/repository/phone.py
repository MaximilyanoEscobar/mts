import json
from datetime import datetime

from domain.model.phone import Phone
from domain.repository.base import BasesRepository


class PhonesRepository(BasesRepository):
    def __init__(self, db_name='phones.json'):
        super().__init__(db_name)

    async def add_new_phone(self, phone_data: Phone = Phone()) -> str:
        """
        :param phone_data:
        :return: phone_id
        """
        id = await self._get_new_id()
        phone_data.id = id
        await self._update_phone_data_by_id(id, phone_data)
        return phone_data.id

    async def _update_phone_data_by_id(self, id: str, phone_data: Phone) -> bool:
        try:
            phone_data.updated_at = datetime.now()
            self._db[id] = json.loads(phone_data.model_dump_json())
            await self._update_db()
            return True
        except Exception as e:
            return False

    async def get_phone_data_by_id(self, id: str) -> Phone:
        return Phone.model_validate_json(self._db[id])
