import json
from typing import List, Optional

from domain.model.user import User
from domain.repository.base import BasesRepository


class UsersRepository(BasesRepository):
    def __init__(self, db_name='users.json'):
        super().__init__(db_name)

    async def add_new_user(self, user_data: User) -> bool:
        try:
            id = await self.get_new_id()
            user_data.id = id
            self._db[id] = json.loads(user_data.model_dump_json())
            await self._update_db()
            return True
        except Exception as e:
            return False

    async def get_all_users(self) -> List[Optional[User]]:
        return [User(**user_data) for user_data in self._db]

    async def get_user_by_id(self, id: str) -> Optional[User]:
        try:
            return User(**self._db[id])
        except Exception as e:
            return None

    async def update_user_by_id(self, id: str, user_data: User) -> bool:
        try:
            self._db[id] = json.loads(user_data.model_dump_json())
            await self._update_db()
            return True
        except Exception as e:
            return False

    async def ban_user_by_id(self, id: str) -> bool:
        try:
            user_data = await self.get_user_by_id(id)
            if user_data:
                user_data.is_banned = True
                return await self.update_user_by_id(id, user_data)
            return False
        except Exception as e:
            return False

    async def get_user_by_tg_id(self, tg_id: int) -> Optional[User]:
        try:
            for user_data in self._db:
                user_data = User(**user_data)
                if user_data.tg_id == tg_id:
                    return user_data
        except Exception as e:
            return None
