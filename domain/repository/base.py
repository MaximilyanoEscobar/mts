import json
import logging

from loader import ROOT_PATH


class BasesRepository:
    def __init__(self, db_name):
        with open(f'{ROOT_PATH}/db/{db_name}', mode='r') as f:
            self._db_name = db_name
            self._db: dict = json.loads(f.read())

    async def _update_db(self) -> bool:
        try:
            with open(f'{ROOT_PATH}/db/{self._db_name}', 'w') as file:
                json.dump(self._db, file, indent=2)
            return True
        except FileNotFoundError:
            logging.error(f'{ROOT_PATH}/db/{self._db_name}')
            raise

    async def _get_new_id(self) -> str:
        if self._db.__len__() == 0:
            return "1"
        return str(self._db.__len__() + 1)
