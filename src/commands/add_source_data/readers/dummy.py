import pandas as pd

from src.commands.add_source_data.readers.base import Reader
from src.commands.add_source_data.readers.validation import validate_data


class Dummy(Reader):
    @validate_data
    def read(self, file):
        data = pd.read_csv(file)
        data["date"] = pd.to_datetime(data["date"], format="%Y-%m-%d")
        return data
