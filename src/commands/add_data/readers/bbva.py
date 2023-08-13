import pandas as pd

from src.commands.add_data.readers.base import Reader
from src.commands.add_data.readers.validation import validate_data


class Bbva(Reader):
    excel_format = {
        "sheet_name": "Informe BBVA",
        "skiprows": list(range(4)),
        "names": [
            "empty",
            "date",
            "date_value",
            "concept",
            "movement",
            "amount",
            "currency",
            "total",
        ],
        "usecols": ["date", "concept", "amount", "total"],
    }

    @validate_data
    def read(self, file):
        data = pd.read_excel(file, **self.excel_format)
        data["date"] = pd.to_datetime(data["date"].dt.date)
        data["origin"] = str(self)
        return data
