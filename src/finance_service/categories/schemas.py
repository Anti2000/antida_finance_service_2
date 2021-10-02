from pydantic import BaseModel


# Нужна ли схема CategoryUpdate ?
# Стоит ли реализовать наследование классов-схем от базового класса-схемы ?
class Category(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class CategoryCreate(BaseModel):
    name: str


class CategoryUpdate(BaseModel):
    name: str
