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
    id: Union[int, None] = None
    job_status: Union[JobStatusType, None] = None
    user_job_track_id: Union[int, None] = None
    timestamp: str = None


class JobTrackCreate(JobTrackBase):
    pass


class JobTrack(JobTrackBase):
    """Models job track items."""

    class Config:
        validate_assignment = True
        orm_mode = True
