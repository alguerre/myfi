from typing import List

from jobs.insert_categories.service import InsertCategoriesService
from repositories import CategoriesRepository, FinancesRepository
from base.command import Command
from src.utils.config import get_config
from src.utils.counter import Counter
from src.utils.logging import get_logger
from src.utils.paths import CONFIG_EQUIVALENCES

logger = get_logger(__name__)


class InsertCategoriesCommand(Command):
    def __init__(
        self, service: InsertCategoriesService
    ) -> None:
        self.service = service
        self.equivalences = get_config(CONFIG_EQUIVALENCES)
        self.counter = Counter(initial=0)

    def execute(self) -> None:
        for category, keywords in self.equivalences.items():
            updates = self.service.update_category(category, keywords)

            logger.info(f"Category insertions {updates} for [{category}]")
            self.counter.increment(updates)

        logger.info(f"Total updated rows {self.counter.value()}")
