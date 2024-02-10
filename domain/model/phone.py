from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Phone(BaseModel):
    id: Optional[str] = None
    phone: Optional[str] = None
    key_id: Optional[str] = None
    created_at: Optional[datetime] = datetime.now()
    updated_at: Optional[datetime] = datetime.now()