from typing import Optional, List

from pydantic import BaseModel


class Admin(BaseModel):
    admins_list: Optional[List[int]]