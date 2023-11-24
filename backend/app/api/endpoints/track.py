from typing import Annotated, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.crud import track as crud
from backend.app.models import JobTrack as TrackModel
from backend.app.schemas import JobTrack as TrackSchema
from backend.app.schemas import JobTrackCreate as TrackCreate

from ..deps import get_db
from .login import User, get_current_active_user

router = APIRouter()


@router.get("/", response_model=List[TrackSchema])
async def get_track_points(
    current_user: Annotated[User, Depends(get_current_active_user)],
    job_id: int,
    db: Session = Depends(get_db),
):
    """Returns all jobs from the database."""
    return crud.get_track_points(db, job_id, current_user.id)


@router.post("/", response_model=TrackSchema)
async def create_track_point(track: TrackCreate, db: Session = Depends(get_db)):
    """Adds a JobTrack object to the database."""
    db_track = TrackModel(
        **{
            k: v
            for k, v in track.dict().items()
            if k in TrackModel.__table__.columns.keys() and v is not None
        }
    )
    return crud.create_track_point(db, db_track)
