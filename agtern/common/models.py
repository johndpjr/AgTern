
"""This file contains Pydantic models that are SHARED between the client and the server (ex: returned by the API)"""

from enum import Enum
from typing import Union

from pydantic import BaseModel, validator


class Season(str, Enum):
    spring = "Spring"
    summer = "Summer"
    fall = "Fall"
    winter = "Winter"
    unknown = ""

    def __str__(self):
        return self.value if self.value is not None else ""


class Internship(BaseModel):
    """Models internship details."""

    id: Union[int, None] = None  # Auto-incremented primary key, leave None for automatic id
    company: str = ""
    title: str = ""
    link: str = ""
    period: Season = Season.unknown
    year: int = 0
    location: str = ""
    description: str = ""

    class Config:
        validate_assignment = True
        orm_mode = True

    @validator("period", pre=True)
    def validate_period(cls, value):
        if isinstance(value, str):
            return value.capitalize()
        else:
            return value
