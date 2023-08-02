import pandas as pd

from base.command import Command
from src.jobs.add_source_data.reader import get_reader
from src.jobs.add_source_data.service import AddDataService
from src.utils.logging import get_logger

logger = get_logger(__name__)


class AddSourceDataCommand(Command):
    def __init__(self, service: AddDataService, file: str) -> None:
        self.service = service
        self.source_file = file

    def read_source(self) -> pd.DataFrame:
        reader = get_reader(self.source_file)
        return reader.read(file=self.source_file)

    def execute(self) -> None:
        data = self.read_source()

        if self.service.is_new_data(data):
            insertions = self.service.add_data(data)
            logger.info(f"{insertions} new rows")
        else:
            logger.warning("Provided data may be not new. Aborting process.")
