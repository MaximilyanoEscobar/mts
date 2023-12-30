import math
from typing import List

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from domain.model.key import Key


class Paginator:
    def __init__(self, items, page_now=0, move_page=1, per_page=10):
        self.items: list = items
        self.per_page = per_page
        self.page_now = page_now
        self.move_page = move_page

    def generate_page(self):
        ...

    def __str__(self):
        ...


class HistoryPaginator(Paginator):
    def __init__(self, items: List[Key], page_now=1, move_page=1, per_page=5):
        super().__init__(items=items, page_now=page_now, move_page=move_page, per_page=per_page)

    def generate_page(self) -> InlineKeyboardMarkup:
        keys: List[Key] = self.items
        page_kb = InlineKeyboardBuilder()

        if self.page_now <= 0:
            self.page_now = 1

        if not bool(len(keys[(self.page_now - 1) * self.per_page:self.page_now * self.per_page])):
            self.page_now = 1

        for key_data in keys[(self.page_now - 1) * self.per_page:self.page_now * self.per_page]:
            page_kb.row(InlineKeyboardButton(text=f'🔍 {key_data.key}',
                                             callback_data=f'{key_data.id}:look_key'))
        page_kb.row(InlineKeyboardButton(text='◀️ Назад',
                                         callback_data=f'{self.page_now}:page_prev_keys'))
        page_kb.add(InlineKeyboardButton(text=f'{self.page_now}/{math.ceil(keys.__len__() / self.per_page)}',
                                         callback_data=f'{self.page_now}:page_now'))
        page_kb.add(InlineKeyboardButton(text='Вперед ▶️',
                                         callback_data=f'{self.page_now}:page_next_keys'))
        page_kb.row(InlineKeyboardButton(text='🔽 Вернуться в список объявлений',
                                         callback_data='back_to_keys'))
        return page_kb.as_markup()

    def __str__(self):
        return '<b>Список объявлений:</b>'