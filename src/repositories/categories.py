from repositories.base import Repository
from src.models import Categories


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
