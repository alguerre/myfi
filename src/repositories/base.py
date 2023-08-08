from abc import ABC
from typing import Dict, List, Optional

import pandas as pd
from sqlalchemy import asc, desc, func
from sqlalchemy.orm import Session

from src.utils.database import Base
from src.utils.order import Order


class Repository(ABC):
    def __init__(self, table: Base, session: Session):
        self._table = table
        self._session = session

    def add_bulk(self, data: pd.DataFrame) -> int:
        self._session.bulk_insert_mappings(self._table, data.to_dict("records"))
        return len(data)

    def update(self, params: Dict, values: Dict) -> int:
        filters = self._build_filters(params)
        return self._session.query(self._table).filter(*filters).update(values)

    def get(
        self,
        columns: Optional[List[str]] = None,
        params: Optional[Dict] = None,
        order: Optional[Order] = None,
        limit: Optional[int] = None,
    ) -> pd.DataFrame:
        query = self._session.query(self._table)

        if columns:
            columns = [self._table.__table__.c[col_name] for col_name in columns]
            query = self._session.query(*columns)

        if params:
            filters = self._build_filters(params)
            query = query.filter(*filters)

        if order:
            if order == Order.asc:
                query = query.order_by(asc(*columns))
            elif order == Order.desc:
                query = query.order_by(desc(*columns))

        if limit:
            query = query.limit(limit)

        return pd.read_sql(query.statement, self._session.bind)

    def get_one(
        self,
        columns: Optional[List[str]] = None,
        params: Optional[Dict] = None,
        order: Optional[Order] = None,
    ) -> Dict:
        df = self.get(columns, params, order, 1)

        if df.empty:
            return {}

        return df.iloc[0].to_dict()

    def _build_filters(self, params: Dict) -> Optional[List]:
        filters = []
        for key, value in params.items():
            if "%" in value:
                col = getattr(self._table, key)
                filters.append(func.lower(col).like(value.lower()))
            else:
                filters.append(getattr(self._table, key) == value)
        return filters
