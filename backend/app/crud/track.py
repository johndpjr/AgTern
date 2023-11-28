from typing import List

from sqlalchemy.orm import Session

from backend.app.models import JobTrack as JobTrackModel
from backend.app.models import UserJobTrack as UserJobTrackModel
from backend.app.schemas import JobTrack as JobTrackSchema
from backend.app.schemas import UserJobTrack as UserJobTrackSchema


def get_user_job_track(
    db: Session, job_id: int, user_id: int
) -> List[UserJobTrackSchema]:
    return (
        db.query(UserJobTrackModel)
        .filter(
            UserJobTrackModel.job_id == job_id, UserJobTrackModel.user_id == user_id
        )
        .first()
    )


def create_user_job_track(db: Session, job_id: int, user_id: int) -> UserJobTrackSchema:
    user_job_track = UserJobTrackModel(job_id=job_id, user_id=user_id)
    db.add(user_job_track)
    db.commit()
    return db.query(UserJobTrackModel).order_by(UserJobTrackModel.id.desc()).first()


def get_track_points(db: Session, job_id: int, user_id: int) -> List[JobTrackSchema]:
    """Get all tracking points for a job."""
    user_job_track_id = (
        db.query(UserJobTrackModel.id)
        .filter(
            UserJobTrackModel.user_id == user_id, UserJobTrackModel.job_id == job_id
        )
        .first()
    )
    return (
        db.query(JobTrackModel)
        .filter(JobTrackModel.user_job_track_id == user_job_track_id)
        .all()
    )


def create_track_point(db: Session, track: JobTrackModel):
    """Creates a job track point."""

    db.add(track)
    db.commit()
    return db.query(JobTrackModel).order_by(JobTrackModel.id.desc()).first()


def delete_track():
    pass


def update_track():
    pass


def get_track_statuses(db: Session):
    return []
