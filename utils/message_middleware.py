import asyncio
import time
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject

from domain.model.user import User
from domain.repository.user import UsersRepository
from loader import MESSAGE_SPAM_TIME


class MessageMiddleware(BaseMiddleware):
    def __init__(self):
        self.storage = {}

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:

        if not await self.is_registered(event):
            await self.register(event)

        if await self.throttling(event):
            return

        return await handler(event, data)

    @staticmethod
    async def is_registered(event: Message) -> bool:
        user_repo = UsersRepository()
        user = await user_repo.get_user_by_tg_id(tg_id=event.from_user.id)
        return bool(user)

    @staticmethod
    async def register(event: Message) -> bool:
        user_repo = UsersRepository()
        return await user_repo.add_new_user(user_data=User(
            tg_id=event.from_user.id,
            username=event.from_user.username))

    async def throttling(self, event: Message):
        user_id = f'{event.from_user.id}'
        check_user = self.storage.get(user_id)
        if check_user:

            if check_user['spam_block']:
                return True

            if time.time() - check_user['timestamp'] <= int(MESSAGE_SPAM_TIME):
                self.storage[user_id]['timestamp'] = time.time()
                self.storage[user_id]['spam_block'] = True
                await event.answer(f'<b>Обнаружена подозрительная активность.</b>')
                await asyncio.sleep(int(MESSAGE_SPAM_TIME))
                self.storage[user_id]['spam_block'] = False
                return True

        self.storage[user_id] = {'timestamp': time.time(), 'spam_block': False}
        return False
