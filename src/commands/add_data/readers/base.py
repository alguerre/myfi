from abc import ABC, abstractmethod

import pandas as pd


class Reader(ABC):
    def __str__(self):
        return self.__class__.__name__

    @abstractmethod
    def read(self, file: str) -> pd.DataFrame:
        pass
