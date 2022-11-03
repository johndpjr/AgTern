from pydantic import ValidationError
from sqlalchemy.orm import Session

from . import DatabaseInternship
from ...common import LOG, Internship, InternshipCreateSchema


def get_internship(db: Session, internship_id: int) -> Internship:
    """Gets an internship by internship_id."""
    return db.query(DatabaseInternship)\
        .filter(DatabaseInternship.id == internship_id)\
        .first()

def get_all_internships(db: Session, skip: int = 0, limit: int = 100) -> list[Internship]:
    """Gets all internships. Use skip and limit to offset and limit number of results."""
    return db.query(DatabaseInternship)\
        .offset(skip)\
        .limit(limit)\
        .all()


def create_internships(db: Session, *internships: InternshipCreateSchema):
    db_internships = []
    for internship in internships:
        try:
            db_internships.append(DatabaseInternship(**internship.dict()))
        except ValidationError as errors:
            LOG.error("Could not create internship!")
            LOG.error(errors)
            return None

    db.add_all(db_internships)
    db.commit()
    # Maybe call db.refresh()?
    return db_internships

def create_internship(db: Session, internship: InternshipCreateSchema):
    """Creates an internship in the database."""
    ret = create_internships(db, internship)
    if ret is None or len(ret) == 0:
        return None
    else:
        return ret[0]  # We know here that len == 1
