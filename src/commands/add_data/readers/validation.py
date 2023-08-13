from functools import wraps
from typing import Callable

import pandera as pa

schema = pa.DataFrameSchema(
    {
        "amount": pa.Column(float, coerce=True),
        "concept": pa.Column(str),
        "date": pa.Column("datetime64"),
        "origin": pa.Column(str),
        "total": pa.Column(float, coerce=True, nullable=True),
    }
)


def validate_data(func: Callable):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return schema(result)

    return wrapper
