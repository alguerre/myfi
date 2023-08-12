from datetime import date

import pandas as pd
from pytest import fixture

from src.commands.base.uow import UnitOfWork
from src.gui.service import DataService
from src.repositories.base import Repository


class FakeRepository(Repository):
    def __init__(self, data):
        super().__init__(table="Fake", session=None)
        self.data = data

    def get(self, *args, **kwargs):
        return self.data


class FakeUnitOfWork(UnitOfWork):
    def __init__(self):
        self.repo_categories = FakeRepository(
            data=pd.DataFrame(
                {"id": [1, 2, 3, 4], "category": ["BILLS", "CASH", "HOUSING", "SALARY"]}
            )
        )
        self.repo_finances = FakeRepository(
            data=pd.DataFrame(
                {
                    "category_id": 2 * [2, 4, 3, 1, 1] + [2, 3],
                    "date": [date(2020, 1, day + 1) for day in range(5)]
                    + [date(2021, 1, day + 1) for day in range(5)]
                    + [date(2022, 1, day + 1) for day in range(2)],
                    "concept": 2
                    * ["cash", "salary", "rental", "electricity", "internet"]
                    + ["cash", "rental"],
                    "amount": [-200, 2000, -900, -20, -25]
                    + [-180, 2200, -950, -21, -28]
                    + [-350, -2200],
                    "total": [10025, 12025, 11125, None, None]
                    + [None, None, None, None, None]
                    + [None, None],
                }
            )
        )
        self.committed = False

    def commit(self):
        self.committed = True

    def rollback(self):
        pass


@fixture
def service() -> DataService:
    uow = FakeUnitOfWork()
    return DataService(uow)


def test_data(service):
    assert service.data["total"].to_list() == [
        9551,
        11751,
        12101,
        12129,
        12150,
        13100,
        10900,
        11080,
        11105,
        11125,
        12025,
        10025,
    ]


def test_years(service):
    assert service.years == [2020, 2021, 2022]


def test_categories(service):
    assert service.categories == ["BILLS", "CASH", "HOUSING", "SALARY"]


def test_total_salary_per_year(service):
    assert service.total_salary_per_year().to_dict() == {
        "amount": {2020: 2000, 2021: 2200}
    }


def test_expenses_per_category_per_year(service):
    assert service.expenses_per_category_per_year("BILLS").to_dict() == {
        "amount": {2020: -45, 2021: -49}
    }


def test_categorized_expenses(service):
    expenses = service.categorized_expenses(2020).to_dict()
    share = expenses["share"]
    assert round(share["CASH"], 1) == 17.5
    assert round(share["HOUSING"], 1) == 78.6
    assert round(share["REMAINING"], 1) == 3.9


def test_categorized_expenses__single_category():
    uow = FakeUnitOfWork()
    repo_categories = FakeRepository(
        data=pd.DataFrame({"id": [1], "category": ["CASH"]})
    )
    repo_finances = FakeRepository(
        data=pd.DataFrame(
            {
                "category_id": [1],
                "amount": [-100],
                "date": [date(2020, 1, 1)],
                "total": [0],
                "concept": ["total"],
            }
        )
    )
    uow.repo_categories = repo_categories
    uow.repo_finances = repo_finances
    service = DataService(uow)

    expenses = service.categorized_expenses(2020).to_dict()
    share = expenses["share"]
    assert round(share["CASH"], 1) == 100


def test_total_money(service):
    assert service.total_money().to_dict("list") == {
        "date": [date(2020, 1, day + 1) for day in range(5)]
        + [date(2021, 1, day + 1) for day in range(5)]
        + [date(2022, 1, day + 1) for day in range(2)],
        "total": [
            10025,
            12025,
            11125,
            11105,
            11080,
            10900,
            13100,
            12150,
            12129,
            12101,
            11751,
            9551,
        ],
    }


def test_yearly_savings(service):
    assert service.yearly_savings().to_dict() == {
        2020: 1055.0,
        2021: 1201.0,
        2022: -2200.0,
    }
