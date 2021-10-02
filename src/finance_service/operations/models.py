from sqlalchemy import (
    Column,
    Date,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from ..database import Base


class Operation(Base):
    __tablename__ = 'operation'

    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    account_id = Column(ForeignKey('account.id', ondelete='CASCADE'), nullable=False)
    shop_id = Column(ForeignKey('shop.id', ondelete='CASCADE'), nullable=False)
    category_id = Column(ForeignKey('category.id', ondelete='CASCADE'), nullable=True)
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    amount = Column(Integer, nullable=False)

    account = relationship('Account', back_populates='operations')
    shop = relationship('Shop', back_populates='operations')
    category = relationship('Category', back_populates='operations')
