import pandas as pd

from src.base.command import Command
from src.jobs.add_source_data.reader import get_reader
from src.jobs.add_source_data.rules import Rules
from src.jobs.add_source_data.service import AddDataService
from src.utils.logging import get_logger

logger = get_logger(__name__)


class AddSourceDataCommand(Command):
    def __init__(self, service: AddDataService, file: str) -> None:
        self.service = service
        self.source_file = file
        self.rules = Rules()

    def read_source(self) -> pd.DataFrame:
        reader = get_reader(self.source_file)
        return reader.read(file=self.source_file)

    def apply_rules(self, data: pd.DataFrame) -> pd.DataFrame:
        return self.rules.apply(data)

    def execute(self) -> None:
        data = self.read_source()

        if self.service.is_new_data(data):
            data = self.apply_rules(data)
            insertions = self.service.add_data(data)
            logger.info(f"{insertions} new rows")
        else:
            logger.warning("Provided data may be not new. Aborting process.")
