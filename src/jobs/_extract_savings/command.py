import pandas as pd

from src.repositories import FinancesRepository, SavingsRepository
from src.utils.command import Command
from src.utils.logging import get_logger

logger = get_logger(__name__)


class ExtractSavingsCommand(Command):
    def __init__(
        self, repo_finances: FinancesRepository, repo_savings: SavingsRepository
    ) -> None:
        self.repo_finances = repo_finances
        self.repo_savings = repo_savings
        self.savings_concept = "TRANSFERENCIA A ALONSO GUERRERO LLORENTE"

    def insert_savings_to_table(self, savings: pd.DataFrame) -> int:
        savings["date"] = pd.to_datetime(savings["date"], format="%d/%m/%Y")
        savings["finance_id"] = savings["id"]
        savings = savings[["date", "amount", "finance_id"]].sort_values("date")
        savings["total"] = savings["amount"].cumsum()
        self.repo_savings.add_bulk(savings)

        return len(savings)

    def execute(self) -> None:
        savings_rows = self.repo_finances.get_by_concept(self.savings_concept)
        new_rows = (
            self.insert_savings_to_table(savings_rows) if not savings_rows.empty else 0
        )
        logger.info(f"Total new rows {new_rows}")
