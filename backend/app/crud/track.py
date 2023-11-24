from typing import List

from sqlalchemy.orm import Session

from backend.app.models import JobStatus as TrackStatusModel
from backend.app.models import JobTrack as TrackModel
from backend.app.models import UserJobTrack as UserTrackModel
from backend.app.schemas import JobTrack as TrackSchema


def get_track_points(db: Session, job_id: int, user_id: int) -> List[TrackSchema]:
    """Get all tracking points for a job."""
    user_job_track_id = (
        db.query(UserTrackModel.id)
        .filter(UserTrackModel.user_id == user_id, UserTrackModel.job_id == job_id)
        .first()
    )
    return (
        db.query(TrackModel)
        .filter(TrackModel.user_job_track_id == user_job_track_id)
        .all()
    )


def create_track_point(db: Session, track: TrackModel):
    """Creates a job track point."""

    db.add(track)
    db.commit()


def delete_track():
    pass


def update_track():
    pass


def get_track_statuses(db: Session):
    return db.query(TrackStatusModel).all()
