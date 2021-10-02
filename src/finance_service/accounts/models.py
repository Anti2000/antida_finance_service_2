from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from sqlalchemy.orm import relationship

from ..database import Base


class Account(Base):
    __tablename__ = 'account'

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)

    shops = relationship('Shop', back_populates='account')
    categories = relationship('Category', back_populates='account')
    operations = relationship('Operation', back_populates='account')
