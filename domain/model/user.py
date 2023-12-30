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

