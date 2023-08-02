from sqlalchemy.engine.base import Connection

from base.command import Command
from src.models import TABLES
from src.utils.database import Base


class CreateTableCommand(Command):
    def __init__(self, conn: Connection) -> None:
        self.conn = conn

    def execute(self) -> None:
        Base.metadata.drop_all(bind=self.conn, tables=TABLES, checkfirst=False)
        Base.metadata.create_all(bind=self.conn, tables=TABLES, checkfirst=False)
        self.conn.commit()
