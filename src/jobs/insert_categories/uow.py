from typing import Callable

from base.uow import UnitOfWork
from repositories import CategoriesRepository, FinancesRepository


class InsertCategoriesUow(UnitOfWork):
    def __init__(self, session_factory: Callable):
        self.session_factory = session_factory

    def __enter__(self):
        self.session = self.session_factory()
        self.repo_finances = FinancesRepository(self.session)
        self.repo_categories = CategoriesRepository(self.session)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
