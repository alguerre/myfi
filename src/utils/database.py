from functools import wraps

import sqlalchemy
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Session, declarative_base

Base = declarative_base()


def get_engine(
    engine: str, username: str, password: str, host: str, port: str, database: str
) -> Engine:
    return sqlalchemy.create_engine(
        f"{engine}://{username}:{password}@{host}:{port}/{database}",
        connect_args={"connect_timeout": 30},
    )


def with_session(engine):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with Session(engine) as session:
                return func(session, *args, **kwargs)

        return wrapper

    return decorator


def with_connection(engine):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with engine.connect() as connection:
                return func(connection, *args, **kwargs)

        return wrapper

    return decorator
