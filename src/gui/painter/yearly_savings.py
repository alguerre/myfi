import pandas as pd
from matplotlib import pyplot as plt

from src.gui.painter.base import BasePainter


class YearlySavingsPainter(BasePainter):
    def paint(self) -> plt.Figure:
        data = self.data_service.yearly_savings()

        colors = self._color_gradient(data)

        fig, ax = plt.subplots()
        ax.bar(data.index, data.values, color=colors, zorder=2)

        ax.set_title("Savings per Year", weight="bold", fontsize=20)

        ax.grid(axis="y", zorder=1)

        self._remove_spines(ax)
        self._remove_tick_params(ax)

        self.labels_in_column(ax, data)

        return fig

    def labels_in_column(self, ax: plt.Axes, data: pd.Series):
        max_value, max_year = data.max(), data.idxmax()
        min_value, min_year = (  # skip first year, likely incomplete
            data.iloc[1:-1].min(),
            data.iloc[1:-1].idxmin(),
        )
        curr_value, curr_year = data.iloc[-1], data.index[-1]

        self.draw_label_in_column(ax, max_value, max_year)
        self.draw_label_in_column(ax, min_value, min_year)
        self.draw_label_in_column(ax, curr_value, curr_year)

    def draw_label_in_column(
        self,
        ax: plt.Axes,
        value: int,
        year: int,
        year_position_offset: float = 0.35,
        salary_position_offset: int = 1000,
    ):
        text_format = self.text_format.copy()
        if value < 2000:
            text_format["color"] = "#18191A"
            salary_position_offset = -300

        ax.text(
            year - year_position_offset,
            value - salary_position_offset,
            self._money_to_string(value),
            **text_format,
        )
