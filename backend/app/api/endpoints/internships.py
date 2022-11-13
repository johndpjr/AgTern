from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app import crud, models, schemas

from ..deps import get_db

router = APIRouter()


@router.get("/", response_model=List[schemas.Internship])
async def get_all_internships(db: Session = Depends(get_db)):
    """Returns all internships from the database"""
    return crud.get_all_internships(db)


@router.post("/", response_model=schemas.Internship)
async def create_internship(
    internship: schemas.InternshipCreate, db: Session = Depends(get_db)
):
    """Adds an Internship object to the database."""
    db_internship = models.Internship(
        **{
            k: v
            for k, v in internship.dict().items()
            if k in models.Internship.__table__.columns.keys() and v is not None
        }
    )
    return crud.create_internship(db, db_internship)


# @router.delete("/")
# def delete_internship(internship_id: int, db: Session = Depends(get_db)):
#     if not crud.internship_exists(db, internship_id):
#         raise HTTPException(status_code=400, detail="Internship not found")
#     crud.delete_internship(db=db, internship_id=internship_id)
#
#
# @router.put("/")
# def update_internship(internship: schemas.Internship, db: Session = Depends(get_db)):
#     if not crud.internship_exists(db, internship.id):
#         raise HTTPException(status_code=400, detail="Internship not found")
#     crud.update_internship(db=db, internship=internship)
