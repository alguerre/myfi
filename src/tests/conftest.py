from datetime import datetime
from os.path import dirname, join

import pandas as pd
from pytest import fixture
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.models import TABLES
from src.utils.database import Base


@fixture(autouse=True)
def in_memory_db():
    engine = create_engine("sqlite:///:memory:")
    with engine.connect() as connection:
        Base.metadata.drop_all(bind=connection, tables=TABLES, checkfirst=True)
        Base.metadata.create_all(bind=connection, tables=TABLES, checkfirst=False)
        connection.commit()

    return engine


@fixture
def session(in_memory_db):
    yield sessionmaker(bind=in_memory_db)()


@fixture
def sample_bank_history():
    return pd.DataFrame(
        {
            "date": [datetime(2018, 1, 1), datetime(2018, 1, 2), datetime(2018, 1, 3)],
            "amount": [2000.0, -15.0, -50.0],
            "concept": ["Acme Corporation", "netflix", "Hulking Center"],
            "total": [2000.0, 1985.0, 1935.0],
        }
    )


@fixture
def sample_files():
    current_directory = dirname(__file__)
    samples_directory = join(
        current_directory, "commands", "add_data", "readers", "samples"
    )
    return {
        "bbva": join(samples_directory, "source_bbva_01012018_to_03012018.xlsx"),
        "dummy": join(samples_directory, "source_dummy_01012018_to_03012018.csv"),
        "n26": join(samples_directory, "source_n26_01012018_to_03012018.csv"),
        "sabadell": join(samples_directory, "source_sabadell_01012018_to_03012018.xls"),
    }
