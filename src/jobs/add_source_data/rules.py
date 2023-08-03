from typing import Dict, Optional

import pandas as pd

from utils.config import get_config
from utils.logging import get_logger
from utils.paths import CONFIG_RULES

logger = get_logger(__name__)


class Rules:
    def __init__(self):
        self._rules: Dict = get_config(CONFIG_RULES)

    def build_filter(self, data: pd.DataFrame, rule: Dict) -> Optional[pd.Series]:
        """from rule get a boolean series with the corresponding rule"""
        data_filter = None
        for field, value in rule.items():
            if data_filter is None:
                data_filter = data[field] == value
            else:
                data_filter = data_filter & (data[field] == value)
        return data_filter

    def exclude(self, data: pd.DataFrame) -> pd.DataFrame:
        """remove from dataframe all those rows matching the rule criteria"""
        logger.info("Applying EXCLUDE rules.")

        for rule in self._rules["EXCLUDE"]:
            data_filter = self.build_filter(data, rule)
            if data_filter is not None:
                data = data.drop(data[data_filter].index, axis=0)

        return data

    def savings(self, data: pd.DataFrame) -> pd.DataFrame:
        """set amount to 0 in those rows representing savings"""
        logger.info("Applying SAVINGS rules.")

        for rule in self._rules["SAVINGS"]:
            data_filter = self.build_filter(data, rule)
            if data_filter is not None:
                data.loc[data_filter, "amount"] = 0

        return data

    def apply(self, data: pd.DataFrame) -> pd.DataFrame:
        return data.pipe(self.exclude).pipe(self.savings)
