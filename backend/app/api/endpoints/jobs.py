from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.crud import crud
from backend.app.models import Job as JobModel
from backend.app.schemas import Job as JobSchema
from backend.app.schemas import JobCreate

from ..deps import get_db

router = APIRouter()


@router.get("/", response_model=List[JobSchema])
async def get_jobs(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    """Returns all jobs from the database."""
    return crud.get_all_jobs(db, skip=skip, limit=limit)


@router.post("/", response_model=JobSchema)
async def create_job(job: JobCreate, db: Session = Depends(get_db)):
    """Adds a Job object to the database."""
    db_job = JobModel(
        **{
            k: v
            for k, v in job.dict().items()
            if k in JobModel.__table__.columns.keys() and v is not None
        }
    )
    return crud.create_job(db, db_job)


@router.post("/search", response_model=List[JobSchema])
async def search_jobs(
    db: Session = Depends(get_db), q: str = None, skip: int = 0, limit: int = 100
):
    """Searches the database for jobs."""
    return crud.search_jobs(db, q=q, skip=skip, limit=limit)


# @router.delete("/")
# def delete_job(job_id: int, db: Session = Depends(get_db)):
#     if not crud.job_exists(db, job_id):
#         raise HTTPException(status_code=400, detail="Job not found")
#     crud.delete_job(db=db, job_id=job_id)
#
#
# @router.put("/")
# def update_job(job: JobSchema, db: Session = Depends(get_db)):
#     if not crud.job_exists(db, job.id):
#         raise HTTPException(status_code=400, detail="Job not found")
#     crud.update_job(db=db, job=job)
