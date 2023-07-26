from matplotlib import pyplot as plt

from src.gui.painter.base import BasePainter
from src.gui.service.data import DataService


class YearlySalaryBasePainter(BasePainter):
    def __init__(self, data_service: DataService):
        super().__init__(data_service)

    def _paint_values_inside_columns(
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

    def paint(self) -> plt.Figure:
        data = self.data_service.total_salary_per_year()
        fig, ax = plt.subplots()

        ax.set_title("Salary per Year", weight="bold", fontsize=20)

        self._remove_spines(ax)
        self._remove_tick_params(ax)
        colors = self._color_gradient(data.amount)

        max_value, max_year = data.amount.max(), data.amount.idxmax()
        min_value, min_year = (
            data.iloc[1:-1].amount.min(),
            data.iloc[1:-1].amount.idxmin(),
        )
        curr_value, curr_year = data.amount.iloc[-1], data.iloc[-1].name

        self._paint_values_inside_columns(ax, max_value, max_year)
        self._paint_values_inside_columns(ax, min_value, min_year)
        self._paint_values_inside_columns(ax, curr_value, curr_year)

        ax.grid(axis="y", zorder=1)

        ax.bar(data.index, data.amount, color=colors, zorder=2)

        return fig
