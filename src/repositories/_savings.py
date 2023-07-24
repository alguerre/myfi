import pandas as pd
from sqlalchemy.orm import Session

from repositories.abc import Repository
from src.models import Savings


class SavingsRepository(Repository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def add_bulk(self, data: pd.DataFrame) -> int:
        self.session.bulk_insert_mappings(Savings, data.to_dict("records"))
        self.session.commit()
        return len(data)

    def get_all(self) -> pd.DataFrame:
        query = self.session.query(Savings)
        return pd.read_sql(query.statement, self.session.bind)
