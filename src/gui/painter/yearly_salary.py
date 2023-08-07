import pandas as pd
from matplotlib import pyplot as plt

from src.gui.painter.base import BasePainter


class YearlySalaryPainter(BasePainter):
    def paint(self) -> plt.Figure:
        data = self.data_service.total_salary_per_year()

        colors = self._color_gradient(data.amount)

        fig, ax = plt.subplots()
        ax.bar(data.index, data.amount, color=colors, zorder=2)

        ax.set_title("Salary per Year", weight="bold", fontsize=20)
        ax.grid(axis="y", zorder=1)

        self._remove_spines(ax)
        self._remove_tick_params(ax)

        self.labels_in_column(ax, data)

        return fig

    def labels_in_column(self, ax: plt.Axes, data: pd.DataFrame):
        max_value, max_year = data.amount.max(), data.amount.idxmax()
        min_value, min_year = (  # skip first year, likely incomplete
            data.iloc[1:-1].amount.min(),
            data.iloc[1:-1].amount.idxmin(),
        )
        curr_value, curr_year = data.amount.iloc[-1], data.iloc[-1].name

        self.draw_label_in_column(ax, max_value, max_year)
        self.draw_label_in_column(ax, min_value, min_year)
        self.draw_label_in_column(ax, curr_value, curr_year)

    def draw_label_in_column(
        self,
        ax: plt.Axes,
        value: int,
        year: int,
        year_position_offset: float = 0.35,
        salary_position_offset: int = 5000,
    ):
        ax.text(
            year - year_position_offset,
            value - salary_position_offset,
            self._money_to_string(value),
            **self.text_format,
        )
