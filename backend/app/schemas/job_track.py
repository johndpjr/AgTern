from enum import Enum
from typing import Union

from pydantic import BaseModel


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


class JobTrackBase(BaseModel):
    status: Union[JobStatusType, None] = None
    timestamp: Union[str, None] = None


class JobTrackCreate(JobTrackBase):
    job_id: Union[int, None] = None


class JobTrack(JobTrackBase):
    """Models job track items."""

    id: Union[int, None] = None
    user_job_track_id: Union[int, None] = None

    class Config:
        validate_assignment = True
        orm_mode = True
