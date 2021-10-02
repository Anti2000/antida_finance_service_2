from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String
)
from sqlalchemy.orm import relationship

from ..database import Base


class Shop(Base):
    __tablename__ = 'shop'

    id = Column(Integer, primary_key=True)
    account_id = Column(ForeignKey('account.id', ondelete='CASCADE'), nullable=False)
    name = Column(String, nullable=False)

    account = relationship('Account', back_populates='shops')
    operations = relationship('Operation', back_populates='shop')
