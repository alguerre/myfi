from typing import Optional

from src.models import Finances
from src.repositories.base import Repository
from datetime import date
from src.utils.order import Order


class FinancesRepository(Repository):
    def __init__(self, session):
        table = Finances
        super().__init__(table, session)

    def get_last_date(self, origin: str) -> Optional[date]:
        last_date = self.get_one(
            columns=["date"], params={"origin": origin}, order=Order.desc
        )

        return last_date.get("date")

    def update_category(self, word: str, category_id: int) -> int:
        return self.update(
            params={"concept": f"%{word}%"}, values={"category_id": category_id}
        )
