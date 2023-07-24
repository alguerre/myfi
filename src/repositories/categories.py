import pandas as pd
from sqlalchemy.orm import Session

from repositories.abc import Repository
from src.models import Categories


class CategoriesRepository(Repository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, category: str) -> int:
        instance = Categories(category=category.upper())
        self.session.add(instance)
        self.session.commit()
        return instance.id

    def get_by_name(self, category: str):
        query = self.session.query(Categories).filter(
            Categories.category == category.upper()
        )
        return query.scalar()

    def get_all(self) -> pd.DataFrame:
        query = self.session.query(Categories)
        return pd.read_sql(query.statement, self.session.bind)
