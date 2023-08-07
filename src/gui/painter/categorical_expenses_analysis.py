from typing import List

from matplotlib import pyplot as plt
from matplotlib.colors import to_hex
from matplotlib.text import Text

from src.gui.painter.base import BasePainter


class CategoricalExpensesAnalysisPainter(BasePainter):
    def paint(self, **kwargs) -> plt.Figure:
        year: int = kwargs["year"]

        data = self.data_service.categorized_expenses(year)

        fig, ax = plt.subplots()
        _, texts, autotexts = ax.pie(
            data.share,
            labels=data.index,
            autopct="%1.2f%%",
            colors=self.get_colors(len(data)),
            startangle=90,
            counterclock=False,
            pctdistance=0.7,
            wedgeprops={"linewidth": 1, "edgecolor": "white"},
            explode=len(data) * [0.02],
        )

        self.customize_text_labels(texts)
        self.customize_percent_labels(autotexts)

        return fig

    def get_colors(self, num_colors: int) -> List:
        colormap_name = "Set2"
        cmap = plt.get_cmap(colormap_name)
        custom_cmap = cmap(range(num_colors))
        return [to_hex(color) for color in custom_cmap]

    def customize_text_labels(self, texts: List[Text]):
        for t in texts:
            t.set_horizontalalignment("center")

    def customize_percent_labels(self, texts: List[Text]):
        for t in texts:
            t.set_horizontalalignment("center")
            t.set_fontstyle("italic")
