from typing import List

from pydantic import ValidationError
from sqlalchemy import delete, or_
from sqlalchemy.orm import Session

from backend.app.models import Job as JobModel
from backend.app.schemas import Job as JobSchema
from backend.app.utils import LOG

def convert_jobs(*db_jobs: JobModel) -> List[JobSchema]:
    """Converts JobModels as stored in the database to a Job."""
    jobs = []
    for db_job in db_jobs:
        try:
            data = {
                column: getattr(db_job, column)
                for column in JobSchema.__fields__.keys()
                if column in JobModel.__table__.columns.keys()
            }
            jobs.append(
                JobSchema(
                    **{
                        k: v
                        for k, v in data.items()
                        if v is not None
                        and len(str(v)) != 0  # Don't add Nones or empty strings
                    }
                )
            )
        except ValidationError as errors:
            LOG.error("Unable to create Job!")
            LOG.error(f"JobModel: {db_job}")
            LOG.error(errors)
    return jobs

def convert_job(job) -> JobSchema:
    ret = convert_jobs(job)
    return ret[0]

def get_job(db: Session, job_id: int) -> JobSchema:
    """Gets a job by job_id."""
    return convert_job(db.query(JobModel).filter(JobModel.id == job_id).first())

def get_all_jobs(db: Session, skip: int = 0, limit: int = 100) -> list[JobSchema]:
    """Gets all jobs. Use skip and limit to offset and limit the results."""
    return convert_jobs(*db.query(JobModel).offset(skip).limit(limit).all())

def create_jobs(db: Session, *jobs: JobModel) -> List[JobSchema]:
    if len(jobs) > 0:
        db.add_all(jobs)
        db.commit()
        # Maybe call db.refresh()?
    return convert_jobs(*jobs)

def create_job(db: Session, job: JobModel) -> JobSchema:
    """Creates a job in the database."""
    ret = create_jobs(db, job)
    return ret[0]


def search_jobs(db: Session, q: str = None, skip: int = 0, limit: int = 1000):
    terms = q.lower().strip().split()
    conditions = []
    for column in ["company_job_id", "company", "title", "category", "location"]:
        for term in terms:
            # Test if the column contains a word that starts with the term
            conditions.append(getattr(JobModel, column).ilike(f"%{term}%"))
    results = (
        db.query(JobModel).filter(or_(*conditions)).offset(skip).limit(limit).all()
    )
    if len(results) < limit:
        conditions = []
        for term in terms:
            # Test if the column contains a word that starts with the term
            conditions.append(JobModel.description.ilike(f"%{term}%"))
        description_results = (
            db.query(JobModel)
            .filter(or_(*conditions))
            .limit(limit - len(results))
            .all()
        )
        for dresult in description_results:
            found = False
            for result in results:
                if result.id == dresult.id:
                    found = True
                    break
            if not found:
                results.append(dresult)
    return convert_jobs(*results)
