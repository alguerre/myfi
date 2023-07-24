import pandas as pd

from repositories.finances import FinancesRepository
from src.jobs.add_source_data.constants import EXCEL_FORMAT
from src.utils.command import Command
from src.utils.logging import get_logger

logger = get_logger(__name__)


class AddSourceDataCommand(Command):
    def __init__(self, repository: FinancesRepository, file: str) -> None:
        self.repository = repository
        self.source_file = file

    def read_source(self) -> pd.DataFrame:
        data = pd.read_excel(self.source_file, **EXCEL_FORMAT)
        data["date"] = pd.to_datetime(data["date"], format="%d/%m/%Y")
        return data

    def is_new_data(self, data: pd.DataFrame) -> bool:
        last_date = self.repository.get_last_date()
        if last_date:
            if data["date"].min().date() > last_date:
                return True
        else:
            return True

        logger.warning("Provided data may be not new. Aborting process.")
        return False

    def execute(self) -> None:
        data = self.read_source()

        if self.is_new_data(data):
            insertions = self.repository.add_bulk(data)
            logger.info(f"{insertions} new rows")
