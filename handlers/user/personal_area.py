from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, CallbackQuery, FSInputFile

from data.keyboard import personal_area_kb_text, generate_personal_area_kb, my_accounts_cd, activate_history_cd
from domain.repository.key import KeysRepository
from domain.repository.user import UsersRepository
from utils.paginator import HistoryPaginator

personal_area_router = Router()


@personal_area_router.message(F.text == personal_area_kb_text)
async def message_personal_area(message: Message):
    users_repo = UsersRepository()
    user_data = await users_repo.get_user_by_tg_id(tg_id=message.from_user.id)

    await message.answer_photo(photo=FSInputFile(path='data/personal_area.jpg'),
                               caption=user_data.__str__(),
                               reply_markup=generate_personal_area_kb())


@personal_area_router.callback_query(F.data == 'back_to_personal_area')
async def callback_personal_area(call: CallbackQuery):
    users_repo = UsersRepository()
    user_data = await users_repo.get_user_by_tg_id(tg_id=call.from_user.id)

    await call.message.edit_caption(caption=user_data.__str__()
                                    , reply_markup=generate_personal_area_kb())


@personal_area_router.callback_query(F.data == activate_history_cd)
@personal_area_router.callback_query(F.data.endswith('page_prev_keys'))
@personal_area_router.callback_query(F.data.endswith('page_next_keys'))
async def history_paginator(call: CallbackQuery):
    users_repo = UsersRepository()
    user_data = await users_repo.get_user_by_tg_id(tg_id=call.from_user.id)
    keys_repo = KeysRepository()
    keys_data = await keys_repo.get_keys_data_by_user_id(user_id=user_data.id)

    async def send_history(paginator: HistoryPaginator):
        try:
            await call.message.edit_caption(caption=paginator.__str__(),
                                            reply_markup=paginator.generate_page())
        except TelegramBadRequest as e:
            if 'message is not modified' in e.message:
                ...

    if call.data.endswith(activate_history_cd):
        await send_history(HistoryPaginator(items=keys_data))

    elif call.data.endswith('page_next_keys'):
        page_now = int(call.data.split(':')[0])
        await send_history(HistoryPaginator(items=keys_data, page_now=page_now + 1))

    elif call.data.endswith('page_prev_keys'):
        page_now = int(call.data.split(':')[0])
        await send_history(HistoryPaginator(items=keys_data, page_now=page_now - 1))
