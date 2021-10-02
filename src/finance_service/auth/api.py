from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from fastapi.security import OAuth2PasswordRequestForm

from .schemas import Token
from .services import AuthService
from .exceptions import AccountNotFound
from .exceptions import InvalidCredentialsError

router = APIRouter()


@router.post('/signin', response_model=Token)
def login(
        credentials: OAuth2PasswordRequestForm = Depends(),
        auth_service: AuthService = Depends(),
):
    try:
        return auth_service.authenticate(credentials.username, credentials.password)
    except (AccountNotFound, InvalidCredentialsError):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
