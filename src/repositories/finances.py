from datetime import date
from typing import List, Optional

import pandas as pd
from sqlalchemy import desc, func, update
from sqlalchemy.orm import Session

from repositories.abc import Repository
from src.models import Finances


class FinancesRepository(Repository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def add_bulk(self, data: pd.DataFrame) -> int:
        self.session.bulk_insert_mappings(Finances, data.to_dict("records"))
        self.session.commit()
        return len(data)

    def get_last_date(self) -> Optional[date]:
        query = self.session.query(Finances.date).order_by(desc(Finances.date)).limit(1)
        return query.scalar()

    # todo: remove
    def get_by_concept(self, find_target: str) -> pd.DataFrame:
        # TODO: incluir fechas en las que se que han sido, para afinar mas
        query = self.session.query(Finances).filter(Finances.concept == find_target)
        result = pd.read_sql(query.statement, self.session.bind)
        if not result.empty:
            return result
        return pd.DataFrame()

    def update_category(self, word: str, category_id: int) -> int:
        update_query = (
            update(Finances)
            .where(func.lower(Finances.concept).like(f"%{word.lower()}%"))
            .where((Finances.automatic.is_(None)) | (Finances.automatic == True))
            .values(category_id=category_id, automatic=True)
        )

        result = self.session.execute(update_query)
        self.session.commit()
        return result.rowcount

    # todo: remove
    def get_years(self) -> Optional[List[int]]:
        query = self.session.query(func.date_part("YEAR", Finances.date)).distinct()

        if results := query.all():
            return sorted(list(map(lambda x: int(x[0]), results)))
        return None

    def get_all(self) -> pd.DataFrame:
        query = self.session.query(Finances)
        return pd.read_sql(query.statement, self.session.bind)
