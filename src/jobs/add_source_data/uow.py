from sqlalchemy.orm import sessionmaker

from base.uow import UnitOfWork
from deps import engine
from repositories import FinancesRepository


class AddDataUow(UnitOfWork):
    def __init__(self):
        self.session_factory = sessionmaker(bind=engine)

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
