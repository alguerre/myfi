from sqlalchemy import (Boolean, Column, Date, DateTime, ForeignKey, Integer,
                        Text)
from sqlalchemy.sql import func
from sqlalchemy.types import DECIMAL

from src.utils.database import Base


class Finances(Base):
    __tablename__ = "finances"

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=False)
    concept = Column(Text, nullable=False)
    amount = Column(DECIMAL(12, 2), nullable=False)
    total = Column(DECIMAL(12, 2))
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    automatic = Column(Boolean)

    created_on = Column(DateTime(timezone=True), server_default=func.now())
    updated_on = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return "<FinancesRow(id='%s', date='%s', amount='%s', category_id='%s')>" % (
            self.id,
            self.date,
            self.amount,
            self.category_id,
        )
