import pandas as pd

from src.commands.add_data.readers.base import Reader
from src.commands.add_data.readers.validation import validate_data


class N26(Reader):
    csv_format = {"usecols": ["Fecha", "Beneficiario", "Cantidad (EUR)"]}

    @validate_data
    def read(self, file):
        data = pd.read_csv(file, **self.csv_format)
        data = data.rename(
            {"Fecha": "date", "Beneficiario": "concept", "Cantidad (EUR)": "amount"},
            axis=1,
        )
        data["date"] = pd.to_datetime(data["date"], format="%Y-%m-%d")
        data["origin"] = str(self)
        data["total"] = None
        return data
