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


class InternshipBase(BaseModel):
    id: Union[
        int, None
    ] = None  # Auto-incremented primary key, leave None for automatic id
    job_id: str = ""
    company: str = ""
    title: str = ""
    category: str = ""
    link: str = ""
    apply_link: str = ""
    period: Season = Season.unknown
    year: int = 0
    post_date: str = ""  # See models.py on why this is a string
    location: str = ""
    description: str = ""


class InternshipCreate(InternshipBase):
    pass


class Internship(InternshipBase):
    """Models internship details."""

    class Config:
        validate_assignment = True
        orm_mode = True

    @validator("period", pre=True)
    def validate_period(cls, value):
        if isinstance(value, str):
            return value.capitalize()
        else:
            return value
