from typing import List

from pydantic import ValidationError
from sqlalchemy.orm import Session

from backend.app import models, schemas
from backend.app.utils import LOG


def convert_internships(*db_internships: models.Internship) -> List[schemas.Internship]:
    """Converts models.Internships as stored in the database to an Internship that can be returned to the user"""
    internships = []
    for db_internship in db_internships:
        try:
            data = {
                column: getattr(db_internship, column)
                for column in schemas.Internship.__fields__.keys()
                if column in models.Internship.__table__.columns.keys()
            }
            internships.append(
                schemas.Internship(
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
            LOG.error(f"models.Internship: {db_internship}")
            LOG.error(errors)
    return internships


def convert_internship(internship) -> schemas.Internship:
    ret = convert_internships(internship)
    return ret[0]


def get_internship(db: Session, internship_id: int) -> schemas.Internship:
    """Gets an internship by internship_id."""
    return convert_internship(
        db.query(models.Internship)
        .filter(models.Internship.id == internship_id)
        .first()
    )


def get_all_internships(
    db: Session, skip: int = 0, limit: int = 100
) -> list[schemas.Internship]:
    """Gets all internships. Use skip and limit to offset and limit number of results."""
    return convert_internships(
        *db.query(models.Internship).offset(skip).limit(limit).all()
    )


def create_internships(
    db: Session, *internships: models.Internship
) -> List[schemas.Internship]:
    if len(internships) > 0:
        db.add_all(internships)
        db.commit()
        # Maybe call db.refresh()?
    return convert_internships(*internships)


def create_internship(db: Session, internship: models.Internship) -> schemas.Internship:
    """Creates an internship in the database."""
    ret = create_internships(db, internship)
    return ret[0]
