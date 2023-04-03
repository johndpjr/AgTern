from typing import Union

from pydantic import BaseModel


class JobTrackBase(BaseModel):
    id: Union[int, None] = None
    job_status_id: Union[int, None] = None
    user_job_track_id: Union[int, None] = None
    timestamp: str = None


class JobTrackCreate(JobTrackBase):
    pass


class JobTrack(JobTrackBase):
    """Models job track items."""

    class Config:
        validate_assignment = True
        orm_mode = True
