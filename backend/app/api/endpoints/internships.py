from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.crud import crud
from backend.app.models import Internship as InternshipModel
from backend.app.schemas import Internship as InternshipSchema
from backend.app.schemas import InternshipCreate

from ..deps import get_db

router = APIRouter()


@router.get("/", response_model=List[InternshipSchema])
async def get_all_internships(db: Session = Depends(get_db)):
    """Returns all internships from the database"""
    return crud.get_all_internships(db)


@router.post("/", response_model=InternshipSchema)
async def create_internship(
    internship: InternshipCreate, db: Session = Depends(get_db)
):
    """Adds an Internship object to the database."""
    db_internship = InternshipModel(
        **{
            k: v
            for k, v in internship.dict().items()
            if k in InternshipModel.__table__.columns.keys() and v is not None
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
# def update_internship(internship: InternshipSchema, db: Session = Depends(get_db)):
#     if not crud.internship_exists(db, internship.id):
#         raise HTTPException(status_code=400, detail="Internship not found")
#     crud.update_internship(db=db, internship=internship)
