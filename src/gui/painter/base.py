from abc import ABC, abstractmethod
from typing import Iterable, List

from matplotlib import pyplot as plt

from src.gui.service.data import DataService


class BasePainter(ABC):
    def __init__(self, data_service: DataService):
        self.data_service = data_service
        self.text_format = {
            "color": "white",
            "weight": "bold",
            "fontsize": 10,
            "zorder": 3,
        }

        self._cmap = plt.get_cmap("viridis")

    @abstractmethod
    def paint(self, **kwargs) -> plt.Figure:
        raise NotImplementedError

    def _remove_spines(self, ax: plt.Axes):
        for spine in ax.spines.values():
            spine.set_visible(False)

    def _remove_tick_params(self, ax: plt.Axes):
        ax.tick_params(axis="x", bottom=False)
        ax.tick_params(axis="y", left=False)

    def _color_gradient(self, values: Iterable) -> List:
        norm = plt.Normalize(min(values), max(values))
        return [self._cmap(norm(v)) for v in values]

    def _money_to_string(self, value: int) -> str:
        return f"{round(value / 1000.0, 1)} k€".rjust(7)
