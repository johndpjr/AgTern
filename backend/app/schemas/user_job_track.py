from typing import Union

from pydantic import BaseModel


class UserJobTrackBase(BaseModel):
    id: Union[int, None] = None
    job_id: Union[int, None] = None
    user_id: Union[int, None] = None


class UserJobTrackCreate(UserJobTrackBase):
    pass


class UserJobTrack(UserJobTrackBase):
    """Models a user."""

    class Config:
        validate_assignment = True
        orm_mode = True
