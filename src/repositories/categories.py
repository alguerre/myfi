from src.models import Categories
from src.repositories.base import Repository


class CategoriesRepository(Repository):
    def __init__(self, session):
        table = Categories
        self.session = session
        super().__init__(table, session)

    def add(self, category: str) -> int:
        instance = Categories(category=category.upper())
        self.session.add(instance)
        self.session.commit()
        return instance.id
