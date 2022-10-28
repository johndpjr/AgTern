from dataclasses import dataclass
from enum import Enum

from pydantic import BaseModel


class Season(Enum):
    spring = "Spring"
    summer = "Summer"
    fall = "Fall"
    winter = "Winter"

    def __str__(self):
        return self.value


class Internship(BaseModel):
    """Models internship details."""

    company: str
    title: str
    link: str
    period: Season = ""
    year: int = ""
    location: str = ""
    description: str = ""
