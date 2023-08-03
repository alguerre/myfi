from sqlalchemy.engine.base import Connection

from base.command import Command
from src.models import TABLES
from src.utils.database import Base
from utils.logging import get_logger

logger = get_logger(__name__)


class CreateTableCommand(Command):
    def __init__(self, conn: Connection) -> None:
        self.conn = conn

    def execute(self) -> None:
        logger.info("Dropping existing tables")
        Base.metadata.drop_all(bind=self.conn, tables=TABLES, checkfirst=False)

        logger.info("Creating tables")
        Base.metadata.create_all(bind=self.conn, tables=TABLES, checkfirst=False)

        self.conn.commit()
