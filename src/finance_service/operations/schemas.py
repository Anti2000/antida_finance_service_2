from __future__ import annotations

from typing import Optional
from datetime import date

from pydantic import BaseModel


class Operation(BaseModel):
    id: int
    type: str
    date: date
    shop_id: int
    category_id: Optional[int] = None
    name: str
    price: float
    amount: float

    class Config:
        orm_mode = True


class OperationCreate(BaseModel):
    type: str
    date: date
    shop_id: int
    category_id: Optional[int] = None
    name: str
    price: float
    amount: float


class Report:
    content: dict
    months_range: set[date]