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


class JobBase(BaseModel):
    id: Union[int, None] = None  # Auto-incremented primary key is None
    company_job_id: str = ""
    company: str = ""
    title: str = ""
    type: str = ""
    category: str = ""
    posting_link: str = ""
    apply_link: str = ""
    period: Season = Season.unknown
    year: int = 0
    post_date: str = ""
    location: str = ""
    description: str = ""
    tags: str = ""


class JobCreate(JobBase):
    pass


class Job(JobBase):
    """Models job details."""

    class Config:
        validate_assignment = True
        orm_mode = True

    @validator("period", pre=True)
    def validate_period(cls, value):
        if isinstance(value, str):
            return value.capitalize()
        else:
            return value
