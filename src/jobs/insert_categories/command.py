from typing import List

from repositories import CategoriesRepository, FinancesRepository
from src.utils.command import Command
from src.utils.config import get_config
from src.utils.counter import Counter
from src.utils.logging import get_logger
from src.utils.paths import CONFIG_EQUIVALENCES

logger = get_logger(__name__)


class InsertCategoriesCommand(Command):
    def __init__(
        self, repo_categories: CategoriesRepository, repo_finances: FinancesRepository
    ) -> None:
        self.repo_categories = repo_categories
        self.repo_finances = repo_finances
        self.equivalences = get_config(CONFIG_EQUIVALENCES)
        self.counter_category = Counter(initial=0)
        self.counter_total = Counter(initial=0)

    def get_category_id(self, category: str) -> int:
        if result := self.repo_categories.get_by_name(category):
            return result.id

        return self.repo_categories.add(category)

    def set_category(self, category_id: int, keywords: List[str]) -> int:
        self.counter_category.reset()

        for word in keywords:
            updated_rows = self.repo_finances.update_category(word, category_id)
            self.counter_category.increment(updated_rows)

        return self.counter_category.value()

    def execute(self) -> None:
        for category, keywords in self.equivalences.items():
            category_id = self.get_category_id(category)
            updates = self.set_category(category_id, keywords)

            logger.info(f"Category insertions {updates} for [{category}]")
            self.counter_total.increment(updates)

        logger.info(f"Total updated rows {self.counter_total.value()}")
