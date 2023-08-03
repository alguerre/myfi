from sqlalchemy import Column, DateTime, Integer, Text, func

from src.utils.database import Base


class Categories(Base):
    __tablename__ = "categories"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    category = Column(Text)

    created_on = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return "<CategoriesRow(id='%s', category='%s')>" % (
            self.id,
            self.category,
        )
