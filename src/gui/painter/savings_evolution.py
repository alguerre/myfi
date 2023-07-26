import pandas as pd
from matplotlib import pyplot as plt

from src.gui.painter.base import BasePainter


class SavingsEvolutionBasePainter(BasePainter):
    def _smooth(self, data: pd.Series) -> pd.Series:
        return data.ewm(span=50, adjust=True).mean()

    def paint(self) -> plt.Figure:
        data = self.data_service.total_money()

        fig, ax = plt.subplots()
        ax.plot(data.date, data.total, linewidth=2, alpha=0.5)
        ax.plot(data.date, self._smooth(data.total), linewidth=3, color="orange")

        ax.grid(axis="y", zorder=1)
        ax.set_ylabel("€", loc="top", rotation=0)

        self._remove_spines(ax)
        self._remove_tick_params(ax)

        return fig
