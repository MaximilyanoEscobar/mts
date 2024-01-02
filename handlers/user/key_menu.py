import re

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup
from magic_filter import F

from data.keyboard import help_kb_text, key_input_kb_text, generate_cancel_input_kb
from domain.repository.key import KeysRepository
from loader import InputUser

key_router = Router()


@key_router.message(F.text == key_input_kb_text)
async def key_press(message: Message, state: FSMContext):
    message = await message.answer(text='<b>Введите купленный вами ключ</b>', reply_markup=generate_cancel_input_kb())
    await state.update_data(message=message)
    await state.set_state(InputUser.key)


@key_router.message(InputUser.key)
async def key_input(message: Message, state: FSMContext):
    key = re.search(r'[a-z0-9]{16}', message.text)
    if not key:
        await message.reply(text='<b>Ключ неверного формата</b>')
    key = key.group(0)
    state_data = await state.get_data()
    await state.clear()
    message_before: Message = state_data['message']
    await message_before.edit_reply_markup()
    keys_repo = KeysRepository()
    key_data = await keys_repo.get_key_data_by_key(key=key)
    if not key_data:
        return await message.reply('<b>Такой ключ отсутствует в базе</b>')
    elif key_data.is_used:
        return await message.reply('<b>Ключ уже использован</b>')
    elif key_data.user_id and message.from_user.id == key_data.user_id:
        message = await message.answer(text='<b>Пришлите номер телефона:</b>',
                                       reply_markup=generate_cancel_input_kb())
        await state.update_data(message=message,
                                key_data=key_data)
        await state.set_state(InputUser.phone_number)
    key_data.user_id = message.from_user.id
    await keys_repo.update_key_data_by_id(id=key_data.id,
                                          key_data=key_data)
