from matplotlib import pyplot as plt
from matplotlib.colors import to_hex

from src.gui.painter.base import BasePainter


class CategoricalExpensesAnalysisBasePainter(BasePainter):
    def paint(self, **kwargs) -> plt.Figure:
        year: int = kwargs["year"]

        data = self.data_service.categorized_expenses_for_year(year)

        colormap_name = "Set2"
        cmap = plt.get_cmap(colormap_name)
        num_colors = len(data)
        custom_cmap = cmap(range(num_colors))
        custom_colors = [to_hex(color) for color in custom_cmap]

        fig, ax = plt.subplots()
        patches, texts, autotexts = ax.pie(
            data.share,
            labels=data.index,
            autopct="%1.2f%%",
            colors=custom_colors,
            startangle=90,
            counterclock=False,
            # labeldistance=0.75,
            pctdistance=0.7,
            wedgeprops={"linewidth": 1, "edgecolor": "white"},
            explode=len(data) * [0.02],
        )

        # Customize text labels
        for text in texts:
            text.set_horizontalalignment("center")

        # Customize percent labels
        for autotext in autotexts:
            autotext.set_horizontalalignment("center")
            autotext.set_fontstyle("italic")

        return fig
