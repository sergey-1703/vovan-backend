from pydantic import BaseModel, EmailStr
from typing import Optional


class UserBase(BaseModel):
    login: str
    nickname: Optional[str] = None
    about: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int


class UserInDB(UserBase):
    id: int
    password_hash: str