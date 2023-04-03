from typing import Union

from pydantic import BaseModel


class UserBase(BaseModel):
    id: Union[int, None] = None
    username: str = ""
    password: str = ""


class UserCreate(UserBase):
    pass


class User(UserBase):
    """Models job details."""

    class Config:
        validate_assignment = True
        orm_mode = True
