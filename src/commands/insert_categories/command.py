from src.commands.base.command import Command
from src.commands.insert_categories.service import InsertCategoriesService
from src.utils.config import get_config
from src.utils.counter import Counter
from src.utils.logging import get_logger
from src.utils.paths import paths

logger = get_logger(__name__)


class InsertCategoriesCommand(Command):
    def __init__(self, service: InsertCategoriesService) -> None:
        self.service = service
        self.categories = get_config(paths.config_categories)
        self.counter = Counter(initial=0)

    def execute(self) -> None:
        for category, keywords in self.categories.items():
            updates = self.service.update_category(category, keywords)

            logger.info(f"Category insertions {updates} for [{category}]")
            self.counter.increment(updates)

        logger.info(f"Total updated rows {self.counter.value()}")
