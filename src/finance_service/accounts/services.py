from fastapi import Depends
from passlib.hash import pbkdf2_sha256
from sqlalchemy.exc import IntegrityError

from .exceptions import AccountAlreadyExist
from ..database import Session
from ..database import get_session
from .models import Account
from .schemas import AccountRegister


class AccountService:

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def create_account(self, account_register: AccountRegister) -> Account:
        account = Account(
            email=account_register.email,
            username=account_register.username,
            password=pbkdf2_sha256.hash(account_register.password),
        )
        self.session.add(account)
        try:
            self.session.commit()
            return account
        except IntegrityError:
            raise AccountAlreadyExist from None
