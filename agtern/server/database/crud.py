from pydantic import ValidationError
from sqlalchemy.orm import Session

from . import models
from ...common import LOG, schemas


def get_internship(db: Session, internship_id: int) -> schemas.Internship:
    """Gets an internship by internship_id."""
    return db.query(models.Internship)\
        .filter(models.Internship.id == internship_id)\
        .first()

def get_all_internships(db: Session, skip: int = 0, limit: int = 100) -> list[schemas.Internship]:
    """Gets all internships. Use skip and limit to offset and limit number of results."""
    return db.query(models.Internship)\
        .offset(skip)\
        .limit(limit)\
        .all()

def create_internship(db: Session, internship: schemas.InternshipCreate):
    """Creates an internship in the database."""

    try:
        db_internship = models.Internship(**internship.dict())
    except ValidationError as errors:
        LOG.error("Could not create internship!")
        LOG.error(errors)
        return None
    db.add(db_internship)
    # TODO: commit internships in a batch when site is scraped for efficiency
    #   (i.e. call add() on many internship objects before commit())
    db.commit()
    db.refresh(db_internship)
    return db_internship
