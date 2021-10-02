from typing import Optional
from datetime import date

from fastapi import Query

from finance_service.operations.models import Operation


class BaseOperationFilter:
    def should_run(self) -> bool:
        pass

    def apply(self, query):
        pass


class OperationsFilter:
    def __init__(
            self,
            date_from: Optional[date] = None,
            date_to: Optional[date] = None,
            shops: Optional[list[int]] = Query(None),
            categories: Optional[list[int]] = Query(None)
    ):
        self.date_from = date_from
        self.date_to = date_to
        self.shops = shops
        self.categories = categories


class DateFromFilter(BaseOperationFilter):
    def __init__(self, date_from: Optional[date] = None):
        self.date_from = date_from

    def should_run(self) -> bool:
        return self.date_from is not None

    def apply(self, query):
        return query.where(Operation.date >= self.date_from)


class DateToFilter(BaseOperationFilter):
    def __init__(self, date_to: Optional[date] = None):
        self.date_to = date_to

    def should_run(self) -> bool:
        return self.date_to is not None

    def apply(self, query):
        return query.where(Operation.date <= self.date_to)


class CategoryFilter(BaseOperationFilter):
    def __init__(self, categories: Optional[date] = None):
        self.categories = categories

    def should_run(self) -> bool:
        return self.categories is not None

    def apply(self, query):
        return query.where(Operation.category_id.in_(self.categories))


class ShopFilter(BaseOperationFilter):
    def __init__(self, shops: Optional[date] = None):
        self.shops = shops

    def should_run(self) -> bool:
        return self.shops is not None

    def apply(self, query):
        return query.where(Operation.shop_id.in_(self.shops))
