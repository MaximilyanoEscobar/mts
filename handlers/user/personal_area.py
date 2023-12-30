from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from data.keyboard import personal_area_kb_text, generate_personal_area_kb, my_accounts_cd, activate_history_cd
from domain.repository.key import KeysRepository
from domain.repository.user import UsersRepository
from utils.paginator import HistoryPaginator

personal_area_router = Router()


@personal_area_router.message(F.text == personal_area_kb_text)
async def personal_area(message: Message):
    await message.answer('<b>Добро пожаловать в ваш личный кабинет:\n'
                         , reply_markup=generate_personal_area_kb())


@personal_area_router.callback_query(F.text == activate_history_cd)
async def activate_history(call: CallbackQuery):
    users_repo = UsersRepository()
    user_data = await users_repo.get_user_by_tg_id(tg_id=call.from_user.id)
    keys_repo = KeysRepository()
    key_data = await keys_repo.get_keys_data_by_user_id(user_id=user_data.id)
    paginator = HistoryPaginator(items=key_data)
    await call.message.edit_text('<b>Ваш список активаций</b>',
                                 reply_markup=...)
