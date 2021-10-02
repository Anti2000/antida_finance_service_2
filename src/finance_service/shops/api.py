from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from .exceptions import ShopNotFound
from .schemas import Shop as ShopSchema
from .schemas import ShopCreate
from .schemas import ShopUpdate
from .services import ShopService
from ..auth.dependencies import get_current_account
from ..auth.schemas import AuthAccount

router = APIRouter()


@router.post(
    '/shops',
    response_model=ShopSchema,
    status_code=status.HTTP_201_CREATED
)
def create_shop(
        shop_create: ShopCreate,
        current_account: AuthAccount = Depends(get_current_account),
        service: ShopService = Depends(),

):
    shop = service.create_shop(shop_create, current_account.id)
    return shop


@router.patch('/shops/{shop_id}', response_model=ShopSchema)
def edit_shop(
        shop_id: int,
        shop_update: ShopUpdate,
        current_account: AuthAccount = Depends(get_current_account),
        service: ShopService = Depends(),
):
    try:
        shop = service.update_shop(shop_id, shop_update, current_account.id)
        return shop
    except ShopNotFound:
        raise HTTPException(status.HTTP_404_NOT_FOUND) from None


@router.delete('/shops/{shop_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_shop(
        shop_id: int,
        current_account: AuthAccount = Depends(get_current_account),
        service: ShopService = Depends(),
):
    try:
        service.delete_shop(shop_id, current_account.id)
    except ShopNotFound:
        raise HTTPException(status.HTTP_404_NOT_FOUND) from None
