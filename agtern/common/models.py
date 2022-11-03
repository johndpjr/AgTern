from enum import Enum

from pydantic import BaseModel, validator


class Season(str, Enum):
    spring = "Spring"
    summer = "Summer"
    fall = "Fall"
    winter = "Winter"

    def __str__(self):
        return self.value


class Internship(BaseModel):
    """Models internship details."""

    id: int  # Auto-incremented primary key
    company: str = ""
    title: str = ""
    link: str = ""
    period: Season = ""
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
