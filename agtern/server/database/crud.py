from sqlalchemy.orm import Session

from . import models
from ...common import schemas


def get_internship(db: Session, internship_id: int) -> schemas.Internship:
    """Gets an internship by the id."""
    return db.query(models.Internship)\
        .filter(models.Internship.id == internship_id)\
        .first()

def get_all_internships(db: Session, skip: int = 0, limit: int = 100) -> list[schemas.Internship]:
    """Returns all internships."""
    return db.query(models.Internship)\
        .offset(skip)\
        .limit(limit)\
        .all()

def create_internship(db: Session, internship: schemas.InternshipCreate):
    """Creates an internship in the database."""
    db_internship = models.Internship(**internship.dict())
    db.add(db_internship)
    # TODO: commit changes once all of the internships have been scraped for a given site
    db.commit()
    db.refresh(db_internship)
    return db_internship
