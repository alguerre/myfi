from abc import ABC, abstractmethod

import pandas as pd


class Repository(ABC):
    @abstractmethod
    def get_all(self) -> pd.DataFrame:
        raise NotImplementedError
