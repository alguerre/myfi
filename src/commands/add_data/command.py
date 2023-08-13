import pandas as pd

from src.commands.add_data.readers import get_reader
from src.commands.add_data.rules import Rules
from src.commands.add_data.service import AddDataService
from src.commands.base.command import Command
from src.utils.logging import get_logger

logger = get_logger(__name__)


class AddDataCommand(Command):
    def __init__(self, service: AddDataService, file: str) -> None:
        self.service = service
        self.file = file
        self.rules = Rules()

    def read_data(self) -> pd.DataFrame:
        reader = get_reader(self.file)
        return reader.read(file=self.file)

    def apply_rules(self, data: pd.DataFrame) -> pd.DataFrame:
        return self.rules.apply(data)

    def execute(self) -> None:
        data = self.read_data()

        if self.service.is_new_data(data):
            data = self.apply_rules(data)
            insertions = self.service.add_data(data)
            logger.info(f"{insertions} new rows")
        else:
            logger.warning("Provided data may be not new. Aborting process.")
