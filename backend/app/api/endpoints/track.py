from typing import Annotated, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.crud import track as crud
from backend.app.models import JobTrack as JobTrackModel
from backend.app.schemas import JobTrack as JobTrackSchema
from backend.app.schemas import JobTrackCreate as JobTrackCreate

from ..deps import get_db
from .login import User, get_current_active_user

router = APIRouter()


@router.get("/", response_model=List[JobTrackSchema])
async def get_track_points(
    current_user: Annotated[User, Depends(get_current_active_user)],
    job_id: int,
    db: Session = Depends(get_db),
):
    """Returns all jobs."""
    return crud.get_track_points(db, job_id, current_user.id)


@router.post("/", response_model=JobTrackSchema)
async def create_track_point(track: JobTrackCreate, db: Session = Depends(get_db)):
    """Adds a JobTrack."""
    db_track = JobTrackModel(
        **{
            k: v
            for k, v in track.dict().items()
            if k in JobTrackModel.__table__.columns.keys() and v is not None
        }
    )
    return crud.create_track_point(db, db_track)


@router.get("/statuses", response_model=List[JobTrackSchema])
async def get_track_statuses(db: Session = Depends(get_db)):
    """Returns all job track statuses."""
    return crud.get_track_statuses(db)
