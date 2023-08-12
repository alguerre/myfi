from typing import List

from src.commands.base.service import BaseService
from src.commands.insert_categories.uow import InsertCategoriesUow
from src.utils.counter import Counter


class InsertCategoriesService(BaseService):
    def __init__(self, uow: InsertCategoriesUow):
        self.uow = uow
        self.counter = Counter(initial=0)

    def _get_category_id(self, category: str) -> int:
        with self.uow:
            category_id = self.uow.repo_categories.get_id_by_category(category)

            if category_id:
                return category_id

            return self.uow.repo_categories.add(category)

    def _set_category(self, category_id: int, keywords: List[str]) -> int:
        self.counter.reset()

        with self.uow:
            for word in keywords:
                updated_rows = self.uow.repo_finances.update_category(word, category_id)
                self.counter.increment(updated_rows)
            self.uow.commit()

        return self.counter.value()

    def update_category(self, category: str, keywords: List[str]) -> int:
        category_id = self._get_category_id(category)
        return self._set_category(category_id, keywords)
