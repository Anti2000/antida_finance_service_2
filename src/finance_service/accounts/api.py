from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from .exceptions import AccountAlreadyExist
from .schemas import AccountRegister
from .services import AccountService
from ..auth.services import AuthService
from ..auth.schemas import Token

router = APIRouter()


@router.post(
    '/signup',
    response_model=Token,
    status_code=status.HTTP_201_CREATED
)
def register_account(
        account_register: AccountRegister,
        service: AccountService = Depends(),
        auth_service: AuthService = Depends()
):
    try:
        account = service.create_account(account_register)
        token = auth_service.create_access_token(account)
        return token
    except AccountAlreadyExist:
        raise HTTPException(status.HTTP_409_CONFLICT) from None
