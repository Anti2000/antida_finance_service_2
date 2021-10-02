from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from .exceptions import OperationCategoryNotFound
from .exceptions import OperationShopNotFound
from .filters import OperationsFilter
from .schemas import Operation as OperationSchema
from .schemas import Report
from .schemas import OperationCreate
from .services import OperationService
from ..auth.dependencies import get_current_account
from ..auth.schemas import AuthAccount
from ..shops.services import ShopService
from ..categories.services import CategoryService

router = APIRouter()


@router.get(
    '/operations',
    response_model=list[OperationSchema],
)
def get_operations(
        operations_filter: OperationsFilter = Depends(OperationsFilter),
        current_account: AuthAccount = Depends(get_current_account),
        operation_service: OperationService = Depends(),
):
    operations = operation_service.get_operations(current_account.id, operations_filter)

    return operations


@router.get('/operations/report')
def get_report_by_operations(
        operations_filter: OperationsFilter = Depends(OperationsFilter),
        current_account: AuthAccount = Depends(get_current_account),
        operation_service: OperationService = Depends(),
        operation_report: Report = Depends()
):
    operations = operation_service.get_operations(current_account.id, operations_filter)
    report = operation_service.get_report(operations, operation_report)

    return report


@router.post(
    '/operations',
    response_model=OperationSchema,
    status_code=status.HTTP_201_CREATED
)
def create_operation(
        operation_create: OperationCreate,
        current_account: AuthAccount = Depends(get_current_account),
        operation_service: OperationService = Depends(),
        shop_service: ShopService = Depends(),
        category_service: CategoryService = Depends(),
):
    try:
        operation = operation_service.create_operation(
            operation_create=operation_create,
            category_service=category_service,
            shop_service=shop_service,
            account_id=current_account.id,
        )

        return operation

    except (OperationCategoryNotFound, OperationShopNotFound):
        raise HTTPException(status.HTTP_404_NOT_FOUND) from None
