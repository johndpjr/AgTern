from enum import Enum
from typing import Union

from pydantic import BaseModel, validator


class JobStatusType(str, Enum):
    unapplied = "unapplied"
    applying = "applying"
    applied = "applied"
    waiting = "waiting"
    interviewing = "interviewing"
    offer_pending = "offer_pending"
    offer_given = "offer_given"
    offer_rescinded = "offer_rescinded"
    rejected = "rejected"
    withdrew = "withdrew"
    unknown = "unknown"
    accepted_offer = "accepted_offer"
    rejected_offer = "rejected_offer"
    negotiating_offer = "negotiating_offer"
    none = ""

    def __str__(self):
        return self.value if self.value is not None else ""


class JobStatusBase(BaseModel):
    id: Union[int, None] = None
    status: JobStatusType = JobStatusType.none
    description: str = ""


class JobStatusCreate(JobStatusBase):
    pass


class JobStatus(JobStatusBase):
    """Models job status."""

    class Config:
        validate_assignment = True
        orm_mode = True

    @validator("status", pre=True)
    def validate_status(cls, value):
        if isinstance(value, str):
            return value.capitalize()
        else:
            return value
