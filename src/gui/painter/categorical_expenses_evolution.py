from matplotlib import pyplot as plt

from src.gui.painter.base import BasePainter


class CategoricalExpensesEvolutionPainter(BasePainter):
    def paint(self, **kwargs) -> plt.Figure:
        category: str = kwargs["category"]

        data = self.data_service.expenses_per_category_per_year(category)

        fig, ax = plt.subplots()
        colors = self._color_gradient(data.amount)
        ax.bar(data.index, abs(data.amount), color=colors, zorder=2)

        self._remove_spines(ax)
        self._remove_tick_params(ax)

        ax.grid(axis="y", zorder=1)
        ax.set_ylabel("€", loc="top", rotation=0)

        return fig
