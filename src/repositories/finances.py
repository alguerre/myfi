from src.models import Finances
from src.repositories.base import Repository


class FinancesRepository(Repository):
    def __init__(self, session):
        table = Finances
        super().__init__(table, session)
