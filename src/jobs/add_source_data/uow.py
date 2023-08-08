from typing import Callable

from src.base.uow import UnitOfWork
from src.repositories import FinancesRepository


class AddDataUow(UnitOfWork):
    def __init__(self, session_factory: Callable):
        self.session_factory = session_factory

    def __enter__(self):
        self.session = self.session_factory()
        self.repo = FinancesRepository(self.session)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
