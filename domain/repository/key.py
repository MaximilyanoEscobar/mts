import json
import uuid
from typing import List, Optional

from domain.model.key import Key
from domain.repository.base import BasesRepository


class KeysRepository(BasesRepository):
    def __init__(self, db_name='keys.json'):
        super().__init__(db_name)

    async def get_all_keys(self) -> List[Optional[Key]]:
        return [Key(**self._db[id]) for id in self._db]

    async def get_key_data_by_id(self, id: str) -> Optional[Key]:
        try:
            return Key(**self._db[id])
        except Exception as e:
            return None

    async def update_key_data_by_id(self, id: str, key_data: Key) -> bool:
        try:
            self._db[id] = json.loads(key_data.model_dump_json())
            await self._update_db()
            return True
        except Exception as e:
            return False

    async def get_key_data_by_key(self, key: str) -> Optional[Key]:
        for id in self._db:
            key_data = Key(**self._db[id])
            if key_data.key == key:
                return key_data

    async def get_keys_data_by_user_id(self, user_id: str) -> List[Optional[Key]]:
        return [Key(**self._db[id]) for id in self._db if Key(**self._db[id]).user_id == user_id]

    async def add_new_key(self, key_data: Key) -> str:
        id = await self.get_new_id()
        key_data.id = id
        key_data.key = uuid.uuid4().__str__()
        await self.update_key_data_by_id(id, key_data)
        return key_data.key
