from enum import Enum

from pydantic import BaseModel, validator


class Season(str, Enum):
    spring = "Spring"
    summer = "Summer"
    fall = "Fall"
    winter = "Winter"

    def __str__(self):
        return self.value


class InternshipBaseModel(BaseModel):
    """Models internship details."""

    company: str = ""
    title: str = ""
    link: str = ""
    period: Season = ""
    year: int = 0
    location: str = ""
    description: str = ""

    class Config:
        validate_assignment = True
