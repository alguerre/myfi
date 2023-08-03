import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import TABLES
from utils.database import Base


@pytest.fixture
def in_memory_db():
    engine = create_engine("sqlite:///:memory:")
    with engine.connect() as connection:
        Base.metadata.drop_all(bind=connection, tables=TABLES, checkfirst=True)
        Base.metadata.create_all(bind=connection, tables=TABLES, checkfirst=False)
        connection.commit()

    return engine


@pytest.fixture
def session(in_memory_db):
    yield sessionmaker(bind=in_memory_db)()
