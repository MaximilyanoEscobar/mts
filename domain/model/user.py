from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    id: Optional[str] = None
    tg_id: int
    username: str
    is_banned: bool = False
    created_at: Optional[datetime] = datetime.now()
    updated_at: Optional[datetime] = datetime.now()

    def __str__(self):
        return (f'<b>🔴 Добро пожаловать в ваш личный кабинет: 🔴 \n'
                f'🔺 Telegram ID: <i>{self.tg_id}</i>\n'
                f'🔺 Username: <i>{self.username}</i>\n'
                f'🔺 Banned: <i>{"Да" if self.is_banned else "Нет"}</i>\n'
                f'🔺 Зарегистрирован: <i>{self.created_at}</i></b>')


