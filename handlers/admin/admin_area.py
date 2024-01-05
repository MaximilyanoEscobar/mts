import random
import string
import uuid

from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery

from data.keyboard import generate_admin_kb, generate_new_keys_cd
from domain.model.key import Key
from domain.repository.key import KeysRepository
from utils.admin_filter import is_admin

admin_router = Router()


@admin_router.message(Command('admin'),
                      F.chat.func(lambda chat: is_admin(tg_id=chat.id)))
async def admin(message: Message):
    await message.delete()
    admin_keyboard = generate_admin_kb()
    await message.answer('<b>🔴 Вы успешно вошли в панель администратора: ✅</b>',
                         reply_markup=admin_keyboard)



@admin_router.callback_query(F.data == generate_new_keys_cd,
                             F.from_user.func(lambda from_user: is_admin(tg_id=from_user.id)))
async def generate_new_keys(call: CallbackQuery):
    keys_repo = KeysRepository()
    keys = []
    for test in range(10):
        key = await keys_repo.add_new_key(key_data=Key(key=uuid.uuid4().hex))
        keys.append(key)
    await call.message.answer('\n'.join(f'<code>{key}</code>' for key in keys))


