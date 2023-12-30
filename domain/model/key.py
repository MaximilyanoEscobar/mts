from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Key(BaseModel):
    id: Optional[str] = None
    is_used: bool = False
    user_id: Optional[str] = None
    key: Optional[str] = None
    created_at: Optional[datetime] = datetime.now()
    updated_at: Optional[datetime] = datetime.now()




