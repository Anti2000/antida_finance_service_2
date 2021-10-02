from fastapi import Depends

from sqlalchemy import select
from sqlalchemy import delete
from sqlalchemy.exc import NoResultFound

from .exceptions import CategoryNotFound
from .models import Category
from .schemas import CategoryCreate
from .schemas import CategoryUpdate
from ..database import Session
from ..database import get_session


class CategoryService:

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def create_category(self, category_create: CategoryCreate, account_id: int) -> Category:
        category = Category(
            name=category_create.name,
            account_id=account_id
        )
        self.session.add(category)
        self.session.commit()

        return category

    def delete_category(self, category_id: int, account_id: int) -> None:
        category = self._get_category(category_id, account_id)

        self.session.execute(
            delete(Category)
            .where(Category.id == category.id)
        )

        self.session.commit()

    def update_category(
            self,
            category_id: int,
            category_update: CategoryUpdate,
            account_id: int
    ) -> Category:
        category = self._get_category(category_id, account_id)

        for k, v in category_update.dict(exclude_unset=True).items():
            setattr(category, k, v)

        self.session.commit()

        return category

    def validate_category_on_exist(self, category_id: int, account_id: int) -> None:
        self._get_category(category_id, account_id)

    def _get_category(self, category_id: int, account_id: int) -> Category:
        try:
            category = self.session.execute(
                select(Category)
                .where(
                    Category.id == category_id,
                    Category.account_id == account_id
                )
            ).scalar_one()
            return category
        except NoResultFound:
            raise CategoryNotFound from None
