from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from .exceptions import CategoryNotFound
from .schemas import Category as CategorySchema
from .schemas import CategoryCreate
from .schemas import CategoryUpdate
from .services import CategoryService
from ..auth.dependencies import get_current_account
from ..auth.schemas import AuthAccount

router = APIRouter()


@router.post(
    '/categories',
    response_model=CategorySchema,
    status_code=status.HTTP_201_CREATED
)
def create_category(
        category_create: CategoryCreate,
        current_account: AuthAccount = Depends(get_current_account),
        service: CategoryService = Depends(),

):
    category = service.create_category(category_create, current_account.id)
    return category


@router.patch('/categories/{category_id}', response_model=CategorySchema)
def edit_category(
        category_id: int,
        category_update: CategoryUpdate,
        current_account: AuthAccount = Depends(get_current_account),
        service: CategoryService = Depends(),
):
    try:
        category = service.update_category(category_id, category_update, current_account.id)
        return category
    except CategoryNotFound:
        raise HTTPException(status.HTTP_404_NOT_FOUND) from None


@router.delete('/categories/{category_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
        category_id: int,
        current_account: AuthAccount = Depends(get_current_account),
        service: CategoryService = Depends(),
):
    try:
        service.delete_category(category_id, current_account.id)
    except CategoryNotFound:
        raise HTTPException(status.HTTP_404_NOT_FOUND) from None
