from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, func
from sqlalchemy.types import DECIMAL

from src.utils.database import Base


class Savings(Base):
    __tablename__ = "savings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=False)
    amount = Column(DECIMAL(12, 2), nullable=False)
    total = Column(DECIMAL(12, 2))
    finance_id = Column(Integer, ForeignKey("finances.id"), nullable=True)

    created_on = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return "<SavingsRow(date='%s', amount='%s', total='%s')>" % (
            self.date,
            self.amount,
            self.total,
        )
