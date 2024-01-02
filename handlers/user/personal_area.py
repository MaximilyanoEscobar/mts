from aiogram import Router, F
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
async def activate_history(call: CallbackQuery):
    users_repo = UsersRepository()
    user_data = await users_repo.get_user_by_tg_id(tg_id=call.from_user.id)
    keys_repo = KeysRepository()
    keys_data = await keys_repo.get_keys_data_by_user_id(user_id=user_data.id)
    paginator = HistoryPaginator(items=keys_data)
    await call.message.edit_caption(caption=paginator.__str__(),
                                    reply_markup=paginator.generate_page())
