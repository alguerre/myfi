from abc import ABC, abstractmethod

from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import sessionmaker


class UnitOfWork(ABC):
    def __init__(
        self,
        engine: Engine,
    ):
        self.session_factory = sessionmaker(bind=engine)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @abstractmethod
    def commit(self):
        raise NotImplementedError

    @abstractmethod
    def rollback(self):
        raise NotImplementedError
