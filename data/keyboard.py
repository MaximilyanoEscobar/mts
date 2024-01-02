from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from api.mts.models import TariffList

personal_area_kb_text = 'Личный кабинет 🏠'
key_input_kb_text = 'Ввести ключ 🔑'
check_number_kb_text = 'Проверить номер 📱'
help_kb_text = 'Помощь ❓'


def generate_start_kb() -> ReplyKeyboardMarkup:
    start_kb = ReplyKeyboardBuilder()
    start_kb.row(KeyboardButton(text=personal_area_kb_text))
    start_kb.row(KeyboardButton(text=key_input_kb_text))
    start_kb.row(KeyboardButton(text=check_number_kb_text))
    start_kb.row(KeyboardButton(text=help_kb_text))
    return start_kb.as_markup(resize_keyboard=True)


activate_history_cd = 'my_activate_history'
my_accounts_cd = 'my_accounts'


def generate_personal_area_kb() -> InlineKeyboardMarkup:
    personal_area_kb = InlineKeyboardBuilder()
    personal_area_kb.row(InlineKeyboardButton(text='История активаций 🕒',
                                              callback_data=activate_history_cd))
    # personal_area_kb.row(InlineKeyboardButton(text='Мои аккаунты 📂',
    #                                           callback_data=my_accounts_cd))
    return personal_area_kb.as_markup()


cancel_input_cd = 'cancel_input'


def generate_cancel_input_kb() -> InlineKeyboardMarkup:
    cancel_input_kb = InlineKeyboardBuilder()
    cancel_input_kb.row(InlineKeyboardButton(text='Отменить ввод ❌',
                                             callback_data=cancel_input_cd))
    return cancel_input_kb.as_markup()


def generate_available_subscriptions_kb(allowed_tariff_list: TariffList) -> InlineKeyboardMarkup:
    available_subscriptions_kb = InlineKeyboardBuilder()
    valid_subscriptions = ['4f3fdad5-9d04-4d6a-b049-76c195c79110',
                           '165c5cc9-bd46-4cc1-a152-d4b873584113',
                           '8f734717-702e-42f4-bfaf-bc2240162ab6',
                           'c3be0b5c-760e-43e5-b089-24336ced1950']
    for tariff in allowed_tariff_list.tariffs:
        if tariff.contentId in valid_subscriptions:
            available_subscriptions_kb.row(InlineKeyboardButton(text=tariff.contentName + ' 💳',
                                                                callback_data='...'))
    return available_subscriptions_kb.as_markup()
