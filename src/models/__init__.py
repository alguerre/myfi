from .categories import Categories
from .finances import Finances
from .finances import Base  # for alembic

TABLES = [Categories.__table__, Finances.__table__]
