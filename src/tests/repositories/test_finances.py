from datetime import date

import pandas as pd
from pytest import fixture
from sqlalchemy import text

from repositories import FinancesRepository
from utils.order import Order


@fixture()
def repo(session):
    return FinancesRepository(session)


def insert_new_records(session):
    session.execute(
        text(
            """
                INSERT INTO Finances (date, concept, amount, total, origin)
                VALUES ('2015-12-17', 'gym', 50, 150, 'bbva'),
                       ('2015-12-19', 'cinema', 10, 140, 'bbva'),
                       ('2015-12-22', 'food', 30, 110, 'bbva'),
                       ('2015-12-21', 'bus', 2.5, 107.5, 'bbva');
            """
        )
    )


def test_get(repo, session):
    insert_new_records(session)

    result = repo.get(
        columns=["date", "concept", "amount", "total", "origin"],
        params={"concept": "gym"},
    )

    assert len(result) == 1
    assert result.iloc[0].to_dict() == {
        "amount": 50,
        "concept": "gym",
        "date": date(2015, 12, 17),
        "origin": "bbva",
        "total": 150,
    }


def test_get__last_date(repo, session):
    insert_new_records(session)

    result = repo.get(columns=["date"], order=Order.desc, limit=1)

    assert result["date"].iloc[0] == date(2015, 12, 22)


def test_add_bulk(repo):
    data = pd.DataFrame(
        {
            "amount": [10, 100],
            "concept": ["burger", "amazon"],
            "date": [date(2016, 1, 1), date(2016, 1, 2)],
            "origin": ["bank1", "bank2"],
        }
    )
    assert repo.add_bulk(data) == 2


def test_update(repo, session):
    insert_new_records(session)
    n = repo.update(params={"concept": "gy%"}, values={"amount": 888})
    session.commit()

    updated_row = session.execute(
        text("""SELECT date, concept, amount FROM finances WHERE concept == 'gym' """)
    ).all()

    assert n == 1
    assert updated_row == [("2015-12-17", "gym", 888)]
