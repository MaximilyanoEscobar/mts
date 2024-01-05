from domain.model.admin import Admin
from domain.repository.base import BasesRepository


class AdminsRepository(BasesRepository):
    def __init__(self, db_name='admins.json'):
        super().__init__(db_name)

    def get_all(self) -> Admin:
        return Admin(**self._db)
