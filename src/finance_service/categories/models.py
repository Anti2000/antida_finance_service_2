from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String

from sqlalchemy.orm import relationship

from ..database import Base


class Category(Base):
    __tablename__ = 'category'

    # составной индекс ??
    id = Column(Integer, primary_key=True)
    account_id = Column(ForeignKey('account.id', ondelete='CASCADE'), nullable=False)
    name = Column(String, nullable=False)

    account = relationship('Account', back_populates='categories')
    operations = relationship('Operation', back_populates='category')
