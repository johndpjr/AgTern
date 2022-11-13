from typing import List, Tuple

from pydantic import ValidationError
from sqlalchemy.orm import Session

from agtern.common import LOG, Internship, InternshipCreateSchema

from .models import DatabaseInternship


def convert_internships(*db_internships: DatabaseInternship) -> List[Internship]:
    """Converts DatabaseInternships as stored in the database to an Internship that can be returned to the user"""
    internships = []
    for db_internship in db_internships:
        try:
            data = {
                column: getattr(db_internship, column)
                for column in Internship.__fields__.keys()
                if column in DatabaseInternship.__table__.columns.keys()
            }
            internships.append(
                Internship(
                    **{
                        k: v
                        for k, v in data.items()
                        if v is not None
                        and len(str(v)) != 0  # Don't add Nones or empty strings
                    }
                )
            )
        except ValidationError as errors:
            LOG.error("Unable to create Internship!")
            LOG.error(f"DatabaseInternship: {db_internship}")
            LOG.error(errors)
    return internships


def convert_internship(internship) -> Internship:
    ret = convert_internships(internship)
    return ret[0]


def get_internship(db: Session, internship_id: int) -> Internship:
    """Gets an internship by internship_id."""
    return convert_internship(
        db.query(DatabaseInternship)
        .filter(DatabaseInternship.id == internship_id)
        .first()
    )


def get_all_internships(
    db: Session, skip: int = 0, limit: int = 100
) -> list[Internship]:
    """Gets all internships. Use skip and limit to offset and limit number of results."""
    return convert_internships(
        *db.query(DatabaseInternship).offset(skip).limit(limit).all()
    )


def create_internships(
    db: Session, *internships: DatabaseInternship
) -> List[Internship]:
    if len(internships) > 0:
        db.add_all(internships)
        db.commit()
        # Maybe call db.refresh()?
    return convert_internships(*internships)


def create_internship(db: Session, internship: DatabaseInternship) -> Internship:
    """Creates an internship in the database."""
    ret = create_internships(db, internship)
    return ret[0]
