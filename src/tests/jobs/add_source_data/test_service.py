from datetime import date, datetime

import pandas as pd
from pytest import fixture

from src.commands.add_source_data import AddDataService
from src.commands.base.uow import UnitOfWork
from src.repositories.base import Repository


class FakeRepository(Repository):
    def __init__(self):
        super().__init__(table="Fake", session=None)

    def add_bulk(self, data):
        return len(data)

    def get_last_date(self, origin: str):
        return date(2000, 3, 27)


class FakeUnitOfWork(UnitOfWork):
    def __init__(self):
        self.repo = FakeRepository()
        self.committed = False

    def commit(self):
        self.committed = True

    def rollback(self):
        pass


@fixture
def service():
    uow = FakeUnitOfWork()
    return AddDataService(uow)


def test_is_new_data__yes(service):
    data = pd.DataFrame(
        {
            "origin": ["bank1", "bank1"],
            "date": [datetime(2005, 12, 5), datetime(2005, 12, 25)],
        }
    )
    assert service.is_new_data(data)


def test_is_new_data__no(service):
    data = pd.DataFrame(
        {
            "origin": ["bank1", "bank2"],
            "date": [datetime(1999, 12, 5), datetime(1999, 12, 25)],
        }
    )
    assert not service.is_new_data(data)


def test_add_data(service):
    data = pd.DataFrame({"concept": ["gym", "food"], "amount": [50, 30.5]})

    assert service.add_data(data) == len(data)
    assert service.uow.commit
