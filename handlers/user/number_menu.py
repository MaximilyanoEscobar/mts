import re

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiohttp import ClientResponseError

from api.mts.requests import MtsAPI
from data.keyboard import generate_available_subscriptions_kb
from loader import InputUser

number_router = Router()


@number_router.message(InputUser.test_phone_number)
@number_router.message(InputUser.phone_number)
async def input_phone_number(message: Message, state: FSMContext):
    state_data = await state.get_data()
    state_info = await state.get_state()
    message_before: Message = state_data['message']
    search = re.match(r'7[0-9]{10}', message.text)
    if not search:
        return await message.reply('<b>🔴 Введите правильно номер:\n'
                                   'Пример: <code>79689878787</code></b>')

    async def test_phone_number():
        await message.reply(text=text_to_answer,
                            reply_markup=generate_available_subscriptions_kb(allowed_tariff_list))

    async def real_phone_number():
        await message.answer(text='<b>🔴 Выберите подписку на ваш выбор:</b>')
        await message.reply(text=text_to_answer,
                            reply_markup=generate_available_subscriptions_kb(allowed_tariff_list,
                                                                             with_cb=True))
        await state.update_data(id=state_data['id'], phone_number=phone_number)

    await message_before.edit_reply_markup()
    await state.clear()
    mts_api = MtsAPI()
    phone_number = search.group(0)
    try:
        my_tariff_list = await mts_api.get_tariff_now(phone_number=phone_number)
    except Exception as e:
        return await message.reply(f'<b>🔴 Произошла ошибка: {e}</b>')
    try:
        allowed_tariff_list = await mts_api.get_tariff_list(phone_number=phone_number)
    except ClientResponseError:
        return await message.reply('<b>🔴 Произошла проблема с номером, проверьте его правильность</b>')
    text_to_answer = '🔴 '
    if bool(my_tariff_list.root.__len__()):
        text_to_answer += my_tariff_list.root.pop().__str__() + '\n'
    text_to_answer += f'{allowed_tariff_list.__str__()}'
    text_to_answer = '<b>' + text_to_answer + '</b>'

    if state_info.endswith('test_phone_number'):
        return await test_phone_number()

    elif state_info.endswith('phone_number'):
        return await real_phone_number()
