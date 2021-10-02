from pydantic import BaseModel


# Нужна ли схема ShopUpdate ?
# Реализовать наследование схем ?
class Shop(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class ShopCreate(BaseModel):
    name: str


class ShopUpdate(BaseModel):
    name: str
