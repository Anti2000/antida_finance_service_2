from fastapi import Depends
from sqlalchemy import select
from sqlalchemy import desc

from .exceptions import OperationCategoryNotFound
from .exceptions import OperationShopNotFound
from .filters import OperationsFilter
from .filters import CategoryFilter
from .filters import ShopFilter
from .filters import DateFromFilter
from .filters import DateToFilter
from .models import Operation
from .schemas import OperationCreate
from .schemas import Report
from .utils import OperationReport
from ..categories.exceptions import CategoryNotFound
from ..categories.services import CategoryService
from ..config import Settings
from ..config import get_settings
from ..database import Session
from ..database import get_session
from ..shops.exceptions import ShopNotFound
from ..shops.services import ShopService


class OperationService:
    BUY = 'buy'
    SALE = 'sale'

    def __init__(
            self,
            session: Session = Depends(get_session),
            settings: Settings = Depends(get_settings),
    ):
        self.session = session
        self.settings = settings

    def get_report(self, operations: list[Operation], operation_report: Report) -> Report:
        types_of_operations = {
            self.SALE: OperationReport(self.SALE),
            self.BUY: OperationReport(self.BUY)
        }
        months_range = set()

        for operation in operations:
            operation.date = operation.date.replace(day=1)
            months_range.add(operation.date)
            path = self.generate_operation_path(operation)
            types_of_operations[operation.type].add_row(operation, path)

        operation_report.months_range = sorted(months_range)
        operation_report.content = types_of_operations

        return operation_report

    def create_operation(
            self,
            operation_create: OperationCreate,
            category_service: CategoryService,
            shop_service: ShopService,
            account_id: int
    ) -> Operation:

        if operation_create.category_id is not None:
            self.validate_category(
                category_service=category_service,
                account_id=account_id,
                category_id=operation_create.category_id
            )

        self.validate_shop(
            shop_service=shop_service,
            account_id=account_id,
            shop_id=operation_create.shop_id,
        )

        operation_create = self._convert_price_into_kopecks(operation_create)

        operation = Operation(
            type=operation_create.type,
            date=operation_create.date,
            account_id=account_id,
            shop_id=operation_create.shop_id,
            category_id=operation_create.category_id,
            name=operation_create.name,
            price=operation_create.price,
            amount=operation_create.amount,
        )

        self.session.add(operation)
        self.session.commit()

        return self._convert_price_into_rubles(operation)

    def get_operations(self, account_id: int, operations_filter: OperationsFilter) -> list[Operation]:
        operations = self._get_operations(operations_filter, account_id)

        return [self._convert_price_into_rubles(operation) for operation in operations]

    def _get_operations(self, operations_filter: OperationsFilter, account_id: int) -> list[Operation]:
        query = select(Operation).where(Operation.account_id == account_id).order_by(desc(Operation.date))
        filters = (
            DateFromFilter(operations_filter.date_from),
            DateToFilter(operations_filter.date_to),
            CategoryFilter(operations_filter.categories),
            ShopFilter(operations_filter.shops),
        )

        for one_filter in filters:
            if one_filter.should_run():
                query = one_filter.apply(query)

        return self.session.execute(query).scalars().all()

    def _convert_price_into_kopecks(self, operation_create: OperationCreate) -> OperationCreate:
        operation_create.price = abs(self._rubles_to_kopecks(operation_create.price))

        return operation_create

    def _convert_price_into_rubles(self, operation: Operation) -> Operation:
        operation.price = self._kopecks_to_rubles(operation.price)

        return operation

    @classmethod
    def generate_operation_path(cls, operation: Operation) -> list[str]:
        return [operation.shop.name, operation.category.name or 'Без категории', operation.name]

    @classmethod
    def validate_category(
            cls,
            category_service: CategoryService,
            category_id: int,
            account_id: int
    ) -> None:
        try:
            category_service.validate_category_on_exist(category_id, account_id)
        except CategoryNotFound:
            raise OperationCategoryNotFound from None

    @classmethod
    def validate_shop(
            cls,
            shop_service: ShopService,
            shop_id: int,
            account_id: int
    ) -> None:
        try:
            shop_service.validate_shop_on_exist(shop_id, account_id)
        except ShopNotFound:
            raise OperationShopNotFound from None

    @classmethod
    def _rubles_to_kopecks(cls, rubles):
        return rubles * 100

    @classmethod
    def _kopecks_to_rubles(cls, kopecks):
        return kopecks / 100
