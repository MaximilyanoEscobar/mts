import re

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from api.mts.requests import MtsAPI
from data.keyboard import generate_available_subscriptions_kb
from loader import InputUser

check_number_router = Router()


@check_number_router.message(InputUser.test_phone_number)
async def check_number(message: Message, state: FSMContext):
    state_data = await state.get_data()
    message_before: Message = state_data['message']
    search = re.match(r'[0-9]{11}', message.text)
    if not search:
        return await message.reply('<b>🔴 Введите правильно номер</b>')

    await message_before.edit_reply_markup()
    await state.clear()
    mts_api = MtsAPI()
    phone_number = search.group(0)
    my_tariff_list = await mts_api.get_tariff_now(phone_number=phone_number)
    allowed_tariff_list = await mts_api.get_tariff_list(phone_number=phone_number)
    text_to_answer = '🔴 '
    if bool(my_tariff_list.tariffs.__len__()):
        text_to_answer += my_tariff_list.tariffs[0].__str__() + '\n'
    text_to_answer += f'{allowed_tariff_list.__str__()}'
    text_to_answer = '<b>' + text_to_answer + '</b>'
    await message.reply(text=text_to_answer,
                        reply_markup=generate_available_subscriptions_kb(allowed_tariff_list))


