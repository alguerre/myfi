from ._savings import Savings
from .categories import Categories
from .finances import Finances

TABLES = [Categories.__table__, Finances.__table__, Savings.__table__]
