from functools import cache, cached_property
from typing import List

import pandas as pd

from src.gui.service.uow import DataUow
from src.utils.logging import get_logger

logger = get_logger(__name__)


class DataService:
    def __init__(
        self,
        uow: DataUow,
    ):
        self.uow = uow

        with uow:
            self._data = pd.merge(
                left=uow.repo_categories.get(),
                right=uow.repo_finances.get(),
                how="right",
                left_on="id",
                right_on="category_id",
                suffixes=("_categories", "_finances"),
            )

        if self._data.empty:
            raise NoDataError("No data has been loaded.")

        # Convert savings amount to 0  # todo: do this concept of SAVINGS makes sense?
        self._data.loc[self._data["category"] == "SAVINGS", "amount"] = 0

        # Update total column in proper order and including savings
        self._data = self._data.sort_values("date").reset_index(drop=True)
        self._data["total"] = (
            self._data.amount.cumsum()
            + self._data.total.iloc[0]
            - self._data.amount.iloc[0]
        )

        # Discard and create columns
        self._data = self._data[["date", "concept", "amount", "total", "category"]]
        self._data["category"] = self._data["category"].fillna("UNCATEGORIZED")
        self._data["year"] = pd.to_datetime(self._data["date"]).dt.year

    @cached_property
    def years(self) -> List[int]:
        return list(self._data["year"].unique())

    @cached_property
    def categories(self) -> List[str]:
        return sorted(self._data["category"].unique())

    @cached_property
    def data(self) -> pd.DataFrame:
        data = self._data.drop(["year"], axis=1)
        data.loc[:, "concept"] = data["concept"].replace(
            r"COMPRA TARJ. \d{4}X{8}\d{4}", "", regex=True
        )  # using loc to avoid warnings
        return data.sort_values("date", ascending=False).reset_index(drop=True)

    @cache
    def total_salary_per_year(self) -> pd.DataFrame:
        return (
            self._data[self._data.category == "SALARY"][["amount", "year"]]
            .groupby(by=["year"])
            .sum()
        )

    @cache
    def expenses_per_category_per_year(self, category: str) -> pd.DataFrame:
        data = self._data[self._data.category == category]
        data = data[["amount", "year"]]
        data = data.groupby(by=["year"]).sum()
        return data

    @cache
    def categorized_expenses(self, year: int) -> pd.DataFrame:
        # Group by category
        data = self._data[self._data.year == year]
        data = data[["amount", "category"]]
        data = data.groupby(by=["category"]).sum()

        # Remove income categories if categorize, else 100% of single category
        data = data[data.amount < 0] if len(data) > 1 else data

        # Compute share
        data.amount = abs(data.amount)
        data["share"] = 100 * data.amount / sum(data.amount)
        data = data.drop(columns="amount")

        # Group all of those representing less than 5%
        data_representative = data[data.share >= 5]
        data_grouped = data[data.share <= 5]

        if data_grouped.empty:
            return data_representative

        remaining = pd.DataFrame(
            {"share": sum(data_grouped.share)}, index=["REMAINING"]
        )
        return pd.concat([data_representative, remaining])

    @cache
    def total_money(self) -> pd.DataFrame:
        data = self._data.sort_values(by="date")
        return data[["date", "total"]]

    @cache
    def yearly_savings(self) -> pd.Series:
        first = self._data.groupby("year").first().total
        last = self._data.groupby("year").last().total
        return last - first


class NoDataError(Exception):
    pass
