import pandas as pd

from src.commands.add_source_data.readers.base import Reader
from src.commands.add_source_data.readers.validation import validate_data


class Sabadell(Reader):
    excel_format = {
        "sheet_name": "Hoja1",
        "skiprows": list(range(8)),
        "names": [
            "date",
            "concept",
            "date_value",
            "amount",
            "total",
            "reference_1",
            "reference_2",
        ],
        "usecols": ["date", "concept", "amount", "total"],
    }

    @validate_data
    def read(self, file):
        data = pd.read_excel(file, **self.excel_format)
        data["date"] = pd.to_datetime(data["date"], format="%d/%m/%Y")
        data["origin"] = str(self)
        return data
