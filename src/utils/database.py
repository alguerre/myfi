import sqlalchemy
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import declarative_base

Base = declarative_base()


def get_engine(
    engine: str, username: str, password: str, host: str, port: str, database: str
) -> Engine:
    return sqlalchemy.create_engine(
        f"{engine}://{username}:{password}@{host}:{port}/{database}",
        connect_args={"connect_timeout": 30},
    )
