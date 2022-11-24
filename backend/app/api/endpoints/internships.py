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
async def get_internships(
    db: Session = Depends(get_db), skip: int = 0, limit: int = 100
):
    """Returns all internships from the database"""
    return crud.get_all_internships(db, skip=skip, limit=limit)


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


@router.post("/search", response_model=List[InternshipSchema])
async def search_internships(
    db: Session = Depends(get_db), q: str = None, skip: int = 0, limit: int = 100
):
    """Searches the database for internships"""
    return crud.search_internships(db, q=q, skip=skip, limit=limit)


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
