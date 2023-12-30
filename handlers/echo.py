from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, InputFile, FSInputFile

from data.keyboard import generate_start_kb, check_number_kb_text, generate_cancel_input_kb

echo_router = Router()


@echo_router.message(Command('start'))
async def echo_start(message: Message):
    await message.answer_photo(photo=FSInputFile(path='data/start_message.jpg'),
                               caption=f'<b>Еж-Шэдоун приветствует тебя!\n'
                                       f'Добро пожаловать в бота для подключения MTS-PREMIUM!\n'
                                       f'Ознакомься с выпавшей снизу клавиатурой и начни получать удовольствие вместе со мной</b>')


@echo_router.message(F.text == check_number_kb_text)
async def check_number(message: Message):
    await message.reply('<b>Пришли мне номер телефона для проверки возможных подписок для подключения</b>',
                        reply_markup=generate_cancel_input_kb())


@echo_router.message()
async def echo(message: Message):
    await message.answer('<b>Я не понимаю вас..</b>')
