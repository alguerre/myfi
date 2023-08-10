import re
from abc import ABC, abstractmethod
from functools import wraps
from os.path import basename
from typing import Callable

import pandas as pd
import pandera as pa

from src.jobs.add_source_data.error import InvalidFilenameError

schema = pa.DataFrameSchema(
    {
        "date": pa.Column("datetime64"),
        "concept": pa.Column(str),
        "amount": pa.Column(float),
        "total": pa.Column(float, coerce=True, nullable=True),
        "origin": pa.Column(str),
    }
)


def validate_data(func: Callable):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return schema(result)

    return wrapper


def identify_bank(filename: str) -> str:
    regex = r"source_(?P<bank>\w+)_\d{8}_to_\d{8}.(csv|xls)$"
    match = re.search(regex, filename)

    if match:
        return match.group("bank")
    raise InvalidFilenameError(
        f"The provided file [{filename}] do not follow the required format [{regex}]"
    )


def get_reader(file: str) -> "Reader":
    bank = identify_bank(filename=basename(file))
    try:
        return _readers[bank.lower()]
    except KeyError:
        raise NotImplementedError(f"Not available reader for [{bank}]")


class Reader(ABC):
    def __str__(self):
        return self.__class__.__name__

    @abstractmethod
    def read(self, file: str) -> pd.DataFrame:
        pass


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


class Dummy(Reader):
    @validate_data
    def read(self, file):
        data = pd.read_csv(file)
        data["date"] = pd.to_datetime(data["date"], format="%Y-%m-%d")
        return data


_readers = {"n26": N26(), "sabadell": Sabadell(), "dummy": Dummy()}
