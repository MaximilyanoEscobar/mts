import random
import string
import uuid

from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from data.keyboard import generate_admin_kb, generate_new_keys_cd, generate_cancel_input_kb
from domain.model.admin import Admin
from domain.model.key import Key
from domain.repository.admin import AdminsRepository
from domain.repository.key import KeysRepository
from domain.repository.user import UsersRepository
from loader import InputAdmin
from utils.admin_filter import is_admin

admin_router = Router()


@admin_router.message(Command('admin'),
                      F.chat.func(lambda chat: is_admin(tg_id=chat.id)))
async def admin(message: Message):
    await message.delete()
    admin_keyboard = generate_admin_kb()
    admin_repo = AdminsRepository()
    admins_list = [str(id) for id in admin_repo.get_all().admins_list]
    user_repo = UsersRepository()
    answer_text = '<b>🔴 Вы успешно вошли в панель администратора: ✅\n</b>'
    answer_text += '<b>Список администраторов на данный момент</b>:\n' + '\n'.join(admins_list)
    answer_text += f'\n<b>Количество юзеров на данный момент: {(await user_repo.get_all_users()).__len__()}</b>'
    await message.answer(answer_text,
                         reply_markup=admin_keyboard)


@admin_router.callback_query(F.data == generate_new_keys_cd,
                             F.from_user.func(lambda from_user: is_admin(tg_id=from_user.id)))
async def new_keys_callback(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text('<b>🔴 Введите количество ключей:</b>',
                                 reply_markup=generate_cancel_input_kb())
    await state.set_state(InputAdmin.count_keys)


@admin_router.message(F.chat.func(lambda chat: is_admin(tg_id=chat.id)),
                      InputAdmin.count_keys)
async def generate_new_keys(message: Message, state: FSMContext):
    if not message.text.isdigit():
        return message.reply('<b>🔴 Введите <u>правильно</u> количество нужных ключей</b>')
    count_keys = int(message.text)
    keys_repo = KeysRepository()
    keys = []
    for test in range(count_keys):
        key = await keys_repo.add_new_key(key_data=Key(key=uuid.uuid4().hex))
        keys.append(key)
    await message.answer('<b>🔴 Ваши ключи:</b>\n' + '\n'.join(f'<code>{key}</code>' for key in keys))
    await state.clear()
