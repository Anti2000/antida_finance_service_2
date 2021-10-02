from pydantic import BaseModel


class AccountRegister(BaseModel):
    email: str
    password: str
    username: str

    class Config:
        orm_mode = True
