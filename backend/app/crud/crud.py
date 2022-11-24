from typing import List

from pydantic import ValidationError
from sqlalchemy import or_
from sqlalchemy.orm import Session

from backend.app.models import Internship as InternshipModel
from backend.app.schemas import Internship as InternshipSchema
from backend.app.utils import LOG


def convert_internships(*db_internships: InternshipModel) -> List[InternshipSchema]:
    """Converts InternshipModels as stored in the database to an Internship that can be returned to the user"""
    internships = []
    for db_internship in db_internships:
        try:
            data = {
                column: getattr(db_internship, column)
                for column in InternshipSchema.__fields__.keys()
                if column in InternshipModel.__table__.columns.keys()
            }
            internships.append(
                InternshipSchema(
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
            LOG.error(f"InternshipModel: {db_internship}")
            LOG.error(errors)
    return internships


def convert_internship(internship) -> InternshipSchema:
    ret = convert_internships(internship)
    return ret[0]


def get_internship(db: Session, internship_id: int) -> InternshipSchema:
    """Gets an internship by internship_id."""
    return convert_internship(
        db.query(InternshipModel).filter(InternshipModel.id == internship_id).first()
    )


def get_all_internships(
    db: Session, skip: int = 0, limit: int = 100
) -> list[InternshipSchema]:
    """Gets all internships. Use skip and limit to offset and limit number of results."""
    return convert_internships(
        *db.query(InternshipModel).offset(skip).limit(limit).all()
    )


def create_internships(
    db: Session, *internships: InternshipModel
) -> List[InternshipSchema]:
    if len(internships) > 0:
        db.add_all(internships)
        db.commit()
        # Maybe call db.refresh()?
    return convert_internships(*internships)


def create_internship(db: Session, internship: InternshipModel) -> InternshipSchema:
    """Creates an internship in the database."""
    ret = create_internships(db, internship)
    return ret[0]


def search_internships(db: Session, q: str = None, skip: int = 0, limit: int = 1000):
    terms = q.lower().strip().split()
    conditions = []
    for column in ["job_id", "company", "title", "category", "location"]:
        for term in terms:
            # Test if the column contains a word that starts with the term
            conditions.append(getattr(InternshipModel, column).ilike(f"%{term}%"))
    results = (
        db.query(InternshipModel)
        .filter(or_(*conditions))
        .offset(skip)
        .limit(limit)
        .all()
    )
    if len(results) < limit:
        conditions = []
        for term in terms:
            # Test if the column contains a word that starts with the term
            conditions.append(InternshipModel.description.ilike(f"%{term}%"))
        description_results = (
            db.query(InternshipModel)
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
    return convert_internships(*results)
