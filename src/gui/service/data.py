from typing import List

import pandas as pd

from repositories import CategoriesRepository, FinancesRepository


class DataService:
    def __init__(
        self,
        repo_categories: CategoriesRepository,
        repo_finances: FinancesRepository,
    ):
        self.data = pd.merge(
            left=repo_categories.get(),
            right=repo_finances.get(),
            how="outer",
            left_on="id",
            right_on="category_id",
            suffixes=("_categories", "_finances"),
        )
        # Convert savings amount to 0
        self.data.loc[self.data["category"] == "SAVINGS", "amount"] = 0

        # Update total column in proper order and including savings
        self.data = self.data.sort_values("date").reset_index(drop=True)
        self.data["total"] = (
            self.data.amount.cumsum()
            + self.data.total.iloc[0]
            - self.data.amount.iloc[0]
        )

        # Discard and create columns
        self.data = self.data[["date", "concept", "amount", "total", "category"]]
        self.data["category"] = self.data["category"].fillna("UNCATEGORIZED")
        self.data["year"] = pd.to_datetime(self.data["date"]).dt.year

    @property
    def years(self) -> List[int]:
        return list(self.data["year"].unique())

    @property
    def categories(self) -> List[str]:
        return sorted(self.data["category"].unique())

    @property
    def reduced_df(self) -> pd.DataFrame:
        data = self.data[["date", "concept", "amount", "total", "category"]]
        data.loc[:, "concept"] = data["concept"].replace(
            r"COMPRA TARJ. \d{4}X{8}\d{4}", "COMPRA TARJ. ", regex=True
        )  # using loc to avoid warnings
        return data.sort_values("date", ascending=False).reset_index(drop=True)

    def total_salary_per_year(self) -> pd.DataFrame:
        return (
            self.data[self.data.category == "SALARY"][["amount", "year"]]
            .groupby(by=["year"])
            .sum()
        )

    def expenses_per_category_per_year(self, category: str) -> pd.DataFrame:
        data = self.data[self.data.category == category]
        data = data[["amount", "year"]]
        data = data.groupby(by=["year"]).sum()
        return data

    def categorized_expenses_for_year(self, year: int) -> pd.DataFrame:
        # Group by category
        data = self.data[self.data.year == year]
        data = data[["amount", "category"]]
        data = data.groupby(by=["category"]).sum()

        # Remove income categories
        data = data[data.amount < 0]

        # Compute share
        data.amount = abs(data.amount)
        data["share"] = 100 * data.amount / sum(data.amount)
        data = data.drop(columns="amount")

        # Group all of those representing less than 5%
        data_representative = data[data.share >= 5]
        data_grouped = data[data.share <= 5]
        remaining = pd.DataFrame(
            {"share": sum(data_grouped.share)}, index=["REMAINING"]
        )

        return pd.concat([data_representative, remaining])

    def total_money(self) -> pd.DataFrame:
        data = self.data.sort_values(by="date")
        return data[["date", "total"]]

    def yearly_savings(self) -> pd.Series:
        first = self.data.groupby("year").first().total
        last = self.data.groupby("year").last().total
        return last - first
