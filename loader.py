import os

from aiogram import Bot, Dispatcher
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv


class InputUser(StatesGroup):
    test_phone_number = State()
    phone_number = State()
    key = State()


class InputAdmin(StatesGroup):
    count_keys = State()

load_dotenv()
MESSAGE_SPAM_TIME = os.getenv("MESSAGE_SPAM_TIME")
BOT_TOKEN = os.getenv('bot_token')
ROOT_PATH = os.getenv("ROOT_PATH")
bots_list = [Bot(token=BOT_TOKEN, parse_mode='html')]
dp = Dispatcher(storage=MemoryStorage())
