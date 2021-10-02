from fastapi import Depends

from sqlalchemy import select
from sqlalchemy import delete
from sqlalchemy.exc import NoResultFound

from .exceptions import ShopNotFound
from ..database import Session
from ..database import get_session
from .schemas import ShopCreate
from .schemas import ShopUpdate
from .models import Shop


class ShopService:

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def create_shop(self, shop_create: ShopCreate, account_id: int) -> Shop:
        shop = Shop(
            name=shop_create.name,
            account_id=account_id
        )

        self.session.add(shop)
        self.session.commit()

        return shop

    def delete_shop(self, shop_id: int, account_id: int) -> None:
        shop = self._get_shop(shop_id, account_id)

        self.session.execute(
            delete(Shop)
            .where(Shop.id == shop.id)
        )

        self.session.commit()

    def update_shop(
            self,
            shop_id: int,
            shop_update: ShopUpdate,
            account_id: int
    ) -> Shop:
        shop = self._get_shop(shop_id, account_id)

        for k, v in shop_update.dict(exclude_unset=True).items():
            setattr(shop, k, v)

        self.session.commit()

        return shop

    def validate_shop_on_exist(self, shop_id: int, account_id: int) -> None:
        self._get_shop(shop_id, account_id)

    def _get_shop(self, shop_id: int, account_id: int) -> Shop:
        try:
            shop = self.session.execute(
                select(Shop)
                .where(
                    Shop.id == shop_id,
                    Shop.account_id == account_id
                )
            ).scalar_one()
            return shop
        except NoResultFound:
            raise ShopNotFound from None
