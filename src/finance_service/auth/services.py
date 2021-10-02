from datetime import datetime
from datetime import timedelta

from fastapi import Depends
from jose import jwt
from passlib.handlers.pbkdf2 import pbkdf2_sha256
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from .schemas import Token
from ..accounts.models import Account
from ..config import Settings
from ..config import get_settings
from ..database import Session
from ..database import get_session
from .exceptions import AccountNotFound
from .exceptions import InvalidCredentialsError


class AuthService:
    def __init__(
            self,
            session: Session = Depends(get_session),
            settings: Settings = Depends(get_settings),
    ):
        self.session = session
        self.settings = settings

    def authenticate(self, username: str, password: str) -> Token:
        try:
            account = self.session.execute(
                select(Account)
                .where(Account.username == username)
            ).scalar_one()
        except NoResultFound:
            raise AccountNotFound from None

        if not pbkdf2_sha256.verify(password, account.password):
            raise InvalidCredentialsError

        return self.create_access_token(account)

    def create_access_token(self, account: Account) -> Token:
        access_token = self.create_token(
            account,
            secret_key=self.settings.secret_key,
            lifetime=self.settings.jwt_access_lifetime,
        )

        return Token(access_token=access_token)

    @classmethod
    def create_token(cls, account: Account, *, secret_key: str, lifetime: int) -> str:
        now = datetime.utcnow()
        return jwt.encode({
            'sub': str(account.id),
            'exp': now + timedelta(seconds=lifetime),
            'iat': now,
            'nbf': now,
            'account': {
                'id': account.id,
                'email': account.email,
                'username': account.username,
            },
        }, secret_key, 'HS256')
