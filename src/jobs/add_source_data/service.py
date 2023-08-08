import pandas as pd

from src.base.service import BaseService
from src.jobs.add_source_data.uow import AddDataUow
from src.utils.order import Order


class AddDataService(BaseService):
    def __init__(self, uow: AddDataUow):
        self.uow = uow

    def is_new_data(self, data: pd.DataFrame) -> bool:
        with self.uow:
            bank = data["origin"].iloc[0]
            last_date = self.uow.repo.get_one(
                columns=["date"], params={"origin": bank}, order=Order.desc
            )

            if last_date.get("date"):  # will be none if no data for that bank in db
                if data["date"].min().date() <= last_date["date"]:
                    return False
            return True

    def add_data(self, data: pd.DataFrame) -> int:
        with self.uow:
            insertions = self.uow.repo.add_bulk(data)
            self.uow.commit()

        return insertions
