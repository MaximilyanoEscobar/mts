from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile, CallbackQuery

from data.keyboard import generate_start_kb, check_number_kb_text, generate_cancel_input_kb, cancel_input_cd, \
    help_kb_text, generate_help_kb
from loader import InputUser, ROOT_PATH

echo_router = Router()


@echo_router.message(Command('start'))
async def echo_start(message: Message):
    await message.answer_photo(photo=FSInputFile(path=f'{ROOT_PATH}/data/start_message.jpg'),
                               caption='<b>🦔 <u>Еж-Шэдоу приветствует тебя!</u> 🦔\n'
                                       'Добро пожаловать в бота для подключения MTS-PREMIUM! 🚀\n'
                                       'Ознакомься с выпавшей снизу клавиатурой и начни получать удовольствие вместе со мной! 😊🔴</b>',
                               reply_markup=generate_start_kb())


@echo_router.message(F.text == check_number_kb_text)
async def check_number(message: Message, state: FSMContext):
    message = await message.reply('<b>🔴 Пришли мне номер телефона для проверки возможных подписок для подключения</b>',
                                  reply_markup=generate_cancel_input_kb())
    await state.update_data(message=message)
    await state.set_state(InputUser.test_phone_number)


@echo_router.callback_query(F.data == cancel_input_cd)
async def cancel_callback_query(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(f'<b>🔴 Действие отменено</b>')
    await state.clear()


@echo_router.message(F.text == help_kb_text)
async def help_kb(message: Message):
    await message.delete()
    await message.answer('<b>🔴 Меню помощи:</b>',
                         reply_markup=generate_help_kb())


@echo_router.callback_query()
async def callback_query(call: CallbackQuery):
    await call.message.edit_text('<b>🔴 Я не понимаю вас..</b>')


@echo_router.message()
async def echo(message: Message):
    await message.answer('<b>🔴 Я не понимаю вас..</b>')
