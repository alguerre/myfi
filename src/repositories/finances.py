from datetime import date
from typing import Optional

import pandas as pd
from sqlalchemy import desc, func, update
from sqlalchemy.orm import Session

from repositories.base import Repository
from src.models import Finances


class FinancesRepository(Repository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def add_bulk(self, data: pd.DataFrame) -> int:
        self.session.bulk_insert_mappings(Finances, data.to_dict("records"))
        return len(data)

    def get_last_date(self, origin: str) -> Optional[date]:
        query = (
            self.session.query(Finances.date)
            .where(Finances.origin == origin)
            .order_by(desc(Finances.date))
            .limit(1)
        )
        return query.scalar()

    def update_category(self, word: str, category_id: int) -> int:
        update_query = (
            update(Finances)
            .where(func.lower(Finances.concept).like(f"%{word.lower()}%"))
            .where((Finances.automatic.is_(None)) | (Finances.automatic == True))
            .values(category_id=category_id, automatic=True)
        )

        result = self.session.execute(update_query)

        return result.rowcount

    def get_all(self) -> pd.DataFrame:
        query = self.session.query(Finances)
        return pd.read_sql(query.statement, self.session.bind)
